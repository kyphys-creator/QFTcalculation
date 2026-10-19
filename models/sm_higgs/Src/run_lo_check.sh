#!/bin/bash
# Step (1) of the Higgs note: the model, the tree amplitudes and the LO widths.
#   1. generate_SM_CKM.wl : FeynArts model and UFO of SM_CKM.fr (the CKM note's model file), checked to equal the NLO note's
#   2. lo_feyncalc.wl     : sum|M|^2 of H -> f fbar, H -> V f fbar' (general R_xi, masses) and H -> 4 f against the hand forms
#                           (symbolic); writes work/me_hvff.txt
#   3. lo_widths.py       : Eq. (lo) with the MS-bar and the pole Yukawa couplings; Eq. (vv) against the Dalitz integral;
#                           the fermion masses; H -> 4 f with Breit-Wigner propagators
#   4. lo_mg5.py          : MadGraph's two-body widths, standalone sum|M|^2 and madevent four-lepton widths (about 1 min of the 3)
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
mkdir -p work results
wolframscript -file generate_SM_CKM.wl > work/generate_SM_CKM.log 2>&1 || { echo "generate_SM_CKM.wl failed"; exit 1; }
grep -E "^(vertex classes|   SM_CKM)" work/generate_SM_CKM.log
wolframscript -file lo_feyncalc.wl > work/lo_feyncalc.log 2>&1 || { echo "lo_feyncalc.wl failed"; exit 1; }
grep -E "^  .*expect" work/lo_feyncalc.log | grep -v ": 0   (expect 0)"; grep -E "^checks" work/lo_feyncalc.log
python3 lo_widths.py
python3 lo_mg5.py --prepare
rm -rf work/SM_CKM_UFO && cp -R generated/SM_CKM_UFO work/
(cd work/mg5run && "$HOME/hep/bin/mg5_aMC" lo_mg5.mg5 > ../lo_mg5.log 2>&1)
python3 lo_mg5.py --events
python3 lo_mg5.py
