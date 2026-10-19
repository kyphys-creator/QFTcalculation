#!/bin/bash
# Step (8) of the NLO note: the NLO predictions with their uncertainties (mu, scheme, a known higher order) against the measured
# values.  summary.py reads the results of steps (4a)-(7) and recomputes the Z, W and top widths in the on-shell G_mu scheme
# (results/scheme.csv of step (7)); it writes results/summary.csv (~10 s).
# Needs steps (1)-(7) first (run_zweak_check.sh, run_wweak_check.sh, run_tweak_check.sh, run_zpole_check.sh, run_mw_check.sh,
# run_scheme_check.sh).
cd "$(dirname "$0")"
for f in results/zweak_widths.csv results/zpole.csv results/wweak_widths.csv results/tweak_widths.csv results/mw_summary.csv \
  results/scheme.csv results/treal.csv results/ir_massive.csv; do
  [ -e "$f" ] || { echo "$f missing: run the checks of steps (1)-(7) first"; exit 1; }
done
python3 summary.py
