#!/bin/bash
# Two-loop beta function of QCD from the Landau-gauge gluon and ghost self-energies (research note models/qcd, step (7)).
#   1. FeynArts + FeynCalc: the 23 gluon and 7 ghost two-loop diagrams, the one-loop calibration against Eq. (V), the algebra and the
#      shifts onto the family k2, IBP reduction with Kira 3.1 and FIRE 7.1 (compared), transversality at two loops
#      -> results/twoloop_reduction.m                                                         (twoloop_feyncalc.wl)
#   2. the masters exactly and with AMFlow 2.0; Z_3, Z~_3 to two loops, the RG double poles, beta_1, the anomalous dimensions, the
#      renormalized finite parts -> results/twoloop_z.csv, results/twoloop_masters.csv          (twoloop_eval.wl)
#   3. pySecDec for the masters; two-loop running of alpha_s (exact, numerical, MadGraph nloop = 2), Lambda at one and two loops
#      -> results/twoloop_numeric.csv, ../figs/twoloop_running.pdf                              (twoloop_numeric.py, alfas_mg5.f)
# Needs Src/generated/ (run_model_check.sh) and the two-loop tools of environment.pdf (Sec. 8).  About 7 minutes.
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
PY="$HOME/miniforge3/envs/qft/bin/python"
MG5SRC="$HOME/hep/MG5_aMC_v3_8_1/Template/LO/Source"
mkdir -p work results

echo "=== FeynArts + FeynCalc, Kira, FIRE"
wolframscript -file twoloop_feyncalc.wl 2>&1 | grep -E '^\((a|b|c|d|e)\)' | cut -c1-400

echo "=== masters (exact, AMFlow), Z_3, Z~_3, beta_1"
wolframscript -file twoloop_eval.wl 2>&1 | grep -E '^\((a|b|c)\)' | cut -c1-600

echo "=== pySecDec, two-loop running, Lambda"
gfortran -ffixed-line-length-132 -I"$MG5SRC" alfas_mg5.f "$MG5SRC/alfas_functions.f" -o work/alfas_mg5 && echo "built work/alfas_mg5"
"$PY" twoloop_numeric.py 2>&1 | grep -v -i "warning"
