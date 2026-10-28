#!/bin/bash
# Step (2) of the two-loop note: the two-loop renormalization group and the Landau-gauge effective potential (seconds).
#   1. rg2_mv.wl      : general two-loop formulas (Machacek-Vaughn, Luo-Wang-Xiao) with explicit tensors; check on the
#                       Standard Model's U(1)_Y part; beta functions and gamma of the model; the counterterms built
#                       from them against the poles of step (1) (results/v2_landau.m); Q dV/dQ = O(1/K^3)
#                       -> results/rg2.m, results/rg2_beta.csv
#   2. v2_tsil.c      : TSIL 1.46, I(x,y,z) at any Q (built into work/v2_tsil)
#   3. rg2_numeric.py : V along the RG flow from Q = 1 to Q = 2 at one and two loops -> results/rg2_numeric.csv
cd "$(dirname "$0")"
PY="$HOME/miniforge3/envs/qft/bin/python"
mkdir -p work results
wolframscript -file rg2_mv.wl 2>&1 | grep -E "^\("
cc -DTSIL_SIZE_DOUBLE -I"$HOME/hep/include" -o work/v2_tsil v2_tsil.c -L"$HOME/hep/lib" -ltsil -lm 2>/dev/null
"$PY" rg2_numeric.py
