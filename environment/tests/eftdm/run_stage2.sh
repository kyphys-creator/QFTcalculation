#!/bin/bash
# Stage 2 of the EFT and dark-matter tools (environment.pdf): DirectDM, Python 2.2.3 and Mathematica 1.2.1.
# About 1 minute.
cd "$(dirname "$0")"
mkdir -p out
~/hep/bin/wolframscript -file ddm_mma.wl > out/ddm_mma.log 2>&1 || { echo "ddm_mma.wl failed: out/ddm_mma.log"; exit 1; }
~/miniforge3/envs/qft/bin/python test_directdm.py
