#!/bin/bash
# Tree-level check of phi phi -> phi phi (research note models/phi34, step (2)).
#   1. FeynArts + FeynCalc amplitude vs Eq. (8) (eq:Mtree), symbolically     (tree_feyncalc.wl)
#   2. MadGraph cross sections at sqrt(s) = 2.5, 5, 10              (tree_mg5.mg5)
#   3. numerical integration of |Eq. (8) (eq:Mtree)|^2 and comparison         (tree_sigma.py)
# Needs Src/generated/ (run generate_Phi34.wl first).  MadGraph output goes to Src/work/.
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
mkdir -p work

echo "=== FeynCalc"
wolframscript -file tree_feyncalc.wl 2>&1 | grep -E '^(number|M \(|M\(|M at)'

echo "=== MadGraph"
rm -rf work/mg5_tree work/Phi34_UFO
cp -R generated/Phi34_UFO work/Phi34_UFO   # MadGraph rewrites the UFO it imports
mg5_aMC tree_mg5.mg5 > work/tree_mg5.log 2>&1
rm -f py.py MG5_debug
grep -E '^\s+Cross-section' work/tree_mg5.log

echo "=== comparison"
"$HOME/miniforge3/envs/qft/bin/python" tree_sigma.py work/tree_mg5.log
