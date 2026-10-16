#!/bin/bash
# Step (5) of the SM note: muon decay at one loop, Delta r and M_W.
#   1. dr_feyncalc.wl: vertex and box diagrams and the lepton field renormalization at zero momenta (photon mass as IR
#                      regulator): delta'_VB vs Sirlin/Denner in Feynman gauge, Delta r independent of xi in R_xi;
#                      the note's self-energy formulas -> results/dr_note.m
#   2. dr_numeric.wl : Delta r and MW with LoopTools: Denner's parameter set (Eqs. (8.13), (8.23) of his review and the
#                      note's Eq. (mw)) and the note's point -> results/dr_values.csv         (plain kernel + LoopTools)
#   3. dr_formcalc.wl: Delta r from FormCalc's renormalization constants vs the note at the MW of 2 (own kernel)
# Uses only FeynArts' SM.mod (no generated model files).
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
mkdir -p work results

echo "=== FeynCalc: delta_VB and xi independence"
wolframscript -file dr_feyncalc.wl > work/dr_feyncalc.log 2>&1
grep -E '^\((a|b|c)\)' work/dr_feyncalc.log

echo "=== Delta r and MW (LoopTools)"
wolframscript -file dr_numeric.wl > work/dr_numeric.log 2>&1
grep -E '^\((a|b|d)\)' work/dr_numeric.log

echo "=== FormCalc"
wolframscript -file dr_formcalc.wl > work/dr_formcalc.log 2>&1
grep -E '^\(c\)' work/dr_formcalc.log
