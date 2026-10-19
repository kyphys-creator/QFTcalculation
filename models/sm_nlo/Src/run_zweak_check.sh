#!/bin/bash
# Step (4a) of the NLO note: the weak correction to Z -> f fbar and the Z-pole observables at NLO.
#   1. zff_feyncalc.wl t g  : the weak 1PI vertex and the weak self-energy of the eleven fermions (FeynCalc, general R_xi; no
#                             photon, no gluon), six at a time                                                       (~6 min)
#   2. zweak.wl             : the S-matrix element (LSZ factors, Z-photon mixing, MS-bar counterterms): UV finiteness, gauge
#                             independence, delta_weak at mu = M_Z/2, M_Z, 2 M_Z and at the CKM note's MadLoop point     (~2 min)
#   3. zweak_madloop.py     : MadLoop's [virt=QED] with the CKM note's NLO UFO against delta_weak plus the photonic part
#                             (~6 min, mostly the model import; skipped with --no-madloop)
#   4. zweak_widths.py      : the Z widths and the Z-pole observables with the QED and QCD K of steps (2), (3)
# Needs steps (1)-(3) first (run_lo_check.sh, run_ir_check.sh, run_massive_check.sh: results/lo_widths.csv,
# results/ir_massive.csv, results/ir_massive_virtual_ml.csv) and the CKM note's NLO UFO.
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
mkdir -p work results
for f in generated/SM_CKM_FA results/lo_widths.csv results/ir_massive.csv results/ir_massive_virtual_ml.csv; do
  [ -e "$f" ] || { echo "$f missing: run the checks of steps (1)-(3) first"; exit 1; }
done
printf "1 1\n1 2\n1 3\n2 1\n2 2\n2 3\n3 1\n3 2\n4 1\n4 2\n4 3\n" | xargs -P 6 -L 1 sh -c \
  'wolframscript -file zff_feyncalc.wl $0 $1 > work/zff_$0$1.log 2>&1 || echo "zff_feyncalc.wl $0 $1 failed"'
for f in work/zff_*.log; do grep -E "^tree|UV poles|SSL - SSR" "$f" | sed "s|^|$(basename "$f" .log): |" | cut -c1-200; done
wolframscript -file zweak.wl > work/zweak.log 2>&1 || { echo "zweak.wl failed"; exit 1; }
grep -E "^\(a\)|without|Born sum|delta_weak at|^\(d\)" work/zweak.log | sed -E 's/`[0-9.]+//g' | cut -c1-250
if [ "$1" != "--no-madloop" ]; then
  python3 zweak_madloop.py --prepare
  (cd work/ml_zweak && "$HOME/hep/bin/mg5_aMC" run.mg5 < /dev/null > run.log 2>&1) || { echo "mg5_aMC (MadLoop) failed"; exit 1; }
  python3 zweak_madloop.py
fi
python3 zweak_widths.py
