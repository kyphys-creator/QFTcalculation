#!/bin/bash
# Tree-level check (research note models/spinor_qed, step (2)).
#   1. FeynArts + FeynCalc amplitudes and spin sums vs Eq. (11) (eq:Mtree) and Eq. (12) (eq:sumtree), symbolically;
#      xi independence of (A), (B), Ward identity of (C), (D)                                     (tree_feyncalc.wl)
#   2. MadGraph cross sections of (A)-(D) at sqrt(s) = 4, 6, 10, of (C) with |cos theta_e| < 0.98, and the
#      standalone matrix element of (C) at fixed points                                             (tree_mg5.mg5,
#                                                                                                    tree_me_points.f)
#   3. explicit spinors and polarization vectors, gauge checks, cross sections, comparison         (tree_sigma.py)
# Needs Src/generated/ (run generate_SpinorQED.wl first).  MadGraph output goes to Src/work/.
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
mkdir -p work

echo "=== FeynCalc"
wolframscript -file tree_feyncalc.wl 2>&1 | grep -E '^\((A|B|C|D)\)'

echo "=== MadGraph"
rm -rf work/mg5_treeA work/mg5_treeB work/mg5_treeC work/mg5_treeD work/sa_treeC work/SpinorQED_UFO
cp -R generated/SpinorQED_UFO work/SpinorQED_UFO   # MadGraph rewrites the UFO it imports
mg5_aMC tree_mg5.mg5 > work/tree_mg5.log 2>&1
rm -f py.py MG5_debug nsqso_born.inc ../nsqso_born.inc   # output standalone writes nsqso_born.inc here and in ..
grep -E '^\s+Cross-section' work/tree_mg5.log
( cd work/sa_treeC/SubProcesses/P1_ema_ema && make check > /dev/null 2>&1 && \
  gfortran -O2 -ffixed-line-length-132 -o me_points ../../../../tree_me_points.f matrix.o \
    ../../lib/libdhelas.a ../../lib/libmodel.a -I. )

echo "=== comparison"
"$HOME/miniforge3/envs/qft/bin/python" tree_sigma.py work/tree_mg5.log
