#!/bin/bash
# NLO UFO of QCD with UV counterterms and R2 vertices (research note models/qcd, step (5)):
#   1. FeynRules + NLOCT OnShellRenormalization (QCD only, no flavour mixing) -> generated/QCD_ren/   (nlo_renormalize.wl)
#   2. FeynArts + NLOCT WriteCT (QCDOnly, aS with the top at zero momentum) -> generated/QCD_CT.nlo  (nlo_nloct.wl)
#   3. FeynRules: NLOCT's counterterms and R2 vertices against the note and DGPP, WriteUFO
#      -> generated/QCD_NLO_UFO                                                                        (nlo_ufo.wl)
# Each step runs in its own kernel (FeynRules and FeynArts must not share one).
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
for step in nlo_renormalize nlo_nloct nlo_ufo; do
  echo "=== $step"
  wolframscript -file "$step.wl" 2>&1 | grep -E '^(renormalized|written|perturbed|R2 |UV |decimal)|::' |
    grep -v -E 'Symbol::argx|Last::nolast' | cut -c1-300
done
