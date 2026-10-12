#!/bin/bash
# Cross-checks with the thermal tools of the loop-tools review (research note models/phi34_thermal, step (8)):
#   1. dralgo_check.wl     : DRalgo 1.5.0 (+ GroupMath 1.1.3), 3D EFT of the single-field model vs Eq. (13);
#                            (d) the shifted basis at NLO (step (10))
#   2. matchotter_check.wl : Matchete 0.6.0 / Matchotter, the same reduction                -> results/matchotter_check.csv
#   3. pt2gw_check.wl      : PT2GWFinder 1.1.0 + FindBounce 1.1.0, the Dine-form transitions -> results/pt2gw_check.csv
# Each script runs in a kernel of its own.  Needs results/{dine_form,strong_pt,gw_spectrum,cosmotransitions_check}.csv.
# About 40 minutes in total.
cd "$(dirname "$0")"
mkdir -p results
wolframscript -file dralgo_check.wl | grep -E "^\((a|b|c|d)\)"
wolframscript -file matchotter_check.wl | grep -E "^\((a|b)\)"
wolframscript -file pt2gw_check.wl | grep -E "^\((a|b|c|d|e|f)\)"
