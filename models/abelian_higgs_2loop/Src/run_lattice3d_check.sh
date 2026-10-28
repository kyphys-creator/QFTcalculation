#!/bin/bash
# Step (7) of the two-loop note: the 3D U(1)+Higgs theory against the lattice (Kajantie et al., hep-lat/9711048).
#   lattice3d.wl      : the strict expansion in closed form (y_c, Delta l3), the Landau one- and two-loop potentials,
#                       x = 0.0463 and a scan in x, the benchmarks of step (6) on the x axis (reads results/thermal_nlo.csv)
#                       -> results/lattice3d.csv, results/lattice3d_bench.csv
#   lattice3d_plot.py : figs/lattice3d.pdf
cd "$(dirname "$0")"
mkdir -p results
wolframscript -file lattice3d.wl 2>&1 | grep -E "^\(|written"
"$HOME/miniforge3/envs/qft/bin/python" lattice3d_plot.py
