#!/bin/bash
# Thin-wall growth of the one-loop correction and the scheme without tadpole cancellation (research note models/phi34,
# step (11)): decomposition of ln D, thin-wall coefficients, the one-loop degenerate point from the effective potential,
# one-loop agreement of the two schemes, and the cosmological condition in the N scheme
#   -> results/thinwall.csv, ../figs/thinwall.pdf                                                   (thinwall_numeric.py)
# Needs results/prefactor.csv (run_prefactor_check.sh).
cd "$(dirname "$0")"
"$HOME/miniforge3/envs/qft/bin/python" thinwall_numeric.py
