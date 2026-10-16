#!/bin/bash
# Step (2) of the SM note: tree-level squared amplitudes, widths and cross sections.
#   1. tree_feyncalc.wl   : sum|M|^2 of W, Z, H, t decays and e+ e- -> mu+ mu- against the note (symbolic),
#                           xi independence, e+ e- -> W+ W- at 9 points -> results/tree_eeww_points.csv
#   2. tree_numeric.py    : explicit matrices: e+ e- -> W+ W- vs FeynCalc, the longitudinal cancellation,
#                           Eq. (widths) and the cross sections -> results/tree_numeric.csv
#   3. tree_mg5.mg5       : MadGraph widths (compute_widths) and cross sections
#   4. compare_tree_mg5.py: MadGraph vs tree_numeric.py -> results/tree_mg5_comparison.csv
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
wolframscript -file tree_feyncalc.wl 2>&1 | grep -E "note =|expect|compared|amplitudes:"
python3 tree_numeric.py
mkdir -p work && rm -rf work/SM_UFO work/mg5_eemm work/mg5_eeww && cp -R generated/SM_UFO work/
"$HOME/hep/bin/mg5_aMC" tree_mg5.mg5 > work/tree_mg5.log 2>&1
if grep -q -E "No model currently active|not allowed for your current model" work/tree_mg5.log; then
  echo "ERROR: MadGraph did not use SM_UFO (see work/tree_mg5.log)"; exit 1
fi
python3 compare_tree_mg5.py
