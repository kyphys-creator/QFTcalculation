#!/bin/bash
# Step (4) of the abelian Higgs note: UV poles of the three- and four-point functions and NLOCT.
#   1. vertex_feyncalc.wl  : FeynArts + FeynCalc, general R_xi: UV poles of h h h, G G h, A A h, A G h (1PI + tadpole-attached)
#                            and h h h h, G G G G, G G h h, A A h h, A A G G, A A A A (1PI, zero momenta) against the FJ
#                            counterterm vertices of the note (about 4 minutes)
#   2. nlo_renormalize.wl  : FeynRules + NLOCT OnShellRenormalization (Feynman gauge) -> generated/AbelianHiggs_ren/
#   3. nlo_nloct.wl        : FeynArts + NLOCT WriteCT -> generated/AbelianHiggs_CT.nlo
#   4. nlo_compare.wl      : the 1/eps poles of NLOCT's UV vertices against the note -> results/nlo_compare.csv
# Each Mathematica step runs in its own kernel (FeynRules and FeynArts/FeynCalc must not share one).
# Needs Src/generated/AbelianHiggs_FA (run generate_AbelianHiggs.wl first) and the local FeynRules patches.
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
mkdir -p work results
wolframscript -file vertex_feyncalc.wl 2>&1 | grep -E "^counter|UV \+ counterterm|^\(c\)|Summary" | sed -E 's/;  K UV.*;  UV \+/;  UV +/'
wolframscript -file nlo_renormalize.wl 2>&1 | grep -E "^renormalized|^written" | cut -c1-300
wolframscript -file nlo_nloct.wl > work/nlo_nloct.log 2>&1; grep -E "^written" work/nlo_nloct.log
wolframscript -file nlo_compare.wl 2>&1 | grep -v "^ *$" | sed -E 's/InputForm\[([^]]*)\]/\1/g'
