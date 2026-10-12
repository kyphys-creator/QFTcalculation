#!/bin/bash
# Step (1) of the pseudoscalar Yukawa note: FeynRules model -> FeynArts model and UFO, and the MadGraph diagrams.
#   1. generate_PsYukawa.wl : checks (hermiticity, normalisation, masses), vertices yps gamma5 and -I lamphi,
#                             writes generated/
#   2. model_mg5.mg5        : phi phi -> phi phi (expect 1 diagram), psi psi~ -> phi phi (2), psi psi~ -> psi psi~ (2),
#                             psi psi -> psi psi (2), psi psi~ -> phi phi phi (7), phi phi -> phi psi psi~ (7)
cd "$(dirname "$0")"
wolframscript -file generate_PsYukawa.wl
mkdir -p work && rm -rf work/PsYukawa_UFO && cp -R generated/PsYukawa_UFO work/
"$HOME/hep/MG5_aMC_v3_8_1/bin/mg5_aMC" model_mg5.mg5 > work/model_mg5.log 2>&1
grep -E "^Process|diagrams:|^[0-9]+ processes with" work/model_mg5.log
