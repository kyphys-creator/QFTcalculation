#!/bin/bash
# Research note models/sm_pp, step (3): MC@NLO with Pythia 8 against the note's own calculations.
#   (3a) mc_hadronic.py: the own LO V + jet and H + jet p_T spectra against the p_T > 0 bins of the fixed-order NLO runs of steps
#        (1) and (2) (work/dy/z/Events/zpeak_NLO*, work/gh/ppo/Events/o_NLO: run_dy_check.sh and run_gh_check.sh first);
#   (3b) mc_mg5.sh: MC@NLO + Pythia 8 for the Z and the H (200000 events each, about 5 minutes on 10 cores; each shower job takes
#        about 0.4 GB), then mc_hadronic.py: the totals, the rapidity and p_T of the boson (results/mc_hadronic.csv).
# With --reuse, mc_mg5.sh runs nothing that has its showered HwU.
cd "$(dirname "$0")"
mkdir -p work
REUSE=""; for a in "$@"; do [ "$a" = "--reuse" ] && REUSE="--reuse"; done
./mc_mg5.sh $REUSE || exit 1
~/hep/opt/lhc/bin/python mc_hadronic.py
