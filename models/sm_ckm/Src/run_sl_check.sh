#!/bin/bash
# Step (6) of the CKM note: semileptonic decays relative to muon decay and the MS-bar V(mu) from the PDG |V_ij|.
#   1. sl_ckm_feyncalc.wl : d_j -> u_i e nubar_e (six channels) and muon decay at zero momentum, general R_xi (about 12 minutes)
#   2. sl_ckm_check.wl    : with the quark self-energies of step (3): UV finiteness, ln MA, gauge independence, the
#                           universal part (alpha/pi) ln(MZ/MA), the top part G(mu) and the CKM factors (exact)
#   3. ckm_pdg_msbar.py   : the PDG |V_ij| -> MS-bar V(M_Z), and the running to M_t
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
mkdir -p work
wolframscript -file sl_ckm_feyncalc.wl > work/sl_ckm_feyncalc.out 2>&1
grep -E "^\(|^   d_|^   mu|Summary|WARNING" work/sl_ckm_feyncalc.out | cut -c1-300
wolframscript -file sl_ckm_check.wl > work/sl_ckm_check.out 2>&1
grep -E "^\(|^   [uc][dsb]|Summary|WARNING" work/sl_ckm_check.out | cut -c1-400
python3 ckm_pdg_msbar.py
