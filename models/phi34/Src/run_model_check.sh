#!/bin/bash
# Step (1) of the phi^3 + phi^4 note: FeynRules model -> FeynArts model and UFO, and the MadGraph diagrams.
#   1. generate_Phi34.wl : checks (hermiticity, normalisation), vertices -I gphi, -I lamphi, writes generated/
#   2. model_mg5.mg5     : phi phi -> phi phi (expect 4 diagrams) and -> phi phi phi (expect 25)
cd "$(dirname "$0")"
wolframscript -file generate_Phi34.wl
mkdir -p work && rm -rf work/Phi34_UFO && cp -R generated/Phi34_UFO work/
"$HOME/hep/MG5_aMC_v3_8_1/bin/mg5_aMC" model_mg5.mg5 > work/model_mg5.log 2>&1
grep -E "^Process|diagrams:" work/model_mg5.log
