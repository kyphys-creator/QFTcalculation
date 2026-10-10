#!/bin/bash
# MadLoop check of the one-loop phi phi -> phi phi amplitude (research note, step (6)).
#   For each NLO UFO in generated/ (OS: NLOCT's on-shell counterterms; MSbar: pole only):
#   1. copy it to work/ and rename the coupling order PHI -> QCD: MadGraph 3.8.1's loop interface only
#      accepts QCD (or QED) perturbations; the model has no coloured particle, so this is only a label;
#   2. mg5_aMC: generate phi phi > phi phi [virt=QCD], output standalone -> work/ml_<scheme>;
#   3. edit the generated check_sa.f: read the point from PS.input, one point per run, and take MU_R
#      from MU_R.input (check_sa.f otherwise sets MU_R = sqrt(s) for every point); compile.
#   4. madloop_numeric.py runs the points and compares with the note's Eqs. (17) and (20)
#      -> results/madloop.csv
# Needs generated/Phi3_NLO_*_UFO (generate_Phi3_NLO.sh) and results/scat4_comparison.csv
# (run_scat4_check.sh).
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
PY="$HOME/miniforge3/envs/qft/bin/python"
mkdir -p work results

for scheme in OS MSbar; do
  echo "=== MadLoop, $scheme counterterms"
  ufo="Phi3_NLO_${scheme}_UFO"
  rm -rf "work/$ufo" "work/ml_$scheme"
  cp -r "generated/$ufo" work/
  "$PY" - "work/$ufo" <<'PYEOF'
import pathlib, sys
d = pathlib.Path(sys.argv[1])
for f in ("coupling_orders.py", "couplings.py", "CT_couplings.py"):
    p = d / f
    p.write_text(p.read_text().replace("'PHI'", "'QCD'")
                 .replace("PHI = CouplingOrder(name = 'QCD'", "QCD = CouplingOrder(name = 'QCD'"))
PYEOF
  printf 'import model ./work/%s\ngenerate phi phi > phi phi [virt=QCD]\noutput standalone ./work/ml_%s\n' \
    "$ufo" "$scheme" > "work/ml_$scheme.mg5"
  mg5_aMC "work/ml_$scheme.mg5" > "work/ml_$scheme.log" 2>&1
  grep -E 'Contributing diagrams' "work/ml_$scheme.log"
  P="work/ml_$scheme/SubProcesses/P0_phiphi_phiphi"
  "$PY" - "$P/check_sa.f" <<'PYEOF'
import sys
p = sys.argv[1]
s = open(p).read()
s = s.replace("PARAMETER (READPS = .FALSE.)", "PARAMETER (READPS = .TRUE.)")
s = s.replace("PARAMETER (NPSPOINTS = 4)", "PARAMETER (NPSPOINTS = 1)")
old = "        MU_R=SQRTS\n"
new = (old + "C       research note, step (6): a fixed MU_R can be given in MU_R.input\n"
       "        OPEN(968, FILE='MU_R.input', STATUS='OLD', ERR=9979)\n"
       "        READ(968,*) MU_R\n"
       "        CLOSE(968)\n"
       " 9979   CONTINUE\n")
assert s.count(old) == 1
open(p, "w").write(s.replace(old, new))
PYEOF
  (cd "$P" && make check > make.log 2>&1 && echo "compiled $P/check") || { echo "compilation failed, see $P/make.log"; exit 1; }
done

echo "=== comparison"
"$PY" madloop_numeric.py
