#!/bin/bash
# One-loop decay rate around the lambda < 0 bounce with the fermion determinant (research note models/yukawa_ps, step (10)).
#   checks of the scalar and fermion determinants (Gel'fand-Yaglom, exact sums, MS-bar loop integrals) against the closed forms
#   of Andreassen, Frost and Schwartz; the one-loop exponent along the benchmark at the stationary scale; the tree-level cutoff
#   bound for Gamma/V < H0^4 (Higgs-like reading) and the size of the fermion corrections there
#   -> results/prefactor.csv, ../figs/prefactor_d4.pdf                                                 (prefactor_numeric.py)
cd "$(dirname "$0")"
mkdir -p results
"$HOME/miniforge3/envs/qft/bin/python" prefactor_numeric.py
