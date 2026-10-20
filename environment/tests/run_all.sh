#!/bin/bash
# Re-run every check of the loop-calculation stack (environment.pdf, Sec. 5).
# Usage: ./run_all.sh [--no-mg5] [--thermal] [--twoloop] [--lhc]      Output goes to ./out and ./out/log.txt
#   --thermal also re-runs the cross-checks of the thermal tools (environment.pdf, Sec. 7) in
#   models/phi34_thermal/Src: CosmoTransitions, DRalgo, Matchotter, PT2GWFinder + FindBounce, PhaseTracer, BSMPT,
#   TransitionListener, WallGo (about 50 minutes; they rewrite the CSV files in Src/results).
#   --twoloop re-runs the two-loop check of models/phi3 (environment.pdf, Sec. 8): Kira, FIRE, AMFlow, TSIL,
#   pySecDec, feyntrop on the d = 4 two-loop self-energy (about 12 minutes).
#   --lhc re-runs the checks of the LHC tools (environment.pdf, Sec. 9) in ./lhc: stage 1, LHAPDF and the PDF sets
#   (sum rules; p p -> e+ e- and g g -> H in MG5 against own integrals; about 1 minute); stage 2, Pythia 8 and HepMC
#   (shower, conservation laws, MLM matching and DJRs; about 45 minutes, 3.5 GB in lhc/out); stage 3, ROOT and Delphes
#   (GenJets against own FastJet, the efficiencies and smearing against the card; about 1.5 minutes); stage 4,
#   MadAnalysis5 and PADForSFS (a 1 TeV gluino signal through ATLAS-SUSY-2016-07, cutflows against the SFS paper;
#   about 16 minutes, 2.7 GB in lhc/out; the control samples of run_stage4.sh --controls are not made here); stage 5,
#   pyhf, SModelS and HiggsTools (one-bin limits against own formulas and MadAnalysis5, the ATLAS 1Lbb likelihood against
#   HEPData, SModelS against own interpolation and pyhf, HiggsSignals with the Higgs note's widths; about 10 minutes).
#   --eftdm re-runs the checks of the EFT and dark-matter tools (environment.pdf, Sec. EFT/DM) in ./eftdm: stage 1,
#   wilson and DsixTools (SMEFT and WET running, tree matching, against own formulas and each other); stage 2, DirectDM;
#   stage 3, MadDM 3.3 (sigma_SI, <sigma v>, Omega h^2 of a Higgs-portal scalar against own formulas; the tree-level
#   continuum indirect sigma v of each channel; the loop-induced lines S S -> a a, a Z against the Higgs note's one-loop
#   amplitudes, with an NLO UFO made by NLOCT the first time, about 5 minutes, and reused afterwards); stage 4,
#   micrOMEGAs 7.1.10 on the same model (about 5 minutes in all, 10 the first time).
# Test files are named test_*: a file called formcalc.wl in the working directory would
# shadow the FormCalc package (macOS file names are case-insensitive).
cd "$(dirname "$0")"
NO_MG5=0; THERMAL=0; TWOLOOP=0; LHC=0; EFTDM=0
for a in "$@"; do
  case "$a" in
    --no-mg5) NO_MG5=1 ;;
    --thermal) THERMAL=1 ;;
    --twoloop) TWOLOOP=1 ;;
    --lhc) LHC=1 ;;
    --eftdm) EFTDM=1 ;;
  esac
done
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

if [ "$NO_MG5" = 0 ]; then
  step "MadGraph (e+e- -> mu+mu-, gg -> H loop-induced)"
  rm -rf out/mg5_ee_mumu out/mg5_ggh
  mg5_aMC mg5_test.mg5 > out/mg5.log 2>&1
  grep -E 'Cross-section' out/mg5.log | tee -a "$log"
fi
if [ "$THERMAL" = 1 ]; then
  TH=../../models/phi34_thermal/Src
  step "Thermal tools: CosmoTransitions (models/phi34_thermal, step (7))"
  $TH/run_cosmotransitions_check.sh 2>&1 | tee -a "$log"
  step "Thermal tools: DRalgo, Matchotter, PT2GWFinder + FindBounce (step (8))"
  $TH/run_thermal_tools_check.sh 2>&1 | tee -a "$log"
  step "Thermal tools: PhaseTracer, BSMPT, TransitionListener (step (11))"
  $TH/run_review_tools_check.sh 2>&1 | grep -v -i warning | tee -a "$log"
  step "Thermal tools: WallGo, TransitionListener's LTE wall speed (step (12))"
  $TH/run_wallgo_check.sh 2>&1 | grep -v -i warning | tee -a "$log"
fi
if [ "$TWOLOOP" = 1 ]; then
  step "Two-loop tools: Kira, FIRE, AMFlow, TSIL, pySecDec, feyntrop (models/phi3, step (16))"
  ../../models/phi3/Src/run_twoloop4_check.sh 2>&1 | tee -a "$log"
fi
if [ "$LHC" = 1 ]; then
  step "LHC tools, stage 1: LHAPDF 6.5.5 and the PDF sets (sum rules, MG5 p p -> e+ e-, g g -> H)"
  ./lhc/run_stage1.sh 2>&1 | tee -a "$log"
  step "LHC tools, stage 2: Pythia 8.317 and HepMC 2.06.09 (shower, conservation, MLM matching, DJRs)"
  ./lhc/run_stage2.sh 2>&1 | tee -a "$log"
  step "LHC tools, stage 3: ROOT 6.32.14, Delphes 3.5.1, FastJet (GenJets, efficiencies, smearing)"
  ./lhc/run_stage3.sh 2>&1 | grep -v "^#" | tee -a "$log"
  step "LHC tools, stage 4: MadAnalysis5 1.11.0, PADForSFS (ATLAS-SUSY-2016-07 cutflows of a 1 TeV gluino)"
  ./lhc/run_stage4.sh 2>&1 | tee -a "$log"
  step "LHC tools, stage 5: pyhf 0.7.6, SModelS 3.2.1, HiggsTools 1.3 (limits, 1Lbb likelihood, HiggsSignals)"
  ./lhc/run_stage5.sh 2>&1 | tee -a "$log"
fi
if [ "$EFTDM" = 1 ]; then
  step "EFT/DM tools, stage 1: wilson (d21596fa) and DsixTools 2.1 (running, matching, WCxf)"
  ./eftdm/run_stage1.sh 2>&1 | tee -a "$log"
  step "EFT/DM tools, stage 2: DirectDM 2.2.3 (Python) and 1.2.1 (Mathematica)"
  ./eftdm/run_stage2.sh 2>&1 | tee -a "$log"
  step "EFT/DM tools, stage 3: MadDM 3.3 (rc/3.3) with RAPIDD, Higgs-portal scalar"
  ./eftdm/run_stage3.sh 2>&1 | tee -a "$log"
  step "EFT/DM tools, stage 3: MadDM's tree-level continuum indirect sigma v of each channel"
  ./eftdm/run_stage3_id.sh 2>&1 | tee -a "$log"
  step "EFT/DM tools, stage 3: MadDM's loop-induced lines S S -> a a, a Z (NLO UFO from NLOCT, made once)"
  if [ -d eftdm/out/model_nlo/SM_SingletDM_NLO_UFO ]; then ./eftdm/run_stage3_line.sh --no-ufo; else ./eftdm/run_stage3_line.sh; fi 2>&1 | tee -a "$log"
  step "EFT/DM tools, stage 4: micrOMEGAs 7.1.10 on the same model and its own SingletDM"
  ./eftdm/run_stage4.sh 2>&1 | tee -a "$log"
fi
echo "done; full log in $log"
