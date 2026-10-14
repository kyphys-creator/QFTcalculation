#!/bin/bash
# The running coupling (research note models/spinor_qed, step (9)).
#   1. the q^2 values: check points and the nodes of the spectral integrals -> work/running_q2.txt  (running_numeric.py --nodes)
#   2. FeynArts + FeynCalc: the photon two-point function of one flavour; Package-X expansions for small q^2 and large -q^2
#      (symbolic mass); K Pibar/e^2 at the q^2 values from Package-X (30 digits) and LoopTools -> results/running_feyncalc.csv
#                                                                                                 (running_feyncalc.wl)
#   3. COLLIER: the same values (built here, run by running_numeric.py)                          (running_collier.f90)
#   4. dispersion relation (real part by the principal-value integral, imaginary part = -pi rho), effective charge against the
#      MS-bar charge at e^(-5/6) Q, decoupling, MS-bar and on-shell Landau poles, Uehling potential (three representations and
#      the spectral integral with the tools' rho), muonic-hydrogen 2P-2S and hydrogen 2S shifts; figure
#      -> results/running.csv, ../figs/running.pdf                                                (running_numeric.py)
# Needs Src/generated/ (run_model_check.sh).  wolframscript may print "libc++abi: ... MathLink::MLException" when LoopTools is
# unloaded at the end; the results are written before that.
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
PY="$HOME/miniforge3/envs/qft/bin/python"
mkdir -p work results

echo "=== q^2 values"
"$PY" running_numeric.py --nodes

echo "=== FeynCalc / Package-X / LoopTools (about 1 min)"
wolframscript -file running_feyncalc.wl 2>&1 | grep -E '^\((a|b)\)'

echo "=== COLLIER"
gfortran -I"$HOME/hep/include" running_collier.f90 -L"$HOME/hep/lib" -lcollier -o work/running_collier && echo "built work/running_collier"

echo "=== dispersion, effective charge, Landau poles, Uehling, figure"
"$PY" running_numeric.py
