#!/bin/bash
# Stage 2 of the LHC tools (environment.pdf): Pythia 8.317 and HepMC 2.06.09 through MG5 (which showers with main164).
#   1. p p -> e+ e- (model sm, 13 TeV, LHAPDF 331700, 60 < m_ee < 120 GeV), 10000 events, showered by Pythia 8:
#      Pythia's cross section against the LHE one, and in every HepMC event the conservation of the four-momentum
#      (sum of the final state = (0, 0, 0, sqrt s)), of the charge (+2) and of the baryon number (2)    (test_pythia.py shower)
#   2. MLM matching of p p -> e+ e- + 0, 1, 2 jets (qCut = 1.5 xqcut): runs 1-3 with NNPDF4.0 and runs 4 with nn23lo1 keep
#      MG5's default (Pythia's ISR on its own NNPDF2.3 LO); runs 5-7 (xqcut 15, 20, 30) set Pythia's PDF to NNPDF4.0 too,
#      run 8 repeats run 6 with 200000 events.  The matched cross section against xqcut and own bookkeeping; the DJRs of
#      MG5aMC_PY8_interface (kT, R = 0.4) against own of the same definition, their step at qCut (with controls away
#      from qCut), and run 8 again with qCut = 25, 40 GeV and the shower-kT scheme                 (test_pythia.py matching)
# Output in ./out (about 3 GB: the HepMC file of step 1 and the parton-level reshowers).  About 45 minutes.
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
  echo "set drjl 0"; echo "set JetMatching:qCut 30.0"; echo "set HEPMCoutput:file /dev/null"; echo "done"
  # runs 5-7: Pythia's PDF set to the matrix elements' (MG5 does not pass it), xqcut = 15, 20, 30; run 8: xqcut 20, 200000 events
  for xn in "15 20000" "20 20000" "30 20000" "20 200000"; do
    xq=${xn% *}; nev=${xn#* }; qc=$(python3 -c "print(1.5 * $xq)")
    echo "launch $HERE/out/mlm_proc"; echo "shower=Pythia8"; echo "done"; echo "set nevents $nev"; pdf
    echo "set ickkw 1"; echo "set xqcut $xq"; echo "set ptj 0"; echo "set etaj -1"; echo "set drjj 0"; echo "set drjl 0"
    echo "set JetMatching:qCut $qc"; echo "set PDF:pSet LHAPDF6:NNPDF40_nlo_as_01180"; echo "set HEPMCoutput:file /dev/null"
    echo "done"
  done; } > out/mlm.mg5
# run MG5 from its own directory (its 'install' and HEPTools paths are relative to the working directory)
for p in shower mlm; do
  (cd ~/hep/MG5_aMC_v3_8_1 && ~/hep/bin/mg5_aMC "$HERE/out/$p.mg5") > out/$p.log 2>&1 || { echo "MG5 $p failed: out/$p.log"; exit 1; }
done
python3 test_pythia.py shower matching
