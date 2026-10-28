#!/bin/bash
# Step (9) of the abelian Higgs note: perturbative unitarity of A_L A_L, h h, A_L h.
#   1. unitarity_feyncalc.wl : A h -> A h in a general R_xi gauge against Eq. (Mah); the four longitudinal amplitudes with
#                              explicit polarization vectors against the hand formulas; high-energy limits
#                              -> results/unitarity_amps.m, results/unitarity_points.csv, work/me_points_*_L.txt
#   2. unitarity_mg5.mg5     : MadGraph standalone matrix elements with zp{0} (unitary and Feynman gauge), evaluated with
#                              tree_me_points.f; compare_unitarity_mg5.py -> results/unitarity_mg5_comparison.csv
#   3. unitarity_numeric.wl  : tree s waves, eigenvalues, the largest MH/MA -> results/unitarity_{tree,bound,curves}.csv
#   4. unitarity_oneloop.py  : one-loop s waves of the scalar sector at high energy -> results/unitarity_oneloop.csv
#   5. unitarity_plot.py     : ../figs/unitarity.pdf
# Needs Src/generated/ (generate_AbelianHiggs.wl).  MadGraph output goes to Src/work/.
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
PY="$HOME/miniforge3/envs/qft/bin/python"
mkdir -p work results ../figs

echo "=== FeynCalc"
wolframscript -file unitarity_feyncalc.wl 2>&1 | grep -E '^\('

echo "=== MadGraph"
rm -rf work/AbelianHiggs_UFO work/sa_LL_u work/sa_LL_f work/sa_LLhh_u work/sa_LLhh_f work/sa_hh_u work/sa_Lh_u work/sa_Lh_f
cp -R generated/AbelianHiggs_UFO work/AbelianHiggs_UFO   # MadGraph rewrites the UFO it imports
mg5_aMC unitarity_mg5.mg5 > work/unitarity_mg5.log 2>&1
rm -f py.py MG5_debug nsqso_born.inc ../nsqso_born.inc
if grep -q -E "No model currently active|not allowed for your current model|with error" work/unitarity_mg5.log; then
  echo "ERROR: MadGraph failed (see work/unitarity_mg5.log)"; exit 1
fi
for d in LL_u LL_f LLhh_u LLhh_f hh_u Lh_u Lh_f; do
  proc=${d%_*}; g=${d##*_}
  sed -i '' -E 's/^DECAY +25 +[0-9.eE+-]+/DECAY  25 0.000000e+00/' work/sa_$d/Cards/param_card.dat
  p=$(ls -d work/sa_$d/SubProcesses/P1_*)
  ( cd "$p" && make check > /dev/null 2>&1 && \
    gfortran -O2 -ffixed-line-length-132 -o me_points ../../../../tree_me_points.f matrix.o \
      ../../lib/libdhelas.a ../../lib/libmodel.a -I. && \
    ./me_points < ../../../me_points_${proc}_L.txt > ../../../me_out_${proc}_L_$g.txt )
done
"$PY" compare_unitarity_mg5.py

echo "=== partial waves"
wolframscript -file unitarity_numeric.wl 2>&1 | grep -E '^\('
"$PY" unitarity_oneloop.py
"$PY" unitarity_plot.py 2>&1 | grep -v Warning
