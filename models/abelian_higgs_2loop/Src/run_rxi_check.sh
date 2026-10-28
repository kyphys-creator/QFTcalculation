#!/bin/bash
# Step (4) of the two-loop note: the background-field R_xi gauge and the Nielsen identity at two loops.
#   1. v2_rxi_feyncalc.wl : FeynArts two-loop vacuum diagrams in the background-field R_xi gauge, FeynCalc, Kira 3.1,
#                           one-loop counterterm insertions; local poles against Martin-Patel's two-loop counterterms,
#                           the finite part against their Eq. (4.127) -> results/v2_rxi.m
#   2. v2_tsil.c          : TSIL 1.46, I(x,y,z) (built into work/v2_tsil)
#   3. nielsen_rxi.wl     : Landau limit, RG invariance through 1/K^2, the Nielsen identity for the minimum value
#                           (symbolic), numbers at the benchmark -> results/nielsen_rxi.csv
# Each Mathematica step runs in its own kernel.
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
mkdir -p work results
wolframscript -file v2_rxi_feyncalc.wl 2>&1 | grep -E "^\("
cc -DTSIL_SIZE_DOUBLE -I"$HOME/hep/include" -o work/v2_tsil v2_tsil.c -L"$HOME/hep/lib" -ltsil -lm 2>/dev/null
wolframscript -file nielsen_rxi.wl 2>&1 | grep -E "^\("
