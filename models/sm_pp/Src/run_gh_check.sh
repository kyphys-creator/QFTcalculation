#!/bin/bash
# Research note models/sm_pp, step (2): g g -> H at NLO in QCD in the heavy-top effective theory.
#   (2a) gh_feyncalc.wl: the D-dimensional real emission, virtual correction and counterterms, the MS-bar coefficient functions against
#        the literature, MadLoop's normalization of the virtual (results/gh_feyncalc.csv; about 40 seconds);
#   (2b) gh_generate_nlo.sh: the attempt at an own NLO UFO with NLOCT (QCDH.fr; its H vertices come out with unevaluated integrals,
#        so it is not used; about 15 minutes; only with --nloct);
#   (2c) gh_madloop.py, gh_tree.py: HC_NLO_X0's virtual correction (MadLoop) and real-emission tree matrix elements against (2a)
#        (needs ~/hep/src/smpp2-dl/extracted/HC_NLO_X0_UFO; the work copy gets the note's pole patch);
#   (2d) gh_mg5.sh: aMC@NLO at fixed order, p p > x0 / t [QCD], LO and NLO (work/gh/pph; about 1 hour on 10 cores);
#   (2e) gh_hadronic.py: the own convolutions with NNPDF4.0 NLO against (2d) (results/gh_hadronic.csv).
# With --reuse, (2d) runs nothing that has its MADatNLO.HwU.
cd "$(dirname "$0")"
mkdir -p work
wolframscript -file gh_feyncalc.wl > work/gh_feyncalc.log 2>&1 || { echo "gh_feyncalc.wl failed: work/gh_feyncalc.log"; exit 1; }
grep "^(a)\|^(b) diagrams\|^(b) 4-dim\|^(c) H_gg\|^(d) PaVe left\|^(e) poles\|^(e) d/d\|^(e) z Delta\|^(f)" work/gh_feyncalc.log
for a in "$@"; do [ "$a" = "--nloct" ] && ./gh_generate_nlo.sh; done
REUSE=""; for a in "$@"; do [ "$a" = "--reuse" ] && REUSE="--reuse"; done
~/hep/opt/lhc/bin/python gh_madloop.py $([ -z "$REUSE" ] && echo --fresh) || exit 1
~/hep/opt/lhc/bin/python gh_tree.py || exit 1
./gh_mg5.sh $REUSE || exit 1
~/hep/opt/lhc/bin/python gh_hadronic.py
