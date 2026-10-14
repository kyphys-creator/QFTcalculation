#!/bin/bash
# Renormalization group of QCD (research note models/qcd, step (6)).
#   1. FeynArts + FeynCalc: the two-point functions (as in step (3)) and their symbolic mu-dependence with Package-X (incl. the
#      residue through the exact A0 relations and the decoupling expansion); the 1PI brackets at mu = 1/2, 1, 2 with Package-X and
#      LoopTools; K W of u ubar -> t tbar and g g -> t tbar (TID amplitudes of step (4)) at mu = 1/2, 1, 2 with LoopTools
#      -> results/rg_feyncalc_onepi.csv, results/rg_feyncalc.csv                                          (rg_feyncalc.wl)
#   2. COLLIER: the same 1PI brackets (built here, run by rg_numeric.py) -> results/rg_collier_onepi.csv  (rg_collier.f90)
#   3. MadLoop u u~ > d d~ [virt=QCD] with the step-(5) UFO (work/ml_C) and the same without the top (/ t, work/ml_C5); check_sa.f
#      reads PS.input and MU_R.input as in run_madloop_check.sh
#   4. MadGraph's ALPHAS(Q) (Template/LO/Source/alfas_functions.f) with a small driver -> work/alfas_mg5     (alfas_mg5.f)
#   5. slopes, gamma's, beta_0 (1PI, LoopTools, MadLoop), decoupling, figure -> results/rg_comparison.csv,
#      results/rg_decoupling.csv, ../figs/rg_running.pdf                                                   (rg_numeric.py)
#   6. the one-loop RG flow of alpha_s, m, xi; physical alpha_s and Lambda -> ../figs/rgflow.pdf             (rgflow.py)
# Needs run_scat_check.sh (work/scat) and run_madloop_check.sh (generated/QCD_NLO_UFO, results/madloop.csv).  wolframscript may print
# "libc++abi: ... MathLink::MLException" when LoopTools is unloaded at the end; the results are written before that.
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
PY="$HOME/miniforge3/envs/qft/bin/python"
MG5SRC="$HOME/hep/MG5_aMC_v3_8_1/Template/LO/Source"
mkdir -p work results

echo "=== FeynCalc / Package-X / LoopTools"
wolframscript -file rg_feyncalc.wl 2>&1 | grep -E '^\((a|b|c|d)\)' | cut -c1-400

echo "=== COLLIER"
gfortran -I"$HOME/hep/include" rg_collier.f90 -L"$HOME/hep/lib" -lcollier -o work/rg_collier && echo "built work/rg_collier"

echo "=== MadLoop u u~ > d d~"
rm -rf work/QCD_NLO_UFO
cp -r generated/QCD_NLO_UFO work/
for proc in C C5; do
  out="work/ml_${proc}"
  case $proc in C) gen="u u~ > d d~ [virt=QCD]";; C5) gen="u u~ > d d~ [virt=QCD] / t";; esac
  rm -rf "$out"
  printf 'import model ./work/QCD_NLO_UFO\ngenerate %s\noutput standalone ./%s\n' "$gen" "$out" > "$out.mg5"
  mg5_aMC "$out.mg5" > "$out.log" 2>&1
  echo "$gen: $(grep -E 'Contributing diagrams' "$out.log" | sed 's/.*generated: //')"
  P=$(ls -d "$out"/SubProcesses/P0_* | head -1)
  "$PY" - "$P/check_sa.f" <<'PYEOF'
import sys
p = sys.argv[1]
s = open(p).read()
s = s.replace("PARAMETER (READPS = .FALSE.)", "PARAMETER (READPS = .TRUE.)")
s = s.replace("PARAMETER (NPSPOINTS = 4)", "PARAMETER (NPSPOINTS = 1)")
old = "        MU_R=SQRTS\n"
new = (old + "C       research note models/qcd, step (6): a fixed MU_R can be given in MU_R.input\n"
       "        OPEN(968, FILE='MU_R.input', STATUS='OLD', ERR=9979)\n"
       "        READ(968,*) MU_R\n"
       "        CLOSE(968)\n"
       " 9979   CONTINUE\n")
assert s.count(old) == 1
open(p, "w").write(s.replace(old, new))
PYEOF
  # aS with all digits as a plain decimal (MG5 writes 7 digits; MadLoop misreads a long mantissa with an exponent), see step (5)
  sed -i '' -E 's/^( +3 +)7\.957747e-02( +# aS)/\10.07957747154594767\2/' "$out/Cards/param_card.dat"
  (cd "$P" && make check > make.log 2>&1 && echo "compiled $P/check") || { echo "compilation failed, see $P/make.log"; exit 1; }
done

echo "=== MadGraph ALPHAS"
gfortran -ffixed-line-length-132 -I"$MG5SRC" alfas_mg5.f "$MG5SRC/alfas_functions.f" -o work/alfas_mg5 && echo "built work/alfas_mg5"

echo "=== slopes, beta_0, decoupling, figure"
"$PY" rg_numeric.py

echo "=== RG flow"
"$PY" rgflow.py
