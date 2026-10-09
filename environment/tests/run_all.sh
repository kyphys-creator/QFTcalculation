#!/bin/bash
# Re-run every check of the loop-calculation stack (environment.pdf, Sec. 5).
# Usage: ./run_all.sh [--no-mg5]      Output goes to ./out and ./out/log.txt
# Test files are named test_*: a file called formcalc.wl in the working directory would
# shadow the FormCalc package (macOS file names are case-insensitive).
cd "$(dirname "$0")"
export PATH="$HOME/hep/bin:$PATH"
export SDKROOT="${SDKROOT:-$(xcrun --show-sdk-path)}"
mkdir -p out
log=out/log.txt
: > "$log"
step () { echo "=== $1" | tee -a "$log"; }

step "FORM"
form test_form_expand.frm 2>&1 | grep -E 'FORM [0-9]|F =|x\^' | tee -a "$log"

step "COLLIER (Fortran)"
gfortran -I"$HOME/hep/include" test_collier_b0.f90 -L"$HOME/hep/lib" -lcollier -o out/test_collier_b0 2>/dev/null &&
  (cd out && ./test_collier_b0) | grep B0 | tee -a "$log"

for t in looptools feynhelpers_b0 packagex feyncalc_feynarts formcalc feynrules_sm; do
  step "test_$t.wl"
  wolframscript -file "test_$t.wl" 2>&1 | grep -v -E 'FrontEndObject|^$|libc\+\+abi' | tail -4 | tee -a "$log"
done

step "FeynRules SM UFO vs MG5 sm"
python3 compare_ufo.py out/feynrules/Standard_Model_UFO/vertices.py \
  "$HOME/hep/MG5_aMC_v3_8_1/models/sm/vertices.py" | tee -a "$log"

step "e+e- -> mu+mu- analytic"
python3 ee_mumu_analytic.py | tee -a "$log"

if [ "$1" != "--no-mg5" ]; then
  step "MadGraph (e+e- -> mu+mu-, gg -> H loop-induced)"
  rm -rf out/mg5_ee_mumu out/mg5_ggh
  mg5_aMC mg5_test.mg5 > out/mg5.log 2>&1
  grep -E 'Cross-section' out/mg5.log | tee -a "$log"
fi
echo "done; full log in $log"
