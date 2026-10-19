#!/bin/bash
# Step (1) of the NLO note: LO widths with MS-bar couplings and pole kinematics.
#   1. generate_SM_CKM.wl : FeynArts model and UFO of SM_CKM.fr (the CKM note's model file), checked to equal the CKM note's
#   2. lo_feyncalc.wl     : sum|M|^2 of Z -> f fbar, H -> f fbar, W+ -> f fbar', t -> d_j W+ against the hand values (symbolic)
#   3. lo_widths.py       : Eq. (lo) with the SM note's MS-bar parameters run to mu (nlo_inputs.py) and the pole masses;
#                           MadGraph compute_widths with param cards of the same couplings and kinematics
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
mkdir -p work results
wolframscript -file generate_SM_CKM.wl > work/generate_SM_CKM.log 2>&1 || { echo "generate_SM_CKM.wl failed"; exit 1; }
grep -E "^(vertex classes|   SM_CKM)" work/generate_SM_CKM.log
wolframscript -file lo_feyncalc.wl > work/lo_feyncalc.log 2>&1 || { echo "lo_feyncalc.wl failed"; exit 1; }
grep -E "^(channels|  .*expect)" work/lo_feyncalc.log | grep -v "= 0 " ; grep -E "^channels" work/lo_feyncalc.log
python3 lo_widths.py --cards
rm -rf work/SM_CKM_UFO && cp -R generated/SM_CKM_UFO work/
"$HOME/hep/bin/mg5_aMC" work/lo_mg5.mg5 > work/lo_mg5.log 2>&1
python3 lo_widths.py
