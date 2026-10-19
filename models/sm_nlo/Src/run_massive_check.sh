#!/bin/bash
# Step (3) of the NLO note: the cancellation of the infrared poles and the inclusive corrections for massive emitters
# (Z -> b bbar, c cbar, tau tau, mu mu with the V and A currents separately; t -> b W+).
#   1. ir_massive_virtual.wl : the virtual correction (FeynCalc TID, Package-X; the on-shell field constants computed the same way)
#                              and the soft emission (the eikonal factor in d dimensions, E_g < delta E_max)          (~25 s)
#   2. ir_massive_real.wl    : the d = 4 real |M|^2 (against the FeynArts model and the eikonal limit), the hard integrals
#                              (Gauss-Legendre in logarithmic variables), K for delta = 1e-4 ... 1e-8 and delta -> 0   (~20 s)
#   3. ir_massive_mg5.py     : MadGraph's tree |M|^2 of Z -> b bbar g, Z -> tau tau gamma, t -> b W+ g at Dalitz points  (~20 s)
#   4. ir_massive_madloop.py : MadLoop's [virt=QCD] Z -> b bbar, t -> b W+ with the CKM note's NLO UFO (~5 min, mostly the model
#                              import; skipped with --no-madloop)
#   5. ir_massive_widths.py  : the corrections with the masses on the LO widths of step (1)
# Needs step (1) first (run_lo_check.sh: generated/SM_CKM_FA, work/SM_CKM_UFO, work/card_Z.dat, results/lo_widths.csv), step (2)
# (results/ir_inclusive.csv) and the CKM note's NLO UFO (models/sm_ckm/Src/generated/SM_CKM_NLO_UFO).
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
mkdir -p work results
for f in generated/SM_CKM_FA work/SM_CKM_UFO work/card_Z.dat results/lo_widths.csv results/ir_inclusive.csv; do
  [ -e "$f" ] || { echo "$f missing: run run_lo_check.sh and run_ir_check.sh first"; exit 1; }
done
wolframscript -file ir_massive_virtual.wl > work/ir_massive_virtual.log 2>&1 || { echo "ir_massive_virtual.wl failed"; exit 1; }
grep -E "expect|MadLoop point" work/ir_massive_virtual.log | cut -c1-250
wolframscript -file ir_massive_real.wl > work/ir_massive_real.log 2>&1 || { echo "ir_massive_real.wl failed"; exit 1; }
grep -E "expect|^R/|^(Z|t)_|extrapolated|limit|threshold" work/ir_massive_real.log | cut -c1-400
python3 ir_massive_mg5.py --prepare
rm -rf work/me_massive
(cd work/mg5run_massive && "$HOME/hep/bin/mg5_aMC" ir_massive_mg5.mg5 > ir_massive_mg5.log 2>&1) || { echo "mg5_aMC failed"; exit 1; }
python3 ir_massive_mg5.py | tail -2
if [ "$1" != "--no-madloop" ]; then
  python3 ir_massive_madloop.py --prepare
  (cd work/ml_massive && "$HOME/hep/bin/mg5_aMC" run.mg5 < /dev/null > run.log 2>&1) || { echo "mg5_aMC (MadLoop) failed"; exit 1; }
  python3 ir_massive_madloop.py
fi
python3 ir_massive_widths.py
