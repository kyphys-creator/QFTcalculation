#!/bin/bash
# e+ e- -> mu+ mu- (gamma) to order alpha^3 (research note models/spinor_qed, step (6)).
#   1. FeynArts + FeynCalc: e+ e- -> mu+ mu- gamma, 4 diagrams, Ward identity, -g against transverse polarization sums,
#      the spin-summed |M|^2 -> generated/msq_eemumua.py                                         (real_feyncalc.wl)
#   2. COLLIER: the one-loop interference K W at the quadrature nodes (CDR)                    (xsec_collier.f90)
#   3. MadGraph: e- e+ > mu- mu+ a with E_gamma > 0.1 at sqrt(s) = 4, 6, 10, diagnostic runs, the standalone matrix
#      element                                                                                   (xsec_mg5.mg5, tree_me_points.f)
#      and again after giving the massive t-channel invariant a grid logarithmic around its pole
#                                                                                        (mg5_tpole.py, xsec_mg5_tpole.mg5)
#   4. soft factor (D-dimensional and photon-mass forms), IR cancellation, hard-photon quadrature and Monte Carlo, DeltaE
#      independence, CDR against four-dimensional spin sums, A_FB, MadGraph (with both grids, binned in the distance y to the
#      electron pole) -> results/xsec.csv, ../figs/xsec_softhard.pdf
#                                                                                                  (xsec_numeric.py)
# Needs Src/generated/ (run_model_check.sh).  MadGraph output goes to Src/work/.
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
mkdir -p work results

echo "=== FeynCalc"
wolframscript -file real_feyncalc.wl 2>&1 | grep -E '^\((a|b|c)\)'

echo "=== COLLIER"
gfortran -I"$HOME/hep/include" xsec_collier.f90 -L"$HOME/hep/lib" -lcollier -o work/xsec_collier && echo "built work/xsec_collier"

echo "=== MadGraph (about 15 min)"
rm -rf work/mg5_xsec3 work/mg5_xsec3_tpole work/sa_xsec3 work/SpinorQED_UFO
cp -R generated/SpinorQED_UFO work/SpinorQED_UFO   # MadGraph rewrites the UFO it imports
mg5_aMC xsec_mg5.mg5 > work/xsec_mg5.log 2>&1
rm -f py.py MG5_debug nsqso_born.inc ../nsqso_born.inc   # output standalone writes nsqso_born.inc here and in ..
grep -E '^\s+Cross-section' work/xsec_mg5.log
( cd work/sa_xsec3/SubProcesses/P1_emep_mummupa && make check > /dev/null 2>&1 && \
  gfortran -O2 -ffixed-line-length-132 -o me_points ../../../../tree_me_points.f matrix.o \
    ../../lib/libdhelas.a ../../lib/libmodel.a -I. )

echo "=== MadGraph with the grid of the massive t-channel pole (about 1 min)"
"$HOME/miniforge3/envs/qft/bin/python" mg5_tpole.py work/mg5_xsec3 work/mg5_xsec3_tpole
mg5_aMC xsec_mg5_tpole.mg5 > work/xsec_mg5_tpole.log 2>&1
rm -f py.py MG5_debug
grep -E '^\s+Cross-section' work/xsec_mg5_tpole.log

echo "=== comparison"
"$HOME/miniforge3/envs/qft/bin/python" xsec_numeric.py
