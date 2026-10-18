#!/bin/bash
# Step (8) of the CKM note: the Delta F = 2 boxes and Delta m_d, Delta m_s, epsilon_K.
#   1. df2_ckm_feyncalc.wl : the boxes of B_s, B_d and K mixing at zero momentum, general R_xi (about 7 minutes)
#   2. df2_ckm_check.wl    : exact checks (closed forms): CKM structure, UV finiteness, xi dependence and GIM, the
#                            Inami-Lim S_0; this note's S at the physical masses
#   3. df2_physics.py      : Delta m_d, Delta m_s, epsilon_K with the literature hadronic inputs and QCD factors
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
mkdir -p work
wolframscript -file df2_ckm_feyncalc.wl > work/df2_ckm_feyncalc.out 2>&1
grep -E "^   (Bs|Bd|K)|WARNING|Summary" work/df2_ckm_feyncalc.out | cut -c1-300
wolframscript -file df2_ckm_check.wl > work/df2_ckm_check.out 2>&1
grep -E "^\(|Summary|WARNING" work/df2_ckm_check.out | cut -c1-300
python3 df2_physics.py
