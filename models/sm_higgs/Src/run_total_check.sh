#!/bin/bash
# Step (8) of the Higgs note: the total width and the branching ratios (after run_loopind_check.sh, run_hff_weak_check.sh,
# run_hgg_check.sh and run_hvv_check.sh: it reads their results/*.csv).
#   total_width.py : the partial widths at mu = M_H, M_H/2, 2 M_H, the scheme shifts, Gamma_H and the BR with their mu and scheme
#                    dependence; the YR4 values and the PDG Gamma_H for reference                                         (~1 s)
cd "$(dirname "$0")"
for f in hff_widths hgg_widths loopind_widths hvv_widths hvv_scheme; do
  [ -e results/$f.csv ] || { echo "results/$f.csv is missing: run the runners of steps (2)-(7) first"; exit 1; }
done
python3 total_width.py
