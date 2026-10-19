#!/bin/bash
# Step (6) of the Higgs note: H -> g g at NLO QCD in the heavy-top effective theory (after run_lo_check.sh: generated/,
# work/card_H.dat).
#   1. generate_HggEFT.wl   : SM_CKM.fr with the operator -(1/4) cHgg (H/vev) G G (HggEFT.fr): FeynArts model and UFO     (~30 s)
#   2. hgg_eft_feyncalc.wl  : Born, real H -> g g g, g q qbar and the virtual correction exact in d = 4 - 2 eps, the MS-bar
#                             alpha_s of the operator, the sum                                                           (~60 s)
#   3. hgg_mg5.py           : MadGraph's tree |M|^2 of H -> g g g, g u ubar with the same UFO at Dalitz points            (~30 s)
#   4. hgg_widths.py        : the NLO width with the heavy-top K factor at mu = M_H/2, M_H, 2 M_H
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
mkdir -p work results
[ -e generated/FeynmanRules_SM_CKM.m ] && [ -e work/card_H.dat ] || { echo "run run_lo_check.sh first"; exit 1; }
wolframscript -file generate_HggEFT.wl > work/generate_HggEFT.log 2>&1 || { echo "generate_HggEFT.wl failed"; exit 1; }
grep -E "^(SM vertex|operator|H g g)" work/generate_HggEFT.log | cut -c1-200
wolframscript -file hgg_eft_feyncalc.wl > work/hgg_eft.log 2>&1 || { echo "hgg_eft_feyncalc.wl failed"; exit 1; }
grep -E "diagram|^4d|expanded|exact|O\(eps\)|at eps = 0|units of" work/hgg_eft.log | grep -v "^in total" | cut -c1-250
python3 hgg_mg5.py --prepare
rm -rf work/SM_CKM_HEFT_UFO work/me_hggtree && cp -R generated/SM_CKM_HEFT_UFO work/
(cd work/mg5run_hgg && "$HOME/hep/bin/mg5_aMC" hgg_mg5.mg5 > hgg_mg5.log 2>&1) || { echo "mg5_aMC failed"; exit 1; }
python3 hgg_mg5.py | tail -2
python3 hgg_widths.py
