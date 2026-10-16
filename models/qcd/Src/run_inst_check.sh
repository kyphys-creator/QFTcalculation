#!/bin/bash
# Research note models/qcd, step (10): instantons.
#   1. inst_bpst.wl: BPST, zero modes, fermion zero mode, radial reduction, massless partial waves and sums, heat-kernel and lattice coefficients
#   2. inst_gy.py (+ inst_gylib.py): Gel'fand-Yaglom determinants, alpha(1/2), alpha(1), quark-mass dependence
#   3. inst_lattice.py: BPST on a lattice (Wilson action, clover charge)
#   4. inst_density.py: MS-bar instanton density, SU(3) size distribution and topological susceptibility
#   5. inst_scheme.wl: Pauli-Villars versus MS-bar (background-field two-point functions of the regulator loops)
#   6. inst_plot.py: figs/inst.pdf
# About 15 minutes (inst_gy.py on 7 processes).
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
PY="$HOME/miniforge3/envs/qft/bin/python"
mkdir -p work results
set -e
echo "=== symbolic"
wolframscript -file inst_bpst.wl | cut -c1-160
echo "=== Gel'fand-Yaglom"
"$PY" inst_gy.py 2>&1 | grep -v Warning
echo "=== lattice"
"$PY" inst_lattice.py
echo "=== density"
"$PY" inst_density.py
echo "=== PV versus MS-bar"
wolframscript -file inst_scheme.wl | cut -c1-200
"$PY" inst_plot.py
