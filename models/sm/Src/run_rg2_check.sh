#!/bin/bash
# Steps (8) and (10) of the SM note: two-loop beta functions from the note's model, the running of the couplings and the
# decay of the electroweak vacuum.
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
#   6. vacuum_decay.py (step (10)): the RG-improved effective potential (Landau gauge, the note's RGEs from the step (7)
#      values; symbolic checks against Eq. (beta), gamma_Phi and Eq. (T)), the instability scale, the bounce (shooting) and
#      the decay probability; the literature start and RGEs as a reference -> results/vacuum_decay.csv, fig_veff.pdf
#   7. vacuum_gravity.py (step (10)): the leading gravitational correction to the Fubini bounce (O(4) metric, checked by
#      graviton exchange) and S(R) with the note's running -> results/vacuum_gravity.csv
#   8. vacuum_prefactor.py (step (10)): the one-loop prefactor (Higgs, W, Z with Goldstones and ghosts, top; bounce_det.py)
#      and the R integral with the gravitational correction -> results/vacuum_prefactor.csv, vacuum_prefactor_grid.csv
#   9. vacuum_gauge_check.py (step (10)): the W/Z sector in background R_xi (xi = 0.5 ... 3) and the counting of the
#      transverse modes from the log divergence of the mode sum -> results/vacuum_gauge_check.csv
# Needs Kira 3.1 and Fermat in ~/hep, AMFlow 2.0 in ~/hep/AMFlow-2.0 (about 65 minutes in all).
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
python3 vacuum_decay.py
python3 vacuum_gravity.py
python3 vacuum_prefactor.py
python3 vacuum_gauge_check.py
