#!/bin/bash
# Step (1) of the QCD note: FeynRules model -> FeynArts model and UFO, and the MadGraph diagrams.
#   1. generate_QCD.wl : checks (hermiticity, normalisation, masses), all 16 vertices against the note (Fig. 1),
#                        writes generated/
#   2. model_mg5.mg5   : u u~ > t t~ (expect 1 diagram), g g > t t~ (3), g g > g g (4), u u~ > g g (3), u g > u g (3),
#                        u u~ > u u~ (2), u u > u u (2), u d > u d (1), e+ e- > u u~ (1), e+ e- > t t~ (1),
#                        e+ e- > u u~ g (2), u u~ > t t~ g (5), g g > t t~ g (16), g g > g g g (25)
cd "$(dirname "$0")"
wolframscript -file generate_QCD.wl
mkdir -p work && rm -rf work/QCD_UFO && cp -R generated/QCD_UFO work/
"$HOME/hep/MG5_aMC_v3_8_1/bin/mg5_aMC" model_mg5.mg5 > work/model_mg5.log 2>&1
grep -E "^Process|diagrams:|^[0-9]+ processes with" work/model_mg5.log
