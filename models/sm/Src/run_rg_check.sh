#!/bin/bash
# Step (4) of the SM note: Slavnov-Taylor identities and the beta functions.
#   1. st_feyncalc.wl        : the identities Eq. (st) in a general R_xi gauge, with and without the tadpole-attached
#                              diagrams (about 1 minute)
#   2. rg_general.py         : the general one-loop formulas with the explicit SM field content vs Eq. (beta)
#   3. rg_feyncalc_check.wl  : charge renormalization Eq. (dZe) and the running of v_beta Eq. (vbeta) from the
#                              functions of step (3) (run run_oneloop_check.sh first)
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
wolframscript -file st_feyncalc.wl 2>&1 | grep -E "ST |without|mixing|Summary"
python3 rg_general.py | tail -1
wolframscript -file rg_feyncalc_check.wl 2>&1 | grep -E "^\(|Summary"
