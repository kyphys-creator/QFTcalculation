#!/bin/bash
# Step (3) of the Higgs note: H -> q qbar at NLO QCD for massless quarks (after run_lo_check.sh: generated/).
#   1. hqq_massless_feyncalc.wl : real, vertex and the MS-bar Yukawa counterterm exact in d = 4 - 2 eps; the d = 4 real |M|^2
#                                 against the FeynArts model for H -> u ubar g, mu- mu+ gamma                      (~10 s)
#   2. hqq_gluonmass.wl         : the same with a gluon mass in 4 dimensions (FeynCalc, Package-X, NIntegrate)   (~3 min)
#   3. hqq_widths.py            : Eq. (hqq) with the MS-bar couplings at mu = M_H/2, M_H, 2 M_H against Eq. (hqqpole)
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
mkdir -p work results
[ -e generated/SM_CKM_FA ] || { echo "generated/SM_CKM_FA missing: run run_lo_check.sh first"; exit 1; }
wolframscript -file hqq_massless_feyncalc.wl > work/hqq_massless.log 2>&1 || { echo "hqq_massless_feyncalc.wl failed"; exit 1; }
grep -E "expect|exact|expanded|O\(eps\)" work/hqq_massless.log | cut -c1-200
wolframscript -file hqq_gluonmass.wl > work/hqq_gluonmass.log 2>&1 || { echo "hqq_gluonmass.wl failed"; exit 1; }
grep -E "expect|^w =" work/hqq_gluonmass.log | cut -c1-200
python3 hqq_widths.py
