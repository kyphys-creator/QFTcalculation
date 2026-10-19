#!/bin/bash
# Step (5) of the NLO note: the effective couplings of the Z, sin^2 theta_eff and the Z-pole asymmetries.
#   1. zeff.wl   : V_f, A_f from the renormalized weak form factors of step (4a) (zweak.wl's S-matrix element): gauge independence,
#                  mu = M_Z/2, M_Z, 2 M_Z, the parts (mixing, vertex, legs), and the inputs of the SM note's alpha scheme   (~3 min)
#   2. zpole.py  : sin^2 theta_eff^lept, A_l, A_b, A_c, A_FB^{0,l}, A_FB^{0,b}, A_FB^{0,c} against LEP and SLD (references)
# Needs step (4a) first (run_zweak_check.sh: work/zff_*.m) and the SM note's self-energies (models/sm/Src/results/oneloop_sigma.m).
cd "$(dirname "$0")"
mkdir -p work results
for f in generated/SM_CKM_FA work/zff_11.m work/zff_43.m ../../sm/Src/results/oneloop_sigma.m ../../sm/Src/results/msbar_fit.csv; do
  [ -e "$f" ] || { echo "$f missing: run the checks of step (4a) first"; exit 1; }
done
wolframscript -file zeff.wl > work/zeff.log 2>&1 || { echo "zeff.wl failed"; exit 1; }
grep -E "^\((a|b|c|d)\)" work/zeff.log | sed -E 's/NumberForm\[([^,]+), [0-9]+\]/\1/g; s/ScientificForm\[([^,]+), [0-9]\]/\1/g; s/`[0-9.]+//g' | \
  sed -E 's/([0-9]\.[0-9]{12})[0-9]+/\1/g' | cut -c1-250
python3 zpole.py
