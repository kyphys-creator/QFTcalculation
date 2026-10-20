#!/bin/bash
# Research note models/sm_pp, step (2): g g -> H at NLO in QCD in the heavy-top effective theory.
#   (2a) gh_feyncalc.wl: the D-dimensional real emission, virtual correction and counterterms, the MS-bar coefficient functions against
#        the literature, MadLoop's normalization of the virtual (results/gh_feyncalc.csv; about 40 seconds);
#   (2b) gh_generate_nlo.sh: NLOCT's counterterms of QCDH.fr (its H vertices come out with unevaluated integrals; about 15 minutes;
#        only with --nloct; otherwise only its last step, gh_nlo_ufo.wl, runs on the stored generated/QCDH_CT.nlo);
#   (2c) gh_madloop.py, gh_tree.py: HC_NLO_X0's virtual correction (MadLoop) and real-emission tree matrix elements against (2a)
#        (needs ~/hep/src/smpp2-dl/extracted/HC_NLO_X0_UFO; the work copy gets the note's pole patch);
#   (2d) gh_mg5.sh: aMC@NLO at fixed order, p p > x0 / t [QCD], LO and NLO (work/gh/pph; about 1 hour on 10 cores);
#   (2e) gh_hadronic.py: the own convolutions with NNPDF4.0 NLO against (2d) and (2f) (results/gh_hadronic.csv);
#   (2f) the own NLO UFO: gh_r2.wl (the g g H R2 vertex and UV counterterm, results/gh_r2.csv, generated/QCDH_H_CT.m; about 40 s),
#        gh_nlo_ufo.wl (generated/QCDH_NLO_UFO with them in place of NLOCT's H vertices; about 20 s), gh_own_madloop.py (MadLoop
#        against (2a)), gh_own_mg5.sh (aMC@NLO p p > h [QCD] with it, work/gh/ppo; about 10 minutes on 10 cores).
# With --reuse, (2d) runs nothing that has its MADatNLO.HwU.
cd "$(dirname "$0")"
mkdir -p work
wolframscript -file gh_feyncalc.wl > work/gh_feyncalc.log 2>&1 || { echo "gh_feyncalc.wl failed: work/gh_feyncalc.log"; exit 1; }
grep "^(a)\|^(b) diagrams\|^(b) 4-dim\|^(c) H_gg\|^(d) PaVe left\|^(e) poles\|^(e) d/d\|^(e) z Delta\|^(f)" work/gh_feyncalc.log
wolframscript -file gh_r2.wl > work/gh_r2.log 2>&1 || { echo "gh_r2.wl failed: work/gh_r2.log"; exit 1; }
grep "^(a)\|^(c) own\|^(d) own" work/gh_r2.log
NLOCT=0; for a in "$@"; do [ "$a" = "--nloct" ] && NLOCT=1; done
if [ "$NLOCT" = 1 ]; then
  ./gh_generate_nlo.sh || exit 1
else
  wolframscript -file gh_nlo_ufo.wl > work/gh_nlo_ufo.log 2>&1 || { echo "gh_nlo_ufo.wl failed: work/gh_nlo_ufo.log"; exit 1; }
  grep -E '^(tree|Integrate|written)' work/gh_nlo_ufo.log
fi
REUSE=""; for a in "$@"; do [ "$a" = "--reuse" ] && REUSE="--reuse"; done
~/hep/opt/lhc/bin/python gh_madloop.py $([ -z "$REUSE" ] && echo --fresh) || exit 1
~/hep/opt/lhc/bin/python gh_tree.py || exit 1
~/hep/opt/lhc/bin/python gh_own_madloop.py $([ -z "$REUSE" ] && echo --fresh) || exit 1
./gh_mg5.sh $REUSE || exit 1
./gh_own_mg5.sh $REUSE || exit 1
~/hep/opt/lhc/bin/python gh_hadronic.py
