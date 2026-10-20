#!/bin/bash
# Research note models/sm_pp, step (4b): the NLO UFO of QCDZp.fr (QCD with u, c, d, s, a massless electron and the SSM Z'):
#   1. FeynRules + NLOCT OnShellRenormalization (QCD only) -> generated/QCDZp_ren/   (zp_nlo_renormalize.wl)
#   2. FeynArts + NLOCT WriteCT (QCDOnly)                  -> generated/QCDZp_CT.nlo (zp_nlo_nloct.wl)
#   3. FeynRules WriteUFO with the counterterms             -> generated/QCDZp_NLO_UFO (zp_nlo_ufo.wl)
# Each step in its own kernel (FeynRules and FeynArts must not share one).  Logs in work/.
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
mkdir -p work
for step in zp_nlo_renormalize zp_nlo_nloct zp_nlo_ufo; do
  echo "=== $step"
  wolframscript -file "$step.wl" > "work/$step.log" 2>&1 || { echo "$step failed: work/$step.log"; exit 1; }
  grep -E '^(renormalized|written|perturbed|vertex legs|R2 |UV |decimal)|::' "work/$step.log" |
    grep -v -E 'Symbol::argx|Last::nolast' | cut -c1-500
done
