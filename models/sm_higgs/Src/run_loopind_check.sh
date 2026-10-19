#!/bin/bash
# Step (2) of the Higgs note: the loop-induced H -> gamma gamma, Z gamma, g g (after run_lo_check.sh: generated/, work/card_H.dat).
#   1. loopind_feyncalc.wl aa | za | gg : the one-loop amplitudes in a general R_xi gauge, their UV poles (symbolic); in parallel
#   2. loopind.wl                       : Package-X: gauge and mu independence, the Ward identity, each loop against Eq. (loop)
#   3. loopind_madloop.py               : MadLoop with the CKM note's NLO UFO (the model import takes about 5 min)
#   4. loopind_widths.py                : the LO widths and their dependence on the inputs
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
mkdir -p work results
for p in aa za gg; do wolframscript -file loopind_feyncalc.wl $p > work/loopind_$p.log 2>&1 & done
wait
for p in aa za gg; do grep -E "^H ->|left over|1/eps|gauge param|WARNING" work/loopind_$p.log | cut -c1-200; done
wolframscript -file loopind.wl > work/loopind.log 2>&1 || { echo "loopind.wl failed"; exit 1; }
grep -E "^H ->|M_H =|rel. diff" work/loopind.log | cut -c1-200
python3 loopind_madloop.py --prepare
(cd work/ml_loopind && "$HOME/hep/bin/mg5_aMC" run.mg5 > mg5.log 2>&1)
python3 loopind_madloop.py
python3 loopind_widths.py
