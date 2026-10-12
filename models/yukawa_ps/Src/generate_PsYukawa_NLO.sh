#!/bin/bash
# NLO UFOs of the pseudoscalar Yukawa model with UV counterterms (research note models/yukawa_ps, step (5)):
#   1. FeynRules + NLOCT OnShellRenormalization -> generated/PsYukawa_ren/        (nlo_renormalize.wl)
#   2. FeynArts + NLOCT WriteCT                 -> generated/PsYukawa_CT.nlo      (nlo_nloct.wl)
#   3. FeynRules WriteUFO -> generated/PsYukawa_NLO_OS_UFO, PsYukawa_NLO_MSbar_UFO   (nlo_ufo.wl)
# Each step runs in its own kernel (FeynRules and FeynArts must not share one).
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
for step in nlo_renormalize nlo_nloct nlo_ufo; do
  echo "=== $step"
  wolframscript -file "$step.wl" 2>&1 | grep -E '^(renormalized|written|perturbed|R2|UV)|::' |
    grep -v -E 'Symbol::argx|Last::nolast' | cut -c1-400
done
