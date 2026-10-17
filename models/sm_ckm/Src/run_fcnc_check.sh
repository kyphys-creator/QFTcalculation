#!/bin/bash
# Step (7) of the CKM note: b -> s gamma and Z -> b sbar at one loop in a general R_xi gauge.
#   1. fcnc_ckm_feyncalc.wl : the 1PI vertices of the two processes (one process per call, in parallel; about 3 minutes)
#   2. fcnc_ckm_numeric.wl  : the external legs (step (3) self-energies), exact UV finiteness, gauge invariance, xi
#                             independence, GIM, and the comparison with the Inami-Lim functions D'_0 and C_0
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
mkdir -p work
pids=""
for p in bsg zbs; do
  wolframscript -file fcnc_ckm_feyncalc.wl $p > work/fcnc_$p.out 2>&1 &
  pids="$pids $!"
done
for p in $pids; do wait $p; done
grep -h -E "^   (bsg|zbs)|WARNING|Summary" work/fcnc_bsg.out work/fcnc_zbs.out | cut -c1-300
wolframscript -file fcnc_ckm_numeric.wl > work/fcnc_ckm_numeric.out 2>&1
grep -E "^\(|^   [0-9]|Summary|WARNING" work/fcnc_ckm_numeric.out | cut -c1-300
