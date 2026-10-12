#!/bin/bash
# Tree-level check (research note models/yukawa_ps, step (2)).
#   1. FeynArts + FeynCalc amplitudes and spin sums vs Eq. (11) (eq:Mtree) and eq:MtreeD, symbolically  (tree_feyncalc.wl)
#   2. MadGraph cross sections of (A)-(D) at sqrt(s) = 2.5, 5, 10                                  (tree_mg5.mg5)
#   3. explicit-spinor spin sums, numerical integration of Eq. (12) (eq:sigma), comparison          (tree_sigma.py)
# Needs Src/generated/ (run generate_PsYukawa.wl first).  MadGraph output goes to Src/work/.
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
mkdir -p work

echo "=== FeynCalc"
wolframscript -file tree_feyncalc.wl 2>&1 | grep -E '^\((A|B|C|D)\)'

echo "=== MadGraph"
rm -rf work/mg5_treeA work/mg5_treeB work/mg5_treeC work/mg5_treeD work/PsYukawa_UFO
cp -R generated/PsYukawa_UFO work/PsYukawa_UFO   # MadGraph rewrites the UFO it imports
mg5_aMC tree_mg5.mg5 > work/tree_mg5.log 2>&1
rm -f py.py MG5_debug
grep -E '^\s+Cross-section' work/tree_mg5.log

echo "=== comparison"
"$HOME/miniforge3/envs/qft/bin/python" tree_sigma.py work/tree_mg5.log
