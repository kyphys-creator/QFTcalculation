#!/bin/bash
# NLO UFO of the Standard Model with UV counterterms and R2 vertices (research note models/sm, step (6)):
#   1. FeynRules + NLOCT OnShellRenormalization -> generated/SM_ren/                 (nlo_renormalize.wl, ~2 min)
#   2. FeynArts + NLOCT WriteCT                 -> generated/SM_CT.nlo (6 MB, not in git) (nlo_nloct.wl, ~3 min)
#   3. FeynRules WriteUFO -> generated/SM_NLO_a0_UFO and SM_NLO_a0_heavy_UFO (on-shell, charge alpha(0), counterterm
#      couplings as 40-digit numbers at the note's point / with m_e = 2, m_mu = 3 GeV), after comparing NLOCT's
#      two-point counterterms with the note                                            (nlo_ufo.wl)
#   4. ufo_digits.py: the numbers of CT_couplings.py split into 7-digit pieces (MadGraph keeps 7 digits)
# Each step runs in its own kernel (FeynRules and FeynArts must not share one).
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
mkdir -p work
for step in nlo_renormalize nlo_nloct nlo_ufo; do
  echo "=== $step"
  wolframscript -file "$step.wl" > "work/$step.log" 2>&1
  grep -E '^(renormalized|written|perturbed|\(a\)|\(b\)|\(c0?\)|The finite)' "work/$step.log" | cut -c1-300
done
"$HOME/miniforge3/envs/qft/bin/python" ufo_digits.py generated/SM_NLO_a0_UFO generated/SM_NLO_a0_heavy_UFO
