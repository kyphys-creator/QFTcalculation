#!/bin/bash
# Research note models/sm_pp, step (2b): the NLO UFO of QCDH.fr (QCD with five massless quarks and the g g H operator):
#   1. FeynRules + NLOCT OnShellRenormalization (QCD only) -> generated/QCDH_ren/   (gh_nlo_renormalize.wl)
#   2. FeynArts + NLOCT WriteCT (QCDOnly)                  -> generated/QCDH_CT.nlo (gh_nlo_nloct.wl)
#   3. FeynRules WriteUFO with the counterterms             -> generated/QCDH_NLO_UFO (gh_nlo_ufo.wl)
# Each step in its own kernel (FeynRules and FeynArts must not share one).  Logs in work/.
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
mkdir -p work
for step in gh_nlo_renormalize gh_nlo_nloct gh_nlo_ufo; do
  echo "=== $step"
  wolframscript -file "$step.wl" > "work/$step.log" 2>&1 || { echo "$step failed: work/$step.log"; exit 1; }
  grep -E '^(renormalized|counterterms|written|perturbed|vertex legs|R2 |UV |decimal)|::' "work/$step.log" |
    grep -v -E 'Symbol::argx|Last::nolast' | cut -c1-400
done
