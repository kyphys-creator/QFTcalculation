#!/bin/bash
# Step (8) of the SM note: two-loop beta functions from the note's model and the running of the couplings.
#   1. twoloop_sym_oneloop.wl: one-loop calibration of the normalizations (symmetric, gaugeless limit)
#   2. twoloop_sym_feyncalc.wl, twoloop_sym_eval.wl: two-loop H, t, b, gluon, ghost two-point functions and the H t tbar vertex
#      -> Z factors, beta_yt^(2), beta_gS^(2), gamma_Phi^(2) (Landau gauge)
#   3. twoloop_lambda_masters.wl (AMFlow), twoloop_lambda_feyncalc.wl, twoloop_lambda_eval.wl: the HHHH vertex at zero
#      momenta with an auxiliary mass -> beta_lambda^(2);  twoloop_lambda_massless.wl: its la = 0 part without the auxiliary mass
#   4. rg_twoloop.py (points 1, 2): the literature RGEs (Buttazzo et al., sm_rge.py) against the general two-loop formulas
#      (Luo-Wang-Xiao) with the explicit SM field content (reference only)
#   5. rg_run.py: running to M_Pl with the note's RGEs (one loop + the two-loop gaugeless terms of 2, 3) and, for comparison,
#      the literature RGEs, from Buttazzo et al., Martin-Robertson and the step (7) values (needs results/msbar_fit.csv from
#      run_fit_check.sh); zero of lambda; FJ versus beta_t masses; fig_rg.pdf
# Needs Kira 3.1 and Fermat in ~/hep, AMFlow 2.0 in ~/hep/AMFlow-2.0 (about 12 minutes in all).
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
mkdir -p work
for f in twoloop_sym_oneloop twoloop_sym_feyncalc twoloop_sym_eval twoloop_lambda_masters twoloop_lambda_feyncalc \
         twoloop_lambda_eval twoloop_lambda_massless; do
  echo "== $f"
  wolframscript -file "$f.wl" > "work/$f.log" 2>&1 || { echo "$f failed (work/$f.log)"; exit 1; }
  grep -E '^\(|^diagrams|^v2' "work/$f.log" | cut -c1-300
done
python3 rg_twoloop.py 1 | tail -3
python3 rg_twoloop.py 2 | tail -1
python3 rg_run.py
