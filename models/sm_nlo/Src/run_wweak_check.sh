#!/bin/bash
# Step (4b) of the NLO note: the electroweak correction to W+ -> f fbar' (virtual, soft and hard photon) and the W widths at NLO.
#   1. wsig_feyncalc.wl      : the W self-energy with the massless photon (FeynCalc, general R_xi), against the SM note's   (~20 s)
#   2. wff_feyncalc.wl t i j : the electroweak 1PI vertex of the nine channels (no gluon), six at a time                  (~11 min)
#   3. wweak.wl              : the S-matrix element (LSZ factors, MS-bar counterterms, dV): UV finiteness, gauge independence,
#                              the infrared pole against the soft photon; virtual + soft at mu = M_W/2, M_W, 2 M_W, and the
#                              virtual alone at the CKM note's MadLoop point                                                 (~6 min)
#   4. wweak_madloop.py      : MadLoop's [virt=QED] with the CKM note's NLO UFO against that virtual
#                              (~6 min, mostly the model import; skipped with --no-madloop)
#   5. wreal.wl              : the tree W+ -> f fbar' gamma (Ward identity, soft limit), the hard photon, delta_EW and its
#                              independence of the cut                                                                       (~1 min)
#   6. wreal_mg5.py          : MadGraph's tree |M|^2 of W+ -> f fbar' gamma against the hand form (~1 min; skipped with --no-madloop)
#   7. wweak_widths.py       : the W widths and branching ratios with the QCD factor alpha_s/pi
# Needs steps (1)-(4a) first (run_lo_check.sh, run_ir_check.sh, run_massive_check.sh, run_zweak_check.sh: generated/SM_CKM_FA,
# work/SM_CKM_UFO, work/card_W.dat, results/lo_widths.csv, work/zff_*.m), the CKM note's self-energies
# (models/sm_ckm/Src/results/oneloop_ckm_sigma.m) and its NLO UFO.
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
mkdir -p work results
for f in generated/SM_CKM_FA work/SM_CKM_UFO work/card_W.dat results/lo_widths.csv work/zff_11.m work/zff_43.m \
  ../../sm_ckm/Src/results/oneloop_ckm_sigma.m; do
  [ -e "$f" ] || { echo "$f missing: run the checks of steps (1)-(4a) first"; exit 1; }
done
wolframscript -file wsig_feyncalc.wl > work/wsig.log 2>&1 || { echo "wsig_feyncalc.wl failed"; exit 1; }
grep -E "^W self-energy|^\(i\)" work/wsig.log | cut -c1-200
printf "1 1\n1 2\n1 3\n3 1 1\n3 1 2\n3 1 3\n3 2 1\n3 2 2\n3 2 3\n" | xargs -P 6 -L 1 sh -c \
  'n=$(echo "$@" | tr -d " "); wolframscript -file wff_feyncalc.wl "$@" > work/wff_$n.log 2>&1 || echo "wff_feyncalc.wl $@ failed"' sh
for f in work/wff_*.log; do grep -E "^tree" "$f" | sed -E 's/normalization.*UV poles/UV poles/; s/;  gauge parameters.*//' | sed "s|^|$(basename "$f" .log): |" | cut -c1-200; done
wolframscript -file wweak.wl > work/wweak.log 2>&1 || { echo "wweak.wl failed"; exit 1; }
grep -E "UV|WARNING|mu = 80|^\(d\)" work/wweak.log | sed -E 's/NumberForm\[([^,]+), 12\]/\1/g; s/ScientificForm\[([^,]+), [0-9]\]/\1/g; s/`[0-9.]+//g' | cut -c1-250
if [ "$1" != "--no-madloop" ]; then
  python3 wweak_madloop.py --prepare
  (cd work/ml_wweak && "$HOME/hep/bin/mg5_aMC" run.mg5 < /dev/null > run.log 2>&1) || { echo "mg5_aMC (MadLoop) failed"; exit 1; }
  python3 wweak_madloop.py
fi
wolframscript -file wreal.wl > work/wreal.log 2>&1 || { echo "wreal.wl failed"; exit 1; }
grep -E "Ward|R/eik|mu = 80" work/wreal.log | cut -c1-250
if [ "$1" != "--no-madloop" ]; then
  python3 wreal_mg5.py --prepare
  (cd work/mg5run_wreal && "$HOME/hep/bin/mg5_aMC" wreal_mg5.mg5 < /dev/null > mg5.log 2>&1) || { echo "mg5_aMC failed"; exit 1; }
  python3 wreal_mg5.py | grep -E "largest|wrote"
fi
python3 wweak_widths.py
