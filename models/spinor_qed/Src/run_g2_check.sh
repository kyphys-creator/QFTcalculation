#!/bin/bash
# The anomalous magnetic moment (research note models/spinor_qed, step (8)).
#   1. the quadrature nodes of the x-representation for the seven mass ratios -> work/g2_nodes.txt  (g2_numeric.py --nodes)
#   2. FeynArts + FeynCalc: the vertex of e and mu (general xi) projected on F1, F2 (D-dimensional traces), against the PaVe forms
#      of the note, F2(0) = alpha/(2 pi) with Package-X; the subtracted vacuum polarization at the nodes (Package-X 30 digits,
#      LoopTools), K F2(q^2)/e^2 at the points of step (3) -> results/g2_feyncalc_pibar.csv, results/g2_feyncalc_f2.csv
#                                                                                                      (g2_feyncalc.wl)
#   3. COLLIER: the same Pibar and F2 (built here, run by g2_numeric.py)                               (g2_collier.f90)
#   4. F2 against the Feynman-parameter integral, the two-loop vacuum-polarization coefficient A(r) from the x-representation
#      (five evaluations of Pibar), the double integral, Passera's closed form, the asymptotics and literature values; a_mu
#      and a_e; figure -> results/g2.csv, ../figs/g2_vp.pdf                                            (g2_numeric.py)
# Needs Src/generated/ (run_model_check.sh).  wolframscript may print "libc++abi: ... MathLink::MLException" when LoopTools is
# unloaded at the end; the results are written before that.
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
PY="$HOME/miniforge3/envs/qft/bin/python"
mkdir -p work results

echo "=== nodes"
"$PY" g2_numeric.py --nodes

echo "=== FeynCalc / Package-X / LoopTools (about 20 s)"
wolframscript -file g2_feyncalc.wl 2>&1 | grep -E '^\((a|b|c)\)'

echo "=== COLLIER"
gfortran -I"$HOME/hep/include" g2_collier.f90 -L"$HOME/hep/lib" -lcollier -o work/g2_collier && echo "built work/g2_collier"

echo "=== comparison, A(r), figure"
"$PY" g2_numeric.py
