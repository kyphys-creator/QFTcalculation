#!/bin/bash
# Step (3) of the SM note: tadpole and self-energies in a general R_xi gauge.
#   1. oneloop_feyncalc.wl : T against Eq. (T) (exact in D), 1PI self-energies and the tadpole-attached diagrams,
#                            UV poles at k^2 = M^2 against (1/2) dM^2/dln mu -> results/oneloop_sigma.m (about 1 min)
#   2. oneloop_numeric.wl  : k^2 structure of the UV poles (field renormalization), MS-bar finite parts and pole
#                            masses in six gauges; writes the B0 arguments for COLLIER
#   3. oneloop_collier.f90 : the same B0 from COLLIER; oneloop_numeric.wl is run again to compare the libraries
#   4. oneloop_smmod.wl    : the same T and 1PI self-energies from FeynArts' SMQCD.mod (Denner's conventions)
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
mkdir -p work
wolframscript -file oneloop_feyncalc.wl 2>&1 | grep -E "^\(|expect|diagrams|Summary"
wolframscript -file oneloop_numeric.wl > work/oneloop_numeric_1.log 2>&1
/opt/homebrew/bin/gfortran -I"$HOME/hep/include" oneloop_collier.f90 -L"$HOME/hep/lib" -lcollier \
  -Wl,-rpath,"$HOME/hep/lib" -o work/oneloop_collier
work/oneloop_collier results/oneloop_b0_args.csv results/oneloop_collier_b0.csv | grep 'COLLIER:'
wolframscript -file oneloop_numeric.wl 2>&1 | grep -E "^\(|spread|pole masses|LoopTools -"
wolframscript -file oneloop_smmod.wl 2>&1 | grep -E "expect|Summary|masses in"
