#!/bin/bash
# Step (1) of the two-loop note: the two-loop effective potential in Landau gauge.
#   1. v2_landau_feyncalc.wl : FeynArts two-loop vacuum diagrams (FeynRules model of models/abelian_higgs), FeynCalc,
#                              Kira 3.1, one-loop counterterm insertions; local poles and the finite part against
#                              Martin's formula (Eq. (V2)) -> results/v2_landau.m
#   2. v2_tsil.c             : TSIL 1.46, I(x,y,z) and A(x) (built into work/v2_tsil)
#   3. v2_amflow.wl          : AMFlow 2.0, the 11 vacuum sunrises at phi = 2, 3 (30 digits) -> results/v2_amflow.csv
#                              (about 40 minutes)
#   4. v2_numeric.py         : I(x,y,z) TSIL against AMFlow; V0, V1/K, V2/K^2 at phi = 2, 3 -> results/v2_numeric.csv
# Each Mathematica step runs in its own kernel.
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
PY="$HOME/miniforge3/envs/qft/bin/python"
mkdir -p work results
wolframscript -file v2_landau_feyncalc.wl 2>&1 | grep -E "^\(" | grep -v "^(d) bare"
cc -DTSIL_SIZE_DOUBLE -I"$HOME/hep/include" -o work/v2_tsil v2_tsil.c -L"$HOME/hep/lib" -ltsil -lm 2>/dev/null
wolframscript -file v2_amflow.wl 2>&1 | grep -E "^\("
"$PY" v2_numeric.py
