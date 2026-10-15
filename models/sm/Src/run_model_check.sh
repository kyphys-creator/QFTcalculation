#!/bin/bash
# Step (1) of the SM note: FeynRules model -> FeynArts model and UFO, and the MadGraph diagrams.
#   1. generate_SM.wl : checks (hermiticity, normalisation, masses), all 93 vertex classes against the note's tables,
#                       writes generated/ (SM_FA with all fermion masses, SM_UFO with e, mu, u, d, s, c massless)
#   2. make_restrict.py: MadGraph's restriction card restrict_massless.dat (cabi = 0; e, mu, u, d, s, c massless)
#   3. model_mg5.mg5  : 21 processes in unitary gauge and in Feynman gauge (numbers of diagrams in the note's table)
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
wolframscript -file generate_SM.wl
mkdir -p work && rm -rf work/SM_UFO && cp -R generated/SM_UFO work/
"$HOME/miniforge3/envs/qft/bin/python" make_restrict.py work/SM_UFO
mg5_aMC model_mg5.mg5 > work/model_mg5.log 2>&1
grep -E "^Process|diagrams:|^[0-9]+ processes with|set gauge|Change to the|gauge" work/model_mg5.log
