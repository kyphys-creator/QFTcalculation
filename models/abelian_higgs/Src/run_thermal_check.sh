#!/bin/bash
# Step (10) of the abelian Higgs note: the finite-temperature phase transition.
#   1. thermal.wl        : high-T series against the exact J_B, thermal masses, the general form (D, E, lam_T, T0) and the
#                          screened longitudinal mode; T_c and phi_c/T_c (general form, high-T one loop, daisy, exact J_B);
#                          background R_xi and Fermi gauges with the same resummation, e = 1/2 ... 1/32
#                          -> results/thermal.csv, thermal_gauge.csv, thermal_curves.csv, thermal_jb.csv
#   2. thermal_ct.py     : CosmoTransitions (J_B spline, phase tracing, critical temperature) -> results/thermal_ct.csv
#   3. thermal_dralgo.wl : DRalgo: 3D parameters, 4D beta functions, the 4D potential rebuilt from the 3D EFT, the
#                          ultrasoft EFT -> results/thermal_dralgo.csv
#   4. thermal_plot.py   : ../figs/thermal.pdf
cd "$(dirname "$0")"
PY="$HOME/miniforge3/envs/qft/bin/python"
mkdir -p results ../figs
wolframscript -file thermal.wl 2>&1 | grep -E "^\("
"$PY" thermal_ct.py
wolframscript -file thermal_dralgo.wl 2>&1 | grep -E "^\("
"$PY" thermal_plot.py 2>&1 | grep -v Warning
