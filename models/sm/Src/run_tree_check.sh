#!/bin/bash
# Step (2) of the SM note: tree-level amplitudes, widths and cross sections.
#   1. tree_feyncalc.wl: FeynArts + FeynCalc, symbolic: (a) FeynRules model vs SM.mod sign rule on 38 vertex classes,
#                        (b) muon decay, (c) two-body widths, (d) e+e- -> mu+mu-, (e) e+e- -> W+W- (results/tree_feyncalc_ww.csv)
#   2. tree_mg5.mg5    : MadGraph compute_widths, the muon width, e+e- -> mu+mu- and W+W- cross sections (work/tree_mg5.log)
#   3. tree_numeric.py : explicit Dirac matrices and polarization vectors; gauge cancellation; comparison with 1 and 2
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
PY="$HOME/miniforge3/envs/qft/bin/python"
mkdir -p work
wolframscript -file tree_feyncalc.wl > work/tree_feyncalc.log 2>&1
grep -E '^\([a-e]\)' work/tree_feyncalc.log
rm -rf work/SM_UFO work/SM_UFO-massless && cp -R generated/SM_UFO work/
"$PY" make_restrict.py work/SM_UFO
mg5_aMC tree_mg5.mg5 > work/tree_mg5.log 2>&1
"$PY" tree_numeric.py work/tree_mg5.log
