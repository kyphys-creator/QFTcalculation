#!/bin/bash
# NLO UFOs of the phi^3 model with UV counterterms (research note models/phi34, step (5)):
#   1. FeynRules + NLOCT OnShellRenormalization -> generated/Phi34_ren/        (nlo_renormalize.wl)
#   2. FeynArts + NLOCT WriteCT                 -> generated/Phi34_CT.nlo      (nlo_nloct.wl)
#   3. FeynRules WriteUFO -> generated/Phi34_NLO_OS_UFO, Phi34_NLO_MSbar_UFO   (nlo_ufo.wl)
# Each step runs in its own kernel (FeynRules and FeynArts must not share one).
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
for step in nlo_renormalize nlo_nloct nlo_ufo; do
  echo "=== $step"
  wolframscript -file "$step.wl" 2>&1 | grep -E '^(renormalized|written|R2 vertices|deltaZ|2 m deltam|vertex counterterm|MS-bar two-point)|::' |
    grep -v -E 'Symbol::argx|Last::nolast' | cut -c1-400
done
