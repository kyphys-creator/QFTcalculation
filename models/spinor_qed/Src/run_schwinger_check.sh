#!/bin/bash
# Schwinger pair production (research note models/spinor_qed, step (11)).
#   1. the points: field strengths, Dirac modes, instanton parameters, (m^2/eE, gt) grids -> work/schw_points.txt
#                                                                                       (schwinger_numeric.py --points)
#   2. Mathematica: residues of the proper-time integrand (Im L), weak-field coefficients = zeta(2n) Gamma(2n-2)/(4 pi^(2n+2))
#      = dispersion (Borel) integrals (symbolic); proper-time integral above the poles; the Dirac equation in the Sauter
#      potential (NDSolve); worldline instantons (NDSolve); Im Gamma from Nikishov's nbar (NIntegrate)
#      -> results/schwinger_mathematica.csv                                                       (schwinger_exact.wl)
#   3. Python (SciPy, mpmath): the same independently, the semiclassical (worldline instanton + WKB prefactor) and locally
#      constant field comparisons, Kim and Page's double integral, the Gaussian field mode by mode, physical rates, figure
#      -> results/schwinger.csv, ../figs/schwinger.pdf (about 30 min)                           (schwinger_numeric.py)
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
PY="$HOME/miniforge3/envs/qft/bin/python"
mkdir -p work results

echo "=== points"
"$PY" schwinger_numeric.py --points

echo "=== Mathematica"
wolframscript -file schwinger_exact.wl 2>&1 | grep -E '^\((a|b|c|d)\)'

echo "=== Python: constant field, Sauter potential, instantons, Gaussian field, figure (about 30 min)"
"$PY" -u schwinger_numeric.py
