#!/bin/bash
# Research note models/sm_pp, step (4): the SSM Z' of stage 6 of the LHC tools (environment.pdf) at NLO in QCD.
#   (4a) zp_hadronic.py: the own LO and NLO with the Drell-Yan coefficient functions, K and K(m_ll) (about 6 minutes);
#   (4b) zp_generate_nlo.sh: the NLO UFO of QCDZp.fr with NLOCT (about 1 minute); zp_madloop.py: MadLoop's u u~ > e+ e- against the
#        own form factor;
#   (4c) zp_mg5.sh: aMC@NLO at fixed order at 1, 3, 5 TeV (about 5 minutes on 10 cores); zp_compare.py: against (4a);
#   (4d) zp_limit.py: stage 6's limits with its Delphes events reweighted by K(m_ll) (about 1 minute, 1.8 GB), and the data of the
#        note's figure 7.
# Needs stage 6's outputs (environment/tests/lhc/out/zprime: the MG5 runs and the Delphes files of run_stage6.sh) and the
# ATLAS HEPData tables (~/hep/data/hepdata-ins1725190).  With --reuse, zp_mg5.sh runs nothing that has its HwU, and the NLO UFO
# is made only if missing.
cd "$(dirname "$0")"
mkdir -p work
REUSE=""; for a in "$@"; do [ "$a" = "--reuse" ] && REUSE="--reuse"; done
~/hep/opt/lhc/bin/python zp_hadronic.py | grep -E "^\(|M = |written" || exit 1
if [ -z "$REUSE" ] || [ ! -d generated/QCDZp_NLO_UFO ]; then ./zp_generate_nlo.sh || exit 1; fi
~/hep/opt/lhc/bin/python zp_madloop.py $([ -z "$REUSE" ] && echo --fresh) || exit 1
./zp_mg5.sh $REUSE || exit 1
~/hep/opt/lhc/bin/python zp_compare.py || exit 1
~/hep/opt/lhc/bin/python zp_limit.py
