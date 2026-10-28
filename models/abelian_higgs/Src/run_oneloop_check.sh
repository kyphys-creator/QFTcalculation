#!/bin/bash
# Step (3) of the abelian Higgs note: tadpole and two-point functions in a general R_xi gauge.
#   1. oneloop_feyncalc.wl : T, Sigma^H, Sigma_T, Sigma_L, Sigma^AG, Sigma^GG, Sigma^c (1PI and tadpole-attached) from the
#                            note's FeynArts model against Eqs. (T), (se) and App. D (exact in D), Sigma^H diagram by
#                            diagram, the Slavnov-Taylor identity, UV poles and counterterms -> results/oneloop_sigma.m
#   2. oneloop_numeric.wl  : MS-bar finite parts, pole masses at xi = 0, 1/2, 1, 3, 10, optical theorem, off-shell xi
#                            dependence (Package-X), LoopTools; writes the B0 arguments for COLLIER
#   3. oneloop_collier.f90 : the same B0 from COLLIER; oneloop_numeric.wl is run again to compare the libraries
# Needs Src/generated/ (run generate_AbelianHiggs.wl first).  The LoopTools link prints "libc++abi: terminating ...
# MathLink::MLException" when the kernel exits; the results are written before that (not a script error).
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
mkdir -p work results
wolframscript -file oneloop_feyncalc.wl 2>&1 | grep -E "^\(|^   \{|Summary"
wolframscript -file oneloop_numeric.wl > work/oneloop_numeric_1.log 2>&1
/opt/homebrew/bin/gfortran -I"$HOME/hep/include" oneloop_collier.f90 -L"$HOME/hep/lib" -lcollier \
  -Wl,-rpath,"$HOME/hep/lib" -o work/oneloop_collier
work/oneloop_collier results/oneloop_b0_args.csv results/oneloop_collier_b0.csv | grep 'COLLIER:'
wolframscript -file oneloop_numeric.wl 2>&1 | grep -E "^\(|^      pole"
