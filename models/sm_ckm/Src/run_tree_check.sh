#!/bin/bash
# Step (2) of the CKM note: tree-level squared amplitudes, widths and cross sections with the CKM matrix.
#   1. tree_ckm_feyncalc.wl   : sum|M|^2 of W+ -> u_i dbar_j, t -> d_j W+, tbar -> bbar W-, u_i dbar_j -> nu e+,
#                               u ubar -> d sbar against the note (symbolic in V), u ubar -> W+ W- reduced to V = 1 by
#                               unitarity, t sbar -> W+ H independent of xiW; benchmark points -> results/tree_ckm_points.csv
#   2. tree_ckm_numeric.py    : explicit matrices (t sbar -> W+ H in unitary gauge) vs FeynCalc, widths, unitarity
#                               sums, cross sections -> results/tree_ckm_numeric.csv
#   3. tree_ckm_mg5.mg5       : MadGraph widths (compute_widths) and cross sections, u u~ > w+ w- also with the SM
#                               note's UFO (V = 1)
#   4. compare_tree_ckm_mg5.py: MadGraph vs tree_ckm_numeric.py -> results/tree_ckm_mg5_comparison.csv
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
mkdir -p work
wolframscript -file tree_ckm_feyncalc.wl > work/tree_ckm_feyncalc.out 2>&1
grep -E "note =|expect|compared|written" work/tree_ckm_feyncalc.out
python3 tree_ckm_numeric.py
rm -rf work/SM_CKM_UFO work/SM_UFO work/mg5_udenu work/mg5_usenu work/mg5_uuds work/mg5_uuww work/mg5_uuww_v1
cp -R generated/SM_CKM_UFO work/ && cp -R ../../sm/Src/generated/SM_UFO work/
"$HOME/hep/bin/mg5_aMC" tree_ckm_mg5.mg5 > work/tree_ckm_mg5.log 2>&1
if grep -q -E "No model currently active|not allowed for your current model|NoDiagramException" work/tree_ckm_mg5.log; then
  echo "ERROR: MadGraph did not use the note's UFOs or found no diagrams (see work/tree_ckm_mg5.log)"; exit 1
fi
python3 compare_tree_ckm_mg5.py
