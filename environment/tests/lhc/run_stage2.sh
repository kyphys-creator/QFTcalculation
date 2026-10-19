#!/bin/bash
# Stage 2 of the LHC tools (environment.pdf): Pythia 8.317 and HepMC 2.06.09 through MG5 (which showers with main164).
#   1. p p -> e+ e- (model sm, 13 TeV, LHAPDF 331700, 60 < m_ee < 120 GeV), 10000 events, showered by Pythia 8:
#      Pythia's cross section against the LHE one, and in every HepMC event the conservation of the four-momentum
#      (sum of the final state = (0, 0, 0, sqrt s)), of the charge (+2) and of the baryon number (2)    (test_pythia.py shower)
#   2. MLM matching of p p -> e+ e- + 0, 1, 2 jets, xqcut = 15, 20, 30 GeV with NNPDF4.0 and 20 GeV with nn23lo1
#      (qCut = 1.5 xqcut), 20000 events each: the matched cross section against xqcut and own bookkeeping; own DJRs
#      (main164 parton-level reshowers, own kT) against the matching's own (MG5aMC_PY8_interface), and the step of the
#      summed DJRs at qCut; run 2 again with Pythia's PDF (and alpha_s) set to the matrix elements' (test_pythia.py matching)
# Output in ./out (about 5 GB: the HepMC file of step 1 and the parton-level reshowers).  About 20 minutes.
cd "$(dirname "$0")"
HERE=$(pwd)
mkdir -p out
pdf () {
  cat <<CARD
set ebeam1 6500
set ebeam2 6500
set pdlabel lhapdf
set lhaid 331700
set use_syst False
set ptl 0
set etal -1
set drll 0
set mmll 60
set mmllmax 120
CARD
}
{ echo "import model sm"; echo "generate p p > e+ e-"; echo "output $HERE/out/shower_proc -f"; echo "launch $HERE/out/shower_proc"
  echo "shower=Pythia8"; echo "done"; echo "set nevents 10000"; pdf
  echo "set fixed_ren_scale True"; echo "set fixed_fac_scale True"; echo "set scale 91.188"
  echo "set dsqrt_q2fact1 91.188"; echo "set dsqrt_q2fact2 91.188"; echo "done"; } > out/shower.mg5
{ echo "import model sm"; echo "generate p p > e+ e- @0"; echo "add process p p > e+ e- j @1"; echo "add process p p > e+ e- j j @2"
  echo "output $HERE/out/mlm_proc -f"
  for xq in 15 20 30; do
    qc=$(python3 -c "print(1.5 * $xq)")
    echo "launch $HERE/out/mlm_proc"; echo "shower=Pythia8"; echo "done"; echo "set nevents 20000"; pdf
    echo "set ickkw 1"; echo "set xqcut $xq"; echo "set ptj 0"; echo "set etaj -1"; echo "set drjj 0"; echo "set drjl 0"
    echo "set JetMatching:qCut $qc"; echo "set HEPMCoutput:file /dev/null"; echo "done"
  done
  # run 4: xqcut = 20 GeV with MG5's internal nn23lo1 (NNPDF2.3 LO, alpha_s 0.130: Pythia's default ISR PDF)
  echo "launch $HERE/out/mlm_proc"; echo "shower=Pythia8"; echo "done"; echo "set nevents 20000"; pdf
  echo "set pdlabel nn23lo1"; echo "set ickkw 1"; echo "set xqcut 20"; echo "set ptj 0"; echo "set etaj -1"; echo "set drjj 0"
  echo "set drjl 0"; echo "set JetMatching:qCut 30.0"; echo "set HEPMCoutput:file /dev/null"; echo "done"; } > out/mlm.mg5
# run MG5 from its own directory (its 'install' and HEPTools paths are relative to the working directory)
for p in shower mlm; do
  (cd ~/hep/MG5_aMC_v3_8_1 && ~/hep/bin/mg5_aMC "$HERE/out/$p.mg5") > out/$p.log 2>&1 || { echo "MG5 $p failed: out/$p.log"; exit 1; }
done
python3 test_pythia.py shower matching
