#!/bin/bash
# Step (2) of the abelian Higgs note: tree amplitudes, width and cross sections.
#   1. tree_feyncalc.wl    : FeynArts + FeynCalc in a general R_xi gauge: h -> A A, A A -> A A, A A -> h h (xi
#                            independence), h h -> h h, G G -> G G, G G -> h h against the note (symbolic); exact
#                            polarization sums at 10 points -> results/tree_feyncalc_points.csv
#   2. tree_numeric.py     : explicit polarization vectors: helicity sums vs FeynCalc, the R_xi diagrams of A A -> h h,
#                            equivalence theorem, width and cross sections, MadGraph points -> results/tree_numeric.csv
#   3. tree_mg5.mg5        : MadGraph width (compute_widths), standalone matrix elements (unitary and Feynman gauge),
#                            cross sections at sqrt(s) = 6, 20
#   4. tree_me_points.f    : evaluates the standalone matrix elements at the points of step 2 (h width set to 0)
#   5. compare_tree_mg5.py : MadGraph vs steps 1-2 -> results/tree_mg5_comparison.csv
# Needs Src/generated/ (run generate_AbelianHiggs.wl first).  MadGraph output goes to Src/work/ (about 1.5 minutes).
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
PY="$HOME/miniforge3/envs/qft/bin/python"
mkdir -p work

echo "=== FeynCalc"
wolframscript -file tree_feyncalc.wl 2>&1 | grep -E '^\((a|b|c|d|e)\)'

echo "=== explicit polarization vectors"
"$PY" tree_numeric.py

echo "=== MadGraph"
rm -rf work/AbelianHiggs_UFO work/sa_aaaa_u work/sa_aaaa_f work/sa_aahh_u work/sa_aahh_f work/sa_hhhh_u \
  work/mg5_aaaa work/mg5_aahh work/mg5_hhhh work/tree_widths.dat
cp -R generated/AbelianHiggs_UFO work/AbelianHiggs_UFO   # MadGraph rewrites the UFO it imports
mg5_aMC tree_mg5.mg5 > work/tree_mg5.log 2>&1
rm -f py.py MG5_debug nsqso_born.inc ../nsqso_born.inc   # output standalone writes nsqso_born.inc here and in ..
if grep -q -E "No model currently active|not allowed for your current model|with error" work/tree_mg5.log; then
  echo "ERROR: MadGraph failed (see work/tree_mg5.log)"; exit 1
fi
grep -E '^\s+Cross-section' work/tree_mg5.log
for pair in aaaa_u:AAAA aaaa_f:AAAA aahh_u:AAhh aahh_f:AAhh hhhh_u:hhhh; do
  d=${pair%%:*}; proc=${pair##*:}; g=${d##*_}
  sed -i '' -E 's/^DECAY +25 +[0-9.eE+-]+/DECAY  25 0.000000e+00/' work/sa_$d/Cards/param_card.dat
  p=$(ls -d work/sa_$d/SubProcesses/P1_*)
  ( cd "$p" && make check > /dev/null 2>&1 && \
    gfortran -O2 -ffixed-line-length-132 -o me_points ../../../../tree_me_points.f matrix.o \
      ../../lib/libdhelas.a ../../lib/libmodel.a -I. && \
    ./me_points < ../../../me_points_$proc.txt > ../../../me_out_${proc}_$g.txt )
done

echo "=== comparison"
"$PY" compare_tree_mg5.py
