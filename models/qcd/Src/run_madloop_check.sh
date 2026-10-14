#!/bin/bash
# MadLoop check of the one-loop u ubar -> t tbar and g g -> t tbar interferences (research note models/qcd, step (5)).
#   0. generate_QCD_NLO.sh (NLOCT counterterms and R2 vertices -> generated/QCD_NLO_UFO), unless NO_UFO=1;
#   1. copy the UFO to work/;
#   2. mg5_aMC: generate u u~ > t t~ [virt=QCD] and g g > t t~ [virt=QCD], output standalone -> work/ml_A, work/ml_B;
#   3. edit the generated check_sa.f: read the point from PS.input, one point per run, and MU_R from MU_R.input
#      (check_sa.f otherwise sets MU_R = sqrt(s)); compile;
#   4. madloop_numeric.py runs the points and compares with step (4) -> results/madloop.csv
# Needs Src/generated/QCD_ren (nlo_renormalize.wl) inputs and results/scat_*.csv + work/scat (run_scat_check.sh).
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
PY="$HOME/miniforge3/envs/qft/bin/python"
mkdir -p work results

if [ "${NO_UFO:-0}" != 1 ]; then ./generate_QCD_NLO.sh; fi

ufo=QCD_NLO_UFO
rm -rf "work/$ufo"
cp -r "generated/$ufo" work/
for proc in A B; do
  out="work/ml_${proc}"
  case $proc in A) gen="u u~ > t t~ [virt=QCD]";; B) gen="g g > t t~ [virt=QCD]";; esac
  echo "=== MadLoop, $gen"
  rm -rf "$out"
  printf 'import model ./work/%s\ngenerate %s\noutput standalone ./%s\n' "$ufo" "$gen" "$out" > "$out.mg5"
  mg5_aMC "$out.mg5" > "$out.log" 2>&1
  grep -E 'Contributing diagrams|loop diagrams|Generated|Error|error' "$out.log" | head -5
  P=$(ls -d "$out"/SubProcesses/P0_* | head -1)
  "$PY" - "$P/check_sa.f" <<'PYEOF'
import sys
p = sys.argv[1]
s = open(p).read()
s = s.replace("PARAMETER (READPS = .FALSE.)", "PARAMETER (READPS = .TRUE.)")
s = s.replace("PARAMETER (NPSPOINTS = 4)", "PARAMETER (NPSPOINTS = 1)")
old = "        MU_R=SQRTS\n"
new = (old + "C       research note models/qcd, step (5): a fixed MU_R can be given in MU_R.input\n"
       "        OPEN(968, FILE='MU_R.input', STATUS='OLD', ERR=9979)\n"
       "        READ(968,*) MU_R\n"
       "        CLOSE(968)\n"
       " 9979   CONTINUE\n")
assert s.count(old) == 1
open(p, "w").write(s.replace(old, new))
PYEOF
  # the param_card has aS with 7 digits (7.957747e-02): write the full 1/(4 pi) as a plain decimal (MadLoop misreads a longer
  # mantissa with an exponent), else MadLoop is off by 4e-8 (Born), 6e-8 (virtual)
  sed -i '' -E 's/^( +3 +)7\.957747e-02( +# aS)/\10.07957747154594767\2/' "$out/Cards/param_card.dat"
  grep -E '# aS' "$out/Cards/param_card.dat"
  (cd "$P" && make check > make.log 2>&1 && echo "compiled $P/check") || { echo "compilation failed, see $P/make.log"; exit 1; }
done

echo "=== comparison"
wolframscript -file madloop_predict.wl 2>&1 | grep -E "^\((a|b)\)"
"$PY" madloop_numeric.py
