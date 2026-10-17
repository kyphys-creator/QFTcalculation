#!/bin/bash
# Step (3) of the CKM note: quark self-energy matrices, the CKM counterterm and the CKM shifts in a general R_xi gauge.
#   1. oneloop_ckm_feyncalc.wl : 18 quark self-energy entries (1PI and tadpole part) and Sigma_T^WW with the CKM matrix;
#                                Denner's form, off-diagonal UV poles (Eq. (uvoff)) and their xi independence, diagonal
#                                UV poles (Eq. (yrun)), V = 1 against the SM note -> results/oneloop_ckm_sigma.m (~10 min)
#   2. oneloop_ckm_smmod.wl    : the same 1PI entries from FeynArts' SMQCD.mod with $CKM = True (symbolic, general R_xi)
#   3. oneloop_ckm_numeric.wl  : off-diagonal finite parts vs xiW, delta V^DS (UV = MS-bar delta V, finite part vs xiW),
#                                exact CKM shifts of DeltaHat, M_W, m_t vs the SM note's estimate
#                                -> results/oneloop_ckm_numeric.csv
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
mkdir -p work
wolframscript -file oneloop_ckm_feyncalc.wl > work/oneloop_ckm_feyncalc.out 2>&1
grep -E "^\(|expect|Summary|WARNING" work/oneloop_ckm_feyncalc.out
wolframscript -file oneloop_ckm_smmod.wl > work/oneloop_ckm_smmod.out 2>&1
grep -E "note's model|Summary|WARNING" work/oneloop_ckm_smmod.out
wolframscript -file oneloop_ckm_numeric.wl > work/oneloop_ckm_numeric.out 2>&1
grep -E "^\(|^   |Summary" work/oneloop_ckm_numeric.out
