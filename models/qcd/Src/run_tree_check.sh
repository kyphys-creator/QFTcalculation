#!/bin/bash
# Tree-level check (research note models/qcd, step (2)).
#   1. FeynArts + FeynCalc amplitudes and spin/colour sums vs Eqs. (Mtree)-(ghostsum), symbolically for (A), (B), (D), with exact
#      rational kinematics for (C); xi independence, gluon polarization sums and ghost pairs, Ward identity  (tree_feyncalc.wl)
#   2. MadGraph cross sections of (A), (B) at sqrt(s) = 3, 5, 10 and (C), (D) with cuts at 5, 10, 20   (tree_mg5.mg5)
#   3. explicit spinors, Gell-Mann matrices and polarization vectors; Eq. (sigtree) and comparison      (tree_sigma.py)
# Needs Src/generated/ (run generate_QCD.wl first).  MadGraph output goes to Src/work/.
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
mkdir -p work

echo "=== FeynCalc"
wolframscript -file tree_feyncalc.wl 2>&1 | grep -E '^\((A|B|C|D)\)'

echo "=== MadGraph"
rm -rf work/mg5_tree[ABCD] work/QCD_UFO
cp -R generated/QCD_UFO work/QCD_UFO   # MadGraph rewrites the UFO it imports
mg5_aMC tree_mg5.mg5 > work/tree_mg5.log 2>&1
rm -f py.py MG5_debug
grep -E '^\s+Cross-section' work/tree_mg5.log

echo "=== explicit matrices, Eq. (sigtree), comparison"
"$HOME/miniforge3/envs/qft/bin/python" tree_sigma.py work/tree_mg5.log
