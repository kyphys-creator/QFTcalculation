#!/bin/bash
# Step (4c) of the NLO note: the electroweak correction to t -> d_j W+ (virtual, soft and hard photon) and the top width at NLO.
#   1. zff_feyncalc.wl 3 3   : the weak self-energy of the top (with the unphysical Z -> t tbar vertex of step (4a)), and
#      tff_feyncalc.wl j     : the electroweak 1PI vertex of t -> d_j W+ (no gluon), the four at a time                  (~6 min)
#   2. tweak.wl              : the S-matrix element (LSZ factors, MS-bar counterterms, dV): gauge independence, the infrared
#                              pole against the soft photon of the three charges; virtual + soft at mu = m_t/2, m_t, 2 m_t and
#                              at m_b/3, m_b/10; the virtual alone at the CKM note's MadLoop point                             (~3 min)
#   3. tweak_madloop.py      : MadLoop's [virt=QED] with the CKM note's NLO UFO against that virtual
#                              (~6 min, mostly the model import; skipped with --no-madloop)
#   4. treal.wl              : the tree t -> d_j W+ gamma (Ward identity, soft limit), the hard photon, delta_EW, its independence
#                              of the cut and of m_b                                                                          (~1 min)
#   5. treal_mg5.py          : MadGraph's tree |M|^2 of t -> b W+ gamma against the hand form (~1 min; skipped with --no-madloop)
#   6. tweak_widths.py       : the top width with the QCD factor of step (3)
# Needs steps (1)-(4b) first (run_lo_check.sh, run_ir_check.sh, run_massive_check.sh, run_zweak_check.sh, run_wweak_check.sh:
# work/card_t.dat, results/lo_widths.csv, results/ir_massive.csv, work/zff_4*.m, work/wsig.m), the CKM note's self-energies and its
# NLO UFO.
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
mkdir -p work results
for f in generated/SM_CKM_FA work/SM_CKM_UFO work/card_t.dat results/lo_widths.csv results/ir_massive.csv work/zff_41.m work/zff_43.m \
  work/wsig.m ../../sm_ckm/Src/results/oneloop_ckm_sigma.m; do
  [ -e "$f" ] || { echo "$f missing: run the checks of steps (1)-(4b) first"; exit 1; }
done
printf "zff_feyncalc.wl 3 3\ntff_feyncalc.wl 1\ntff_feyncalc.wl 2\ntff_feyncalc.wl 3\n" | xargs -P 4 -L 1 sh -c \
  'n=$(echo "$@" | sed "s/_feyncalc.wl//; s/ //g"); wolframscript -file "$@" > work/$n.log 2>&1 || echo "$@ failed"' sh
for f in work/zff33.log work/tff1.log work/tff2.log work/tff3.log; do
  grep -E "^tree|UV poles|SSL - SSR" "$f" | sed -E 's/normalization.*(UV poles|vertex reduced)/\1/; s/;  gauge parameters.*//' | sed "s|^|$(basename "$f" .log): |" | cut -c1-200
done
wolframscript -file tweak.wl > work/tweak.log 2>&1 || { echo "tweak.wl failed"; exit 1; }
grep -E "WARNING|mu = 172|_mb|^\(d\)" work/tweak.log | sed -E 's/NumberForm\[([^,]+), 12\]/\1/g; s/ScientificForm\[([^,]+), [0-9]\]/\1/g; s/`[0-9.]+//g' | cut -c1-250
if [ "$1" != "--no-madloop" ]; then
  python3 tweak_madloop.py --prepare
  (cd work/ml_tweak && "$HOME/hep/bin/mg5_aMC" run.mg5 < /dev/null > run.log 2>&1) || { echo "mg5_aMC (MadLoop) failed"; exit 1; }
  python3 tweak_madloop.py
fi
wolframscript -file treal.wl > work/treal.log 2>&1 || { echo "treal.wl failed"; exit 1; }
grep -E "Ward|R/eik|mu = 172|^\(c\)|K_H\(" work/treal.log | cut -c1-250
if [ "$1" != "--no-madloop" ]; then
  python3 treal_mg5.py --prepare
  (cd work/mg5run_treal && "$HOME/hep/bin/mg5_aMC" treal_mg5.mg5 < /dev/null > mg5.log 2>&1) || { echo "mg5_aMC failed"; exit 1; }
  python3 treal_mg5.py | grep -E "largest|wrote"
fi
python3 tweak_widths.py
