#!/bin/bash
# Step (2) of the NLO note: the cancellation of the infrared poles for massless fermion pairs.
#   1. ir_massless_feyncalc.wl : real emission and virtual correction exact in d = 4 - 2 eps (FeynCalc; Dirichlet integrals of
#                                the 3-body phase space, TID to B0 and C0); the d = 4 real |M|^2 against the FeynArts model
#                                for Z -> mu mu gamma and Z -> u ubar g                                         (~15 s)
#   2. ir_photonmass.wl        : the same with a photon mass in 4 dimensions (FeynCalc, Package-X, NIntegrate)  (~3.5 min)
#   3. ir_mg5.py               : MadGraph's tree |M|^2 of Z -> mu mu gamma and Z -> u ubar g at Dalitz points    (~15 s)
#   4. ir_inclusive.py         : Eq. (inclusive) applied to the LO widths of step (1), against the measured widths
# Needs step (1) first (run_lo_check.sh): generated/SM_CKM_FA, work/SM_CKM_UFO and work/card_Z.dat.
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
mkdir -p work results
for f in generated/SM_CKM_FA work/SM_CKM_UFO work/card_Z.dat; do
  [ -e "$f" ] || { echo "$f missing: run run_lo_check.sh first"; exit 1; }
done
wolframscript -file ir_massless_feyncalc.wl > work/ir_massless.log 2>&1 || { echo "ir_massless_feyncalc.wl failed"; exit 1; }
grep -E "expect|exact|expanded" work/ir_massless.log
wolframscript -file ir_photonmass.wl > work/ir_photonmass.log 2>&1 || { echo "ir_photonmass.wl failed"; exit 1; }
grep -E "expect|drops|d = 4|^w =|leading|Re\(virtual" work/ir_photonmass.log
python3 ir_mg5.py --prepare
rm -rf work/me_ir
(cd work/mg5run && "$HOME/hep/bin/mg5_aMC" ir_mg5.mg5 > ir_mg5.log 2>&1) || { echo "mg5_aMC failed"; exit 1; }
python3 ir_mg5.py | tail -2
python3 ir_inclusive.py
