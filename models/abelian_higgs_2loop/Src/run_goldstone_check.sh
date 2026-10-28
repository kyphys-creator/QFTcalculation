#!/bin/bash
# Step (3) of the two-loop note: the Goldstone boson at small G and its resummation (about 20 seconds).
#   1. v2_tsil.c            : TSIL 1.46, I(x,y,z) at any Q (built into work/v2_tsil)
#   2. goldstone_ir.wl      : V2 for small G (Martin's expansions of I), the minimization condition, the G-free condition
#                             of the resummed potential (Dh1, Dh2), the hbar expansion, the minimum value, RG invariance
#                             of both; numbers at Q = 1, 2 -> results/goldstone.m, goldstone_min.csv, goldstone_curve.csv
#   3. goldstone_numeric.py : Martin's formulas for I against TSIL; figs/goldstone.pdf; the minimum of the resummed and
#                             of the two-loop potential found numerically at Q = 2 -> results/goldstone_numeric.csv
cd "$(dirname "$0")"
PY="$HOME/miniforge3/envs/qft/bin/python"
mkdir -p work results
cc -DTSIL_SIZE_DOUBLE -I"$HOME/hep/include" -o work/v2_tsil v2_tsil.c -L"$HOME/hep/lib" -ltsil -lm 2>/dev/null
wolframscript -file goldstone_ir.wl 2>&1 | grep -E "^\("
"$PY" goldstone_numeric.py
