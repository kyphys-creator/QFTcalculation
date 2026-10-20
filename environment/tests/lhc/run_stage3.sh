#!/bin/bash
# Stage 3 of the LHC tools (environment.pdf): ROOT 6.32.14, Delphes 3.5.1 (with its FastJet) and the Python tools of
# ~/hep/opt/lhc (uproot, awkward, FastJet 3.5 for Python).
#   1. MG5: p p -> e+ e- (model sm, 13 TeV, NNPDF4.0 in the matrix elements and the shower, 60 < m_ee < 120 GeV), 10000 events,
#      shower=Pythia8 and detector=Delphes (MG5's default card, the CMS one): the Delphes tree has every event;
#   2. the same HepMC through Delphes with the CMS card plus TreeWriter branches of the electrons before and after the
#      tracking efficiency, the momentum smearing and the electron efficiency (cards/delphes_card_CMS_checks.tcl);
#   3. test_delphes.py: the GenJets against own anti-kT (R = 0.5, pT > 20 GeV) on the stable non-neutrino particles; the
#      two efficiencies against the card's formulas bin by bin; the smearing against the card's resolution.
# Output in ./out.  About 5 minutes.
cd "$(dirname "$0")"
HERE=$(pwd)
export ROOTSYS="$HOME/hep/root-6.32.14"
export PATH="$ROOTSYS/bin:$PATH"
DELPHES="$HOME/hep/MG5_aMC_v3_8_1/Delphes"
mkdir -p out
{ echo "import model sm"; echo "generate p p > e+ e-"; echo "output $HERE/out/s3_proc -f"; echo "launch $HERE/out/s3_proc"
  echo "shower=Pythia8"; echo "detector=Delphes"; echo "done"
  echo "set nevents 10000"; echo "set ebeam1 6500"; echo "set ebeam2 6500"; echo "set pdlabel lhapdf"; echo "set lhaid 331700"
  echo "set use_syst False"; echo "set ptl 0"; echo "set etal -1"; echo "set drll 0"; echo "set mmll 60"; echo "set mmllmax 120"
  echo "set PDF:pSet LHAPDF6:NNPDF40_nlo_as_01180"; echo "set HEPMCoutput:file hepmc.gz"; echo "done"; } > out/s3.mg5
(cd ~/hep/MG5_aMC_v3_8_1 && ~/hep/bin/mg5_aMC "$HERE/out/s3.mg5") > out/s3.log 2>&1 || { echo "MG5 failed: out/s3.log"; exit 1; }
HEP=$(ls out/s3_proc/Events/run_01/*.hepmc.gz | head -1)
rm -f out/delphes_checks.root
gzip -dc "$HEP" | "$DELPHES/DelphesHepMC2" cards/delphes_card_CMS_checks.tcl out/delphes_checks.root - > out/delphes_checks.log 2>&1 \
  || { echo "Delphes failed: out/delphes_checks.log"; exit 1; }
~/hep/opt/lhc/bin/python test_delphes.py
