#!/bin/bash
# Step (5) of the CKM note: W+ -> u_i dbar_j at one loop with the MS-bar V and with the Denner-Sack V.
#   1. wud_vertex_feyncalc.wl : the 1PI vertex of the six channels in a general R_xi gauge (one process per channel,
#                               in parallel; about 8 minutes) -> work/wud_vertex_<i><j>.m
#   2. wud_renormalized.wl    : LSZ factors and counterterms; exact UV finiteness, gauge independence (MS-bar) and
#                               gauge dependence (Denner-Sack) at the benchmark; Feynman-gauge numbers for FormCalc
#                               (needs results/oneloop_ckm_sigma.m of step (3))
#   3. wud_formcalc.wl        : FeynArts' SM.mod with the CKM matrix and FormCalc (on-shell scheme, Feynman gauge),
#                               against the numbers of 2.
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
mkdir -p work
pids=""
for ch in "1 1" "1 2" "1 3" "2 1" "2 2" "2 3"; do
  set -- $ch
  wolframscript -file wud_vertex_feyncalc.wl $1 $2 > work/wud_vertex_$1$2.out 2>&1 &
  pids="$pids $!"
done
for p in $pids; do wait $p; done
grep -h -E "^\(a\)|W\+ -> u_|^\(d\)|WARNING" work/wud_vertex_??.out | sort -u | cut -c1-300
wolframscript -file wud_renormalized.wl > work/wud_renormalized.out 2>&1
grep -E "^\(|^   |Summary|WARNING" work/wud_renormalized.out | cut -c1-400
wolframscript -file wud_formcalc.wl > work/wud_formcalc.out 2>&1
grep -E "^\(|^   |Summary|WARNING" work/wud_formcalc.out | cut -c1-400
