#!/bin/bash
# One-loop q qbar -> Q Qbar and g g -> Q Qbar (research note models/qcd, step (4)); m = 1, s = 10, t = -3, g = 1, general xi.
#   1. FeynArts + FeynCalc: trees (Born in D dims, colour correlations, counterterm pieces), the one-loop interference of
#      each diagram as family integrals ((A) 15, (B) 46 diagrams, (B) in parallel), Feynman gauge by TID, unitarity cut
#      integrands -> work/scat/{A,B}                                                                  (scat_feyncalc.wl)
#   2. FormCalc (own kernel), Feynman gauge, CDR via Dimension -> 0 -> work/scat/{A,B}/formcalc.m    (scat_formcalc.wl)
#   3. LiteRed IBP reduction to masters -> work/scat/{A,B}/ibp.m                                       (scat_litered.wl)
#   4. masters (exact A0, B0; LoopTools, Package-X), counterterms and residues, IR poles vs Eq. (irpole), xi independence,
#      diagram-by-diagram comparison IBP / TID / FormCalc at xi = 1, unitarity of (A)
#      -> results/scat_mathematica.csv, scat_perdiagram.csv, scat_unitarity.csv                       (scat_eval.wl)
# Needs Src/generated/ (run run_model_check.sh first).  About an hour on 8 cores (NJOBS = 5 jobs for (B) besides the other stages).
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
NJOBS="${NJOBS:-5}"
mkdir -p work/scat/A work/scat/B work/scat/logs results
rm -f work/scat/A/*.m work/scat/B/*.m work/scat/logs/*.txt

echo "=== FeynCalc: trees, (A), TID, cuts; FormCalc"
( wolframscript -file scat_feyncalc.wl tree > work/scat/logs/tree.txt 2>&1;
  wolframscript -file scat_feyncalc.wl A > work/scat/logs/A.txt 2>&1 ) &
wolframscript -file scat_feyncalc.wl tidA > work/scat/logs/tidA.txt 2>&1 &
wolframscript -file scat_feyncalc.wl cuts > work/scat/logs/cuts.txt 2>&1 &
wolframscript -file scat_formcalc.wl > work/scat/logs/formcalc.txt 2>&1 &
echo "=== FeynCalc: (B), $NJOBS jobs at a time; the slowest diagrams as pieces (diagram, power k of 1 - xi)"
{ for i in 26 28 30 3 7 11 32 27 29 31; do for k in 0 1 2 3; do echo "$i $i $k"; done; done
  for i in 1 2 4 5 6 8 9 10 12 13 14 15 16 17 18 19 20 21 22 23 24 25 33 34 35 36 37 38 39 40 41 42 43 44 45 46; do echo "$i $i"; done; } |
  xargs -P "$NJOBS" -L 1 sh -c 'wolframscript -file scat_feyncalc.wl B "$@" > "work/scat/logs/B_$1_${3:-all}.txt" 2>&1' sh
echo "=== FeynCalc: (B) in Feynman gauge by TID, one diagram per job"
seq 1 46 | xargs -P "$NJOBS" -I{} sh -c 'wolframscript -file scat_feyncalc.wl tidB {} {} > work/scat/logs/tidB_{}.txt 2>&1'
wait
grep -hE '^\((a|b|c|d|e)\)' work/scat/logs/tree.txt work/scat/logs/A.txt work/scat/logs/tidA.txt work/scat/logs/cuts.txt work/scat/logs/formcalc.txt
grep -hE '^\(c\)' work/scat/logs/B_*.txt | sort -t' ' -k4 -n
grep -hE '^\(d\)' work/scat/logs/tidB_*.txt | sort -t' ' -k9 -n
ls work/scat/B/d*.m work/scat/B/part_*.m 2>/dev/null | wc -l | xargs echo "(B) diagram and piece files:"

echo "=== LiteRed"
wolframscript -file scat_litered.wl 2>&1 | grep -E '^\((a|b)\)'

echo "=== evaluation"
wolframscript -file scat_eval.wl 2>&1 | grep -E '^\((a|b|c|d|e)\)'
