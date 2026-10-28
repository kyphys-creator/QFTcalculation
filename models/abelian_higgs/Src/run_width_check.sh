#!/bin/bash
# Step (5) of the abelian Higgs note: the NLO width Gamma(h -> A A).
#   1. nlo_width_formcalc.wl : FormCalc, Feynman gauge: the form factors F_g, F_b (1PI + tadpole) -> results/nlo_width_formcalc.m
#   2. nlo_width_feyncalc.wl : FeynCalc, general R_xi: the same form factors exact in D, against FormCalc at xi = 1
#                              -> results/nlo_width_sigma.m
#   3. nlo_width_numeric.wl  : renormalized amplitude (FJ counterterms, LSZ residues from step (3)), UV poles, delta_OS
#                              for xi = 1/2, 1, 3, 10 and mu = 1, 2 (Package-X) -> results/nlo_width.csv
#   4. nlo_ufo.wl            : the UFO with NLOCT's UV and R2 vertices -> generated/AbelianHiggs_NLO_UFO
#   5. MadLoop: generate h > zp zp [virt=QED], output standalone -> work/ml_haa; check_sa.f reads the point from PS.input
#      and MU_R from MU_R.input
#   6. madloop_numeric.py    : MadLoop's finite/born against delta_OS -> results/madloop.csv
#   7. nlo_width_fortran.wl  : FormCalc's Fortran code (WriteSquaredME, WriteRenConst, SetupCodeDir) for the width with
#                              the counterterm dCTAAh -> work/fc_haa
#   8. formcalc_fortran.py   : builds it with LoopTools (Delta = 0, 1e3, 1e7; mu = 1/2, 1, 2, 5), runs the decay and compares
#                              with delta_OS -> results/nlo_width_fortran.csv
# Needs generated/AbelianHiggs_FA, results/oneloop_sigma.m (run_oneloop_check.sh) and generated/AbelianHiggs_CT.nlo
# (run_vertex_check.sh).  Each Mathematica step runs in its own kernel.
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
PY="$HOME/miniforge3/envs/qft/bin/python"
mkdir -p work results
wolframscript -file nlo_width_formcalc.wl 2>&1 | grep -E "^(one-loop|tree|written)"
wolframscript -file nlo_width_feyncalc.wl 2>&1 | grep -E "^\("
wolframscript -file nlo_width_numeric.wl 2>&1 | grep -E "^\("
wolframscript -file nlo_ufo.wl 2>&1 | grep -E "^(R2 vertices|written)"
rm -rf work/AbelianHiggs_NLO_UFO work/ml_haa
cp -R generated/AbelianHiggs_NLO_UFO work/
printf 'import model ./work/AbelianHiggs_NLO_UFO\ngenerate h > zp zp [virt=QED]\noutput standalone ./work/ml_haa\n' > work/ml_haa.mg5
mg5_aMC work/ml_haa.mg5 > work/ml_haa.log 2>&1
rm -f py.py MG5_debug
grep -E 'Contributing diagrams' work/ml_haa.log
P=work/ml_haa/SubProcesses/P0_h_zpzp
"$PY" - "$P/check_sa.f" <<'PYEOF'
import sys
p = sys.argv[1]
s = open(p).read()
s = s.replace("PARAMETER (READPS = .FALSE.)", "PARAMETER (READPS = .TRUE.)")
s = s.replace("PARAMETER (NPSPOINTS = 4)", "PARAMETER (NPSPOINTS = 1)")
old = "        MU_R=SQRTS\n"
new = (old + "C       research note models/abelian_higgs, step (5): a fixed MU_R can be given in MU_R.input\n"
       "        OPEN(968, FILE='MU_R.input', STATUS='OLD', ERR=9979)\n"
       "        READ(968,*) MU_R\n"
       "        CLOSE(968)\n"
       " 9979   CONTINUE\n")
assert s.count(old) == 1
open(p, "w").write(s.replace(old, new))
PYEOF
(cd "$P" && make check > make.log 2>&1 && echo "compiled $P/check") || { echo "compilation failed, see $P/make.log"; exit 1; }
"$PY" madloop_numeric.py
wolframscript -file nlo_width_fortran.wl 2>&1 | grep -E "^(one-loop|written)"
"$PY" formcalc_fortran.py
