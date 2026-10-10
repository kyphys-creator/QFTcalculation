#!/bin/bash
# Total cross section of phi phi scattering to O(g^6) in d = 4 (research note, step (7)).
#   1. COLLIER evaluator of the MS-bar M1 at the quadrature nodes          (xsec_collier.f90)
#   2. MadGraph, tree-level phi phi -> phi phi phi                         (xsec_mg5_2to3.mg5)
#   3. sigma0, sigma1 (Eq. (20); MadLoop at the same nodes), sigma(2->3) by adaptive Monte Carlo in two
#      parametrizations, comparison and figure -> results/xsec.csv, ../figs/xsec_d4.pdf  (xsec_numeric.py)
# Needs work/ml_OS (run_madloop_check.sh) and generated/Phi3_UFO (generate_Phi3.wl).
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
mkdir -p work results
[ -x work/ml_OS/SubProcesses/P0_phiphi_phiphi/check ] || ./run_madloop_check.sh

echo "=== COLLIER"
gfortran -I"$HOME/hep/include" xsec_collier.f90 -L"$HOME/hep/lib" -lcollier -o work/xsec_collier && echo "built work/xsec_collier"

echo "=== MadGraph, phi phi -> phi phi phi"
rm -rf work/mg5_2to3 work/Phi3_UFO
cp -R generated/Phi3_UFO work/Phi3_UFO   # MadGraph rewrites the UFO it imports
mg5_aMC xsec_mg5_2to3.mg5 > work/xsec_mg5_2to3.log 2>&1
rm -f py.py MG5_debug
grep -E '^\s+Cross-section' work/xsec_mg5_2to3.log

echo "=== cross sections"
"$HOME/miniforge3/envs/qft/bin/python" xsec_numeric.py
