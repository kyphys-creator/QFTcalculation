#!/bin/bash
# Step (4) of the Higgs note: H -> b bbar, c cbar, tau tau, mu mu at NLO QCD and QED with the masses
# (after run_lo_check.sh: generated/SM_CKM_FA, work/SM_CKM_UFO, work/card_H.dat; and run_hqq_check.sh: results/hqq_widths.csv).
#   1. hqq_massive_virtual.wl : the virtual correction (MS-bar and on-shell Yukawa counterterms) and the soft emission    (~20 s)
#   2. hqq_massive_real.wl    : the d = 4 real |M|^2 (FeynArts model, eikonal limit), the hard integrals, K_OS against
#                               Drees-Hikasa's Delta_H, the massless and threshold limits                                  (~10 s)
#   3. hqq_massive_mg5.py     : MadGraph's tree |M|^2 of H -> b bbar g, tau tau gamma at Dalitz points                    (~20 s)
#   4. hqq_massive_madloop.py : MadLoop's [virt=QCD] H -> b bbar with the CKM note's NLO UFO (~5 min, the model import;
#                               skipped with --no-madloop)
#   5. hqq_massive_widths.py  : the widths with the masses, MS-bar and pole Yukawa couplings, mu = M_H/2, M_H, 2 M_H
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
mkdir -p work results
for f in generated/SM_CKM_FA work/SM_CKM_UFO work/card_H.dat results/hqq_widths.csv; do
  [ -e "$f" ] || { echo "$f missing: run run_lo_check.sh and run_hqq_check.sh first"; exit 1; }
done
wolframscript -file hqq_massive_virtual.wl > work/hqq_massive_virtual.log 2>&1 || { echo "hqq_massive_virtual.wl failed"; exit 1; }
grep -E "expect|MadLoop point" work/hqq_massive_virtual.log | cut -c1-250
wolframscript -file hqq_massive_real.wl > work/hqq_massive_real.log 2>&1 || { echo "hqq_massive_real.wl failed"; exit 1; }
grep -E "expect|^  H_|massless|threshold" work/hqq_massive_real.log | cut -c1-300
python3 hqq_massive_mg5.py --prepare
rm -rf work/me_hqq
(cd work/mg5run_hqq && "$HOME/hep/bin/mg5_aMC" hqq_massive_mg5.mg5 > hqq_massive_mg5.log 2>&1) || { echo "mg5_aMC failed"; exit 1; }
python3 hqq_massive_mg5.py | tail -2
if [ "$1" != "--no-madloop" ]; then
  python3 hqq_massive_madloop.py --prepare
  (cd work/ml_hqq && "$HOME/hep/bin/mg5_aMC" run.mg5 < /dev/null > run.log 2>&1) || { echo "mg5_aMC (MadLoop) failed"; exit 1; }
  python3 hqq_massive_madloop.py
fi
python3 hqq_massive_widths.py
