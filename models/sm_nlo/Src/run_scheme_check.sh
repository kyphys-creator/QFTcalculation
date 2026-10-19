#!/bin/bash
# Step (7) of the NLO note: the MS-bar results against the on-shell G_mu scheme at one loop.
#   1. scheme.wl          : dW - DeltaHat, dZ - DeltaHat, dW - dZ (the SM note's self-energies with the tadpoles and its muon
#                           decay) at the tree point of the SM note's fit, in three gauges and at the mu of steps (4a)-(4c)  (~30 s)
#   2. scheme_compare.py  : Z -> nu nubar, Z -> e+ e- (weak), W -> e nu, t -> b W in both: the mu dependence of the G_mu results and
#                           the MS-bar minus G_mu difference, split into its O(alpha^2) parts
# Needs steps (1)-(4c) first (results/lo_widths.csv, zweak.csv, wreal.csv, treal.csv) and the SM note's results
# (models/sm/Src/results/oneloop_sigma.m, mudecay_deltahat_finite.m).
cd "$(dirname "$0")"
mkdir -p work results
for f in results/lo_widths.csv results/zweak.csv results/wreal.csv results/treal.csv ../../sm/Src/results/oneloop_sigma.m \
  ../../sm/Src/results/mudecay_deltahat_finite.m; do
  [ -e "$f" ] || { echo "$f missing: run the checks of steps (1)-(4c) and the SM note first"; exit 1; }
done
wolframscript -file scheme.wl > work/scheme.log 2>&1 || { echo "scheme.wl failed"; exit 1; }
grep -E "^\((a|b)\)|^DeltaHat|^tree point" work/scheme.log | sed -E 's/NumberForm\[([^,]+), [0-9]+\]/\1/g; s/`[0-9.]+//g' | \
  sed -E 's/([0-9]\.[0-9]{10})[0-9]+/\1/g' | cut -c1-250
python3 scheme_compare.py
