#!/bin/bash
# Step (5) of the two-loop note: the Coleman-Weinberg model (m2 = 0, lam ~ e^4/K) at the next order.
#   1. v2_tsil.c  : TSIL 1.46, I(x,y,z) (built into work/v2_tsil)
#   2. cw_nlo.wl  : V2 at lam -> 0 (Landau; background R_xi with the two-loop Nielsen identity), the minimum value and
#                   its RG invariance, the curvature ratio; the full one- and two-loop potentials minimized numerically
#                   for e = 1/2 ... 1/16 -> results/cw_nlo.csv, results/cw_nlo.m
cd "$(dirname "$0")"
mkdir -p work results
cc -DTSIL_SIZE_DOUBLE -I"$HOME/hep/include" -o work/v2_tsil v2_tsil.c -L"$HOME/hep/lib" -ltsil -lm 2>/dev/null
wolframscript -file cw_nlo.wl 2>&1 | grep -E "^\("
