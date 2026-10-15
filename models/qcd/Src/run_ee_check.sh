#!/bin/bash
# e+ e- -> hadrons at O(alpha_s) (research note models/qcd, step (8)).
#   1. FeynCalc: -g H of q qbar and q qbar g in D dimensions, the real correction (Dirichlet integrals, exact in eps), the virtual
#      vertex (FeynArts, general xi; B0, C0 exact against Package-X and LoopTools), R/R_0 = 1 + 3 C_F a; the thrust distribution
#      -> results/ee_feyncalc.csv                                                                    (ee_feyncalc.wl)
#   2. the optical theorem: one- and two-loop photon self-energies (u and t), shifts onto the families, Kira; the massless
#      Delta^(1) = 3/4 exactly -> results/ee_optical_reduction.m                                      (ee_optical.wl)
#   3. AMFlow: the t masters at beta = 0.1, ..., 0.9, the on-shell mass counterterm, Delta^(1)(beta) against the closed form
#      -> results/ee_amflow.csv                                                                      (ee_amflow.wl, ~9 min)
#   4. MadGraph5_aMC@NLO: e+ e- > u u~ [QCD], e+ e- > t t~ [QCD] (4 seeds per point), MadEvent e+ e- > u u~ g (T < 0.99)
#      -> results/ee_mg5.csv, work/ee_mg5_thrust.txt                                                  (ee_mg5.py, ~15 min)
#   5. K-factors, thrust histogram, figure -> results/ee_comparison.csv, ../figs/ee_rratio.pdf         (ee_numeric.py)
# Needs Src/generated/ (run_model_check.sh, generate_QCD_NLO.sh).  About 25 minutes.
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
PY="$HOME/miniforge3/envs/qft/bin/python"
mkdir -p work results

echo "=== FeynCalc: real and virtual in D dimensions, thrust"
wolframscript -file ee_feyncalc.wl 2>&1 | grep -E '^\((a|b|c|d|e)\)' | cut -c1-400

echo "=== optical theorem: photon self-energies, Kira"
wolframscript -file ee_optical.wl 2>&1 | grep -E '^\((a|b|c|d)\)' | cut -c1-400

echo "=== AMFlow: heavy quark"
wolframscript -file ee_amflow.wl 2>&1 | grep -E '^\((a|b|c)\)' | cut -c1-400

echo "=== MadGraph5_aMC@NLO"
"$PY" ee_mg5.py

echo "=== comparison"
"$PY" ee_numeric.py 2>&1 | grep -v -i "warning"
