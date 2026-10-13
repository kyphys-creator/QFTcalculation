#!/bin/bash
# MadLoop check of the one-loop e+ e- -> mu+ mu- interference (research note models/spinor_qed, step (5)).
# For each NLO UFO in generated/ (MS: on-shell fields and masses, MS-bar charge; a0: charge alpha(0)), both with
# NLOCT's R2 vertices:
#   1. copy it to work/;
#   2. mg5_aMC: generate e- e+ > mu- mu+ [virt=QED], output standalone -> work/ml_<scheme>;
#   3. edit the generated check_sa.f: read the point from PS.input, one point per run, and take MU_R from MU_R.input
#      (check_sa.f otherwise sets MU_R = sqrt(s) for every point); compile;
#   4. madloop_numeric.py runs the points and compares with the note (Eqs. (16)-(18)) -> results/madloop.csv
# Needs generated/SpinorQED_NLO_*_UFO (generate_SpinorQED_NLO.sh) and results/scat_collier.csv (run_scat_check.sh).
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
PY="$HOME/miniforge3/envs/qft/bin/python"
mkdir -p work results

for scheme in MS a0; do
  ufo="SpinorQED_NLO_${scheme}_UFO"
  rm -rf "work/$ufo"
  cp -r "generated/$ufo" work/
  out="work/ml_${scheme}"
  echo "=== MadLoop, $scheme counterterms, e- e+ > mu- mu+"
  rm -rf "$out"
  printf 'import model ./work/%s\ngenerate e- e+ > mu- mu+ [virt=QED]\noutput standalone ./%s\n' "$ufo" "$out" > "$out.mg5"
  mg5_aMC "$out.mg5" > "$out.log" 2>&1
  grep -E 'Contributing diagrams' "$out.log"
  P=$(ls -d "$out"/SubProcesses/P0_* | head -1)
  "$PY" - "$P/check_sa.f" <<'PYEOF'
import sys
p = sys.argv[1]
s = open(p).read()
s = s.replace("PARAMETER (READPS = .FALSE.)", "PARAMETER (READPS = .TRUE.)")
s = s.replace("PARAMETER (NPSPOINTS = 4)", "PARAMETER (NPSPOINTS = 1)")
old = "        MU_R=SQRTS\n"
new = (old + "C       research note models/spinor_qed, step (5): a fixed MU_R can be given in MU_R.input\n"
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
