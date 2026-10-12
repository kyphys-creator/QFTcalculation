#!/bin/bash
# Total cross section of phi phi scattering to next-to-leading order (research note models/yukawa_ps, step (6)):
#   sigma_tot(phi phi -> X) = sigma(phi phi -> phi phi) + sigma(phi phi -> psi psibar) at tree level and one loop
#   (S-matrix elements, Eqs. (16) and (20) by time reversal) + sigma(phi phi -> phi psi psibar) (same order, lambda ~ y^2).
#   1. COLLIER evaluator of Eqs. (13), (18) at the quadrature nodes                      (xsec_collier.f90)
#   2. MadLoop for phi phi -> psi psibar with the OS UFO (checks the time-reversal step)  -> work/ml_OS_Bbar
#   3. MadGraph standalone, phi phi -> phi psi psibar (spin-summed |M|^2 at given momenta) -> work/sa_xsec3
#      and tree-level cross sections of phi phi -> psi psibar, phi phi -> phi psi psibar  (xsec_mg5.mg5)
#   4. cross sections (one loop also from MadLoop at the same nodes), 2 -> 3 by Gauss-Legendre quadrature in two
#      phase-space parametrizations, comparison, figure -> results/xsec.csv, ../figs/xsec_d4.pdf  (xsec_numeric.py)
# Needs work/ml_OS_A (run_madloop_check.sh) and generated/PsYukawa_UFO, generated/PsYukawa_NLO_OS_UFO.
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
PY="$HOME/miniforge3/envs/qft/bin/python"
mkdir -p work results
[ -x work/ml_OS_A/SubProcesses/P0_phiphi_phiphi/check ] || ./run_madloop_check.sh

echo "=== COLLIER"
gfortran -I"$HOME/hep/include" xsec_collier.f90 -L"$HOME/hep/lib" -lcollier -o work/xsec_collier && echo "built work/xsec_collier"

echo "=== MadLoop, phi phi -> psi psibar (OS counterterms)"
out=work/ml_OS_Bbar
rm -rf "$out"
printf 'import model ./work/PsYukawa_NLO_OS_UFO\ngenerate phi phi > psi psi~ [virt=QCD]\noutput standalone ./%s\n' "$out" > "$out.mg5"
mg5_aMC "$out.mg5" > "$out.log" 2>&1
grep -E 'Contributing diagrams' "$out.log"
P=$(ls -d "$out"/SubProcesses/P0_* | head -1)
"$PY" - "$P/check_sa.f" <<'PYEOF'
import sys
p = sys.argv[1]
s = open(p).read()
s = s.replace("PARAMETER (READPS = .FALSE.)", "PARAMETER (READPS = .TRUE.)")
s = s.replace("PARAMETER (NPSPOINTS = 4)", "PARAMETER (NPSPOINTS = 1)")
old = "        MU_R=SQRTS\n"
new = (old + "C       research note models/yukawa_ps, step (6): a fixed MU_R can be given in MU_R.input\n"
       "        OPEN(968, FILE='MU_R.input', STATUS='OLD', ERR=9979)\n"
       "        READ(968,*) MU_R\n"
       "        CLOSE(968)\n"
       " 9979   CONTINUE\n")
assert s.count(old) == 1
open(p, "w").write(s.replace(old, new))
PYEOF
(cd "$P" && make check > make.log 2>&1 && echo "compiled $P/check") || { echo "compilation failed, see $P/make.log"; exit 1; }

echo "=== MadGraph standalone, phi phi -> phi psi psibar"
rm -rf work/sa_xsec3 work/PsYukawa_UFO
cp -R generated/PsYukawa_UFO work/PsYukawa_UFO   # MadGraph rewrites the UFO it imports
printf 'import model ./work/PsYukawa_UFO\ngenerate phi phi > phi psi psi~\noutput standalone ./work/sa_xsec3\n' > work/sa_xsec3.mg5
mg5_aMC work/sa_xsec3.mg5 > work/sa_xsec3.log 2>&1
rm -f nsqso_born.inc ../nsqso_born.inc py.py MG5_debug   # the standalone output also writes nsqso_born.inc here and in ..
P=$(ls -d work/sa_xsec3/SubProcesses/P1_* | head -1)
(cd "$P" && make check > make.log 2>&1 && echo "compiled $P/check") || { echo "compilation failed, see $P/make.log"; exit 1; }

echo "=== MadGraph, phi phi -> psi psibar and phi phi -> phi psi psibar"
rm -rf work/mg5_xsecBbar work/mg5_xsec3 work/mg5_xsec3lam work/mg5_xsec3y
mg5_aMC xsec_mg5.mg5 > work/xsec_mg5.log 2>&1
rm -f py.py MG5_debug
grep -E '^\s+Cross-section' work/xsec_mg5.log

echo "=== cross sections"
"$PY" xsec_numeric.py
