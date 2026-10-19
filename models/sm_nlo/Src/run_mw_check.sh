#!/bin/bash
# Step (6) of the NLO note: Delta rho from the self-energies and the prediction of M_W.
#   1. mw.wl          : the tadpoles in Sigma^WW/M_W^2 - Sigma^ZZ/M_Z^2, Delta rho of the top-bottom doublet against the formula,
#                       the whole Delta rho (UV pole, gauge dependence), M_W from the couplings of the SM note's alpha scheme in
#                       three gauges and at four mu                                                                      (~2 min)
#   2. mw_summary.py  : the Breit-Wigner mass with Gamma_W of step (4b), the truncation, the SM note's value, the O(alpha alpha_s)
#                       estimate, and the measured M_W (references)
# Needs step (4b) first (run_wweak_check.sh: results/wweak_widths.csv) and the SM note's self-energies and fit
# (models/sm/Src/results/oneloop_sigma.m, msbar_fit.csv).
cd "$(dirname "$0")"
mkdir -p work results
for f in results/wweak_widths.csv ../../sm/Src/results/oneloop_sigma.m ../../sm/Src/results/msbar_fit.csv; do
  [ -e "$f" ] || { echo "$f missing: run the checks of step (4b) and the SM note first"; exit 1; }
done
wolframscript -file mw.wl > work/mw.log 2>&1 || { echo "mw.wl failed"; exit 1; }
grep -E "^\((a|b|c)\)|whole Delta rho|gauge parameters" work/mw.log | sed -E 's/NumberForm\[([^,]+), [0-9]+\]/\1/g; s/ScientificForm\[([^,]+), [0-9]\]/\1/g; s/`[0-9.]+//g' | \
  sed -E 's/([0-9]\.[0-9]{10})[0-9]+/\1/g' | cut -c1-250
python3 mw_summary.py
