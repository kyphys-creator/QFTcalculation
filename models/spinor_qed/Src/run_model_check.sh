#!/bin/bash
# Step (1) of the spinor QED note: FeynRules model -> FeynArts model and UFO, and the MadGraph diagrams.
#   1. generate_SpinorQED.wl : checks (hermiticity, normalisation, masses), vertices -I ee gamma^mu for e and mu,
#                              writes generated/
#   2. model_mg5.mg5         : e+ e- > mu+ mu- (expect 1 diagram), e+ e- > e+ e- (2), e- a > e- a (2), e+ e- > a a (2),
#                              e- mu- > e- mu- (1), e- e- > e- e- (2), e+ e- > mu+ mu- a (4), e+ e- > e+ e- a (8),
#                              e+ e- > a a a (6)
cd "$(dirname "$0")"
wolframscript -file generate_SpinorQED.wl
mkdir -p work && rm -rf work/SpinorQED_UFO && cp -R generated/SpinorQED_UFO work/
"$HOME/hep/MG5_aMC_v3_8_1/bin/mg5_aMC" model_mg5.mg5 > work/model_mg5.log 2>&1
grep -E "^Process|diagrams:|^[0-9]+ processes with" work/model_mg5.log
