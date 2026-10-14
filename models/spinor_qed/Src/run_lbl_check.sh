#!/bin/bash
# Photon-photon scattering (research note models/spinor_qed, step (10)).
#   1. the points: check points, low- and high-energy points, forward points, the nodes of the cross sections
#      -> work/lbl_points_exact.txt, work/lbl_points.txt, work/lbl_ml_points.input              (lbl_numeric.py --points)
#   2. FeynArts + FeynCalc: the six boxes; zero momenta in D dimensions and with a four-dimensional numerator (R2); the
#      low-energy expansion against Euler-Heisenberg and its O(k^6) terms; TID, the UV pole at general momenta, X at the
#      points from Package-X and LoopTools -> results/lbl_feyncalc.csv                                    (lbl_feyncalc.wl)
#   3. FeynArts 3.12 + FormCalc 9.10 + LoopTools: X at the points -> results/lbl_formcalc.csv          (lbl_formcalc.wl)
#   4. COLLIER: explicit Dirac matrices, four-dimensional numerator plus R2 (built here, run by lbl_numeric.py; its values
#      at all points go to work/lbl_collier.csv)
#                                                                                                        (lbl_collier.f90)
#   5. MadGraph: MadLoop per helicity at the check points (lbl_madloop_driver.f) and MadEvent cross sections
#                                                                                         (lbl_mg5.mg5, lbl_me_launch.mg5)
#   6. comparison, low- and high-energy limits, optical theorem and dispersion relation, cross section, figure
#      -> results/lbl.csv, ../figs/lbl.pdf                                                                  (lbl_numeric.py)
# Needs Src/generated/ (run_model_check.sh, generate_SpinorQED_NLO.sh).  wolframscript may print "libc++abi: ...
# MathLink::MLException" when LoopTools is unloaded at the end; the results are written before that.
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
PY="$HOME/miniforge3/envs/qft/bin/python"
mkdir -p work results

echo "=== points"
"$PY" lbl_numeric.py --points

echo "=== FeynCalc / Package-X / LoopTools (about 10 min)"
wolframscript -file lbl_feyncalc.wl 2>&1 | grep -E '^\((a|b|c|d)\)'

echo "=== FormCalc / LoopTools"
wolframscript -file lbl_formcalc.wl 2>&1 | grep -E '^\((a|b)\)'

echo "=== COLLIER"
gfortran -O2 -I"$HOME/hep/include" lbl_collier.f90 -L"$HOME/hep/lib" -lcollier -o work/lbl_collier && echo "built work/lbl_collier"

echo "=== MadGraph: MadLoop standalone and MadEvent output"
rm -rf work/SpinorQED_NLO_MS_UFO work/ml_lbl work/me_lbl
cp -R generated/SpinorQED_NLO_MS_UFO work/SpinorQED_NLO_MS_UFO   # MadGraph rewrites the UFO it imports
mg5_aMC lbl_mg5.mg5 > work/lbl_mg5.log 2>&1
rm -f py.py MG5_debug nsqso_born.inc ../nsqso_born.inc
grep -E 'Contributing diagrams' work/lbl_mg5.log
P=$(ls -d work/ml_lbl/SubProcesses/P0_* | head -1)
cp lbl_madloop_driver.f "$P/check_sa.f"
(cd "$P" && make check > make.log 2>&1 && echo "compiled $P/check") || { echo "compilation failed, see $P/make.log"; exit 1; }
for card in param_card.dat param_card_default.dat; do
  printf '\nBlock loop\n    1 1.000000e+00 # MU_R\n' >> work/me_lbl/Cards/$card
done

echo "=== MadEvent cross sections (12 runs, about 15 min)"
mg5_aMC lbl_me_launch.mg5 > work/lbl_me_launch.log 2>&1
rm -f py.py MG5_debug ME5_debug
grep -E '^\s+Cross-section' work/lbl_me_launch.log

echo "=== comparison, limits, optical theorem, cross section, figure"
"$PY" lbl_numeric.py
