#!/bin/bash
# NLO UFOs of spinor QED with UV counterterms and R2 vertices (research note models/spinor_qed, step (5)):
#   1. FeynRules + NLOCT OnShellRenormalization -> generated/SpinorQED_ren/        (nlo_renormalize.wl)
#   2. FeynArts + NLOCT WriteCT                 -> generated/SpinorQED_CT.nlo      (nlo_nloct.wl)
#   3. FeynRules WriteUFO -> generated/SpinorQED_NLO_MS_UFO (charge MS-bar), SpinorQED_NLO_a0_UFO (alpha(0)),
#      after comparing NLOCT's counterterms and R2 vertices with the note             (nlo_ufo.wl)
# Each step runs in its own kernel (FeynRules and FeynArts must not share one).
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
for step in nlo_renormalize nlo_nloct nlo_ufo; do
  echo "=== $step"
  wolframscript -file "$step.wl" 2>&1 | grep -E '^(renormalized|written|perturbed|vertex|R2|UV|alpha|decimal|The finite)|::' |
    grep -v -E 'Symbol::argx|Last::nolast' | cut -c1-300
done
