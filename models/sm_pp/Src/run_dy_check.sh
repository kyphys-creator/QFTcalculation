#!/bin/bash
# Research note models/sm_pp, step (1): Drell-Yan at NLO in QCD.
#   (1a) dy_feyncalc.wl: the D-dimensional real emission and virtual correction, the MS-bar coefficient functions, the 4-dimensional
#        squared amplitudes against the note's FeynArts model (results/dy_feyncalc.csv; about 15 seconds);
#   (1b) dy_mg5.sh: aMC@NLO at fixed order, LO and NLO, p p -> e+ e-, e+ ve, e- ve~ [QCD] (work/dy; about 3 hours on 10 cores);
#   (1c) dy_hadronic.py: the own convolutions with NNPDF4.0 NLO against (1b) (results/dy_hadronic.csv; about 25 minutes);
#   (1d) dy_ckm.py: the W totals with the PDG CKM matrix instead of V = 1, for the comparison with ATLAS (results/dy_ckm.csv).
# With --reuse, (1b) runs nothing that has its MADatNLO.HwU.
cd "$(dirname "$0")"
wolframscript -file dy_feyncalc.wl > work/dy_feyncalc.log 2>&1 || { echo "dy_feyncalc.wl failed: work/dy_feyncalc.log"; exit 1; }
grep "^(a)\|^(b) v\|^(c) IBP\|^(c) F\|^(c) minus\|^(d)\|^(e)" work/dy_feyncalc.log
./dy_mg5.sh "$@" || exit 1
~/hep/opt/lhc/bin/python dy_hadronic.py
~/hep/opt/lhc/bin/python dy_ckm.py
