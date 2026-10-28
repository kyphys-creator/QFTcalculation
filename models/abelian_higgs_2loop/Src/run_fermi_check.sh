#!/bin/bash
# Step (4), Fermi gauge, of the two-loop note (about 30 seconds).
#   0. work/V2AH          : Martin-Patel's ancillary file (arXiv:1808.07615v1), the two-loop potential of the model for
#                           general gauge fixing; fetched from arXiv into work/ (not redistributed here), SHA-256 checked
#   1. v2_tsil.c          : TSIL 1.46, I(x,y,z) with complex values for negative squared masses (work/v2_tsil)
#   2. fermi_v2.wl        : the file against our diagrams and step (1); RG invariance in Fermi gauge through 1/K^2;
#                           the fixed-order minimum in the Fermi and background-field R_xi gauges; Fermi gauge near G = 0
#                           -> results/fermi_min.csv, results/fermi_ir.csv
#   3. fermi_plot.py      : figs/fermi.pdf
cd "$(dirname "$0")"
PY="$HOME/miniforge3/envs/qft/bin/python"
SHA=7888f139cdaad93303d847daabc29d7e1bc6f1f660d5cc163cb6885d14805529
mkdir -p work results
[ -f work/V2AH ] || curl -sS -L -o work/V2AH https://arxiv.org/src/1808.07615v1/anc/V2AH
if [ "$(shasum -a 256 work/V2AH | cut -d' ' -f1)" != "$SHA" ]; then echo "ERROR: work/V2AH differs from the expected file"; exit 1; fi
cc -DTSIL_SIZE_DOUBLE -I"$HOME/hep/include" -o work/v2_tsil v2_tsil.c -L"$HOME/hep/lib" -ltsil -lm 2>/dev/null
wolframscript -file fermi_v2.wl 2>&1 | grep -E "^\("
"$PY" fermi_plot.py
