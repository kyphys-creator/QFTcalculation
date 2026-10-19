#!/bin/bash
# Step (5) of the Higgs note: the weak correction to H -> f fbar (after run_lo_check.sh and run_hqq_massive_check.sh:
# generated/SM_CKM_FA, results/hqq_massive.csv, results/hqq_massive_virtual_ml.csv).
#   1. hff_weak_feyncalc.wl t g : the weak 1PI vertex and the weak self-energy of tau, mu, b, c (general R_xi; in parallel, ~2 min)
#   2. hff_weak.wl              : UV finiteness, tadpoles, delta_weak at three gauges and three scales, the MadLoop point (~1 min)
#   3. hff_weak_madloop.py      : MadLoop's [virt=QED] H -> tau tau, mu mu, b bbar with the CKM note's NLO UFO (~5 min, the model
#                                 import; skipped with --no-madloop)
#   4. hff_widths.py            : the widths with QCD, QED and the weak correction at mu = M_H/2, M_H, 2 M_H
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
mkdir -p work results
for f in generated/SM_CKM_FA results/hqq_massive.csv results/hqq_massive_virtual_ml.csv; do
  [ -e "$f" ] || { echo "$f missing: run run_lo_check.sh and run_hqq_massive_check.sh first"; exit 1; }
done
wolframscript -file hff_weak_feyncalc.wl 2 3 > work/hff_23.log 2>&1 &
wolframscript -file hff_weak_feyncalc.wl 2 2 > work/hff_22.log 2>&1 &
wolframscript -file hff_weak_feyncalc.wl 4 3 > work/hff_43.log 2>&1 &
wolframscript -file hff_weak_feyncalc.wl 3 2 > work/hff_32.log 2>&1 &
wait
for f in 23 22 43 32; do grep -E "^fermion|vertex:|self-energy|WARNING" work/hff_$f.log | cut -c1-200; done
wolframscript -file hff_weak.wl > work/hff_weak.log 2>&1 || { echo "hff_weak.wl failed"; exit 1; }
grep -E "^\(|^   " work/hff_weak.log | cut -c1-250
if [ "$1" != "--no-madloop" ]; then
  python3 hff_weak_madloop.py --prepare
  (cd work/ml_hffweak && "$HOME/hep/bin/mg5_aMC" run.mg5 < /dev/null > run.log 2>&1) || { echo "mg5_aMC (MadLoop) failed"; exit 1; }
  python3 hff_weak_madloop.py
fi
python3 hff_widths.py
