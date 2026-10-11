#!/bin/bash
# Total cross section of phi phi scattering to one loop in d = 4, phi^3 + phi^4 (research note models/phi34, step (6)).
#   1. COLLIER evaluator of the MS-bar M1 at the quadrature nodes          (xsec_collier.f90)
#   2. MadGraph, tree-level phi phi -> phi phi phi                         (xsec_mg5_2to3.mg5)
#   3. sigma0, sigma1 (Eq. (12); MadLoop at the same nodes), sigma(2->3) by adaptive Monte Carlo in two
#      parametrizations, comparison and figure -> results/xsec.csv, ../figs/xsec_d4.pdf  (xsec_numeric.py)
# Needs work/ml_OS (run_madloop_check.sh) and generated/Phi34_UFO (run_model_check.sh).
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
mkdir -p work results
[ -x work/ml_OS/SubProcesses/P0_phiphi_phiphi/check ] || ./run_madloop_check.sh

echo "=== COLLIER"
gfortran -I"$HOME/hep/include" xsec_collier.f90 -L"$HOME/hep/lib" -lcollier -o work/xsec_collier && echo "built work/xsec_collier"

echo "=== MadGraph, phi phi -> phi phi phi"
rm -rf work/mg5_2to3 work/Phi34_UFO
cp -R generated/Phi34_UFO work/Phi34_UFO   # MadGraph rewrites the UFO it imports
mg5_aMC xsec_mg5_2to3.mg5 > work/xsec_mg5_2to3.log 2>&1
rm -f py.py MG5_debug
grep -E '^\s+Cross-section' work/xsec_mg5_2to3.log

echo "=== cross sections"
"$HOME/miniforge3/envs/qft/bin/python" xsec_numeric.py
