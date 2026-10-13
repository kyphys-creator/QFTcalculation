#!/bin/bash
# One-loop psi psibar -> psi psibar and the completed one-loop partial-wave bound (research note models/yukawa_ps, step (12)).
#   1. COLLIER: the loop integrals of the hand formula (self-energy, vertex and box tensor integrals)        (scatC_collier.f90)
#   2. FeynArts + FeynCalc: the 12 one-loop diagrams, class by class projected on four spinor structures (spin-summed traces),
#      LoopTools values, the tree spin sum, the UV poles -> results/scatC_feyncalc.csv                     (scatC_feyncalc.wl)
#   3. MadLoop: psi psi~ > psi psi~ [virt] with the NLO UFOs of step (5) (OS and MS-bar counterterms; coupling order
#      YUK renamed to QCD as in run_madloop_check.sh) -> work/ml_<OS|MSbar>_C
#   4. helicity amplitudes from the hand formula, the checks (compact form factor, mu-dependence, FeynCalc projections,
#      MadLoop, partial-wave unitarity for J = 0 and 1), the full J = 0 one-loop matrix and the bound (C)
#      -> results/scatC.csv, ../figs/scatC_d4.pdf                                                         (scatC_numeric.py)
# Needs generated/PsYukawa_FA (generate_PsYukawa.wl) and generated/PsYukawa_NLO_*_UFO (generate_PsYukawa_NLO.sh);
# step 4 also needs work/pw_collier (run_pw_check.sh).  Set SKIP_FC=1 or SKIP_ML=1 to reuse the outputs of steps 2, 3.
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
PY="$HOME/miniforge3/envs/qft/bin/python"
mkdir -p work results

echo "=== COLLIER"
gfortran -I"$HOME/hep/include" scatC_collier.f90 -L"$HOME/hep/lib" -lcollier -o work/scatC_collier && echo "built work/scatC_collier"
gfortran -I"$HOME/hep/include" pw_collier.f90 -L"$HOME/hep/lib" -lcollier -o work/pw_collier && echo "built work/pw_collier"

if [ -z "$SKIP_FC" ]; then
  echo "=== FeynCalc (about 1 min)"
  wolframscript -file scatC_feyncalc.wl
fi

if [ -z "$SKIP_ML" ]; then
  for scheme in OS MSbar; do
    ufo="PsYukawa_NLO_${scheme}_UFO"
    rm -rf "work/$ufo"
    cp -r "generated/$ufo" work/
    "$PY" - "work/$ufo" <<'PYEOF'
import pathlib, sys
d = pathlib.Path(sys.argv[1])
for f in ("coupling_orders.py", "couplings.py", "CT_couplings.py"):
    p = d / f
    p.write_text(p.read_text().replace("'YUK'", "'QCD'")
                 .replace("YUK = CouplingOrder(name = 'QCD'", "QCD = CouplingOrder(name = 'QCD'"))
PYEOF
    out="work/ml_${scheme}_C"
    echo "=== MadLoop, $scheme counterterms, psi psi~ > psi psi~"
    rm -rf "$out"
    printf 'import model ./work/%s\ngenerate psi psi~ > psi psi~ [virt=QCD]\noutput standalone ./%s\n' "$ufo" "$out" > "$out.mg5"
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
new = (old + "C       research note models/yukawa_ps, step (12): a fixed MU_R can be given in MU_R.input\n"
       "        OPEN(968, FILE='MU_R.input', STATUS='OLD', ERR=9979)\n"
       "        READ(968,*) MU_R\n"
       "        CLOSE(968)\n"
       " 9979   CONTINUE\n")
assert s.count(old) == 1
open(p, "w").write(s.replace(old, new))
PYEOF
    (cd "$P" && make check > make.log 2>&1 && echo "compiled $P/check") || { echo "compilation failed, see $P/make.log"; exit 1; }
  done
fi

echo "=== helicity amplitudes, checks, partial waves and the bound (C)"
"$PY" scatC_numeric.py
