#!/bin/bash
# Step (4) of the SM note: on-shell counterterms, charge renormalization in R_xi gauge, tadpole schemes, FormCalc.
#   1. ct_feyncalc.wl: (a) Pi^AA(0), Sigma^AZ_T(0) by expansion in the external momentum (vacuum integrals, exact in D):
#                      Feynman gauge vs Eqs. (Pi0), (dZe); general R_xi (SM.mod): delta Z_e independent of xi;
#                      (b) tadpole-attached diagrams c_V T, delta s_W^2 the same in both tadpole schemes, T(xi) vs Eq. (Txi);
#                      (c) the note's counterterms at the numerical point -> results/ct_note.m
#   2. ct_formcalc.wl: FormCalc's RenConst (SM.mod) vs the note with LoopTools -> results/ct_comparison.csv,
#                      the loop functions -> results/ct_functions.csv           (own kernel, unpatched FeynArts)
#   3. ct_numeric.py : B0 and DB0 from mpmath integrals vs LoopTools
# Needs Src/generated/ (run run_model_check.sh first).
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
PY="$HOME/miniforge3/envs/qft/bin/python"
mkdir -p work results

echo "=== FeynCalc"
wolframscript -file ct_feyncalc.wl > work/ct_feyncalc.log 2>&1
grep -E '^\((a|b|c)\)' work/ct_feyncalc.log

echo "=== FormCalc RenConst vs the note (LoopTools)"
wolframscript -file ct_formcalc.wl > work/ct_formcalc.log 2>&1
grep -E '^\((a|d)\)|^   d' work/ct_formcalc.log

echo "=== loop functions: LoopTools vs mpmath"
"$PY" ct_numeric.py
