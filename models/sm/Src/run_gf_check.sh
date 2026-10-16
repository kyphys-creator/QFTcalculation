#!/bin/bash
# Step (6) of the SM note: G_F and alpha(0) in terms of the MS-bar parameters.
#   1. mudecay_feyncalc.wl : one-loop muon decay at zero momentum (tree, vertex, box, external legs, Sigma^W(0) with
#                            the tadpoles) in a general R_xi gauge with a photon mass (about 11 minutes)
#   2. mudecay_check.wl    : UV pole = (1/2) dln v^2/dln mu, no ln MA, gauge independence of DeltaHat, Sirlin's
#                            delta_VB in the Feynman gauge, DeltaHat at the benchmark
#   3. alpha_matching.wl   : e(mu)/e_OS from the photon two-point functions of step (3) (run run_oneloop_check.sh
#                            first), gauge independence, alpha-hat(MZ) against PDG
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
wolframscript -file mudecay_feyncalc.wl 2>&1 | grep -E "expect|computed|unprojected|uncontracted|written"
wolframscript -file mudecay_check.wl 2>&1 | grep -E "^\(|Summary"
wolframscript -file alpha_matching.wl 2>&1 | grep -E "^\(|Summary"
