#!/bin/bash
# Stage 6 of the LHC tools (environment.pdf): an own SSM Z' model end to end, against the ATLAS dilepton search with 139 fb^-1
# (arXiv:1903.06248, HEPData ins1725190, ~/hep/data/hepdata-ins1725190; its published values are references).
#   1. zprime/generate_zp.wl (FeynRules, ZpSSM.fr on SM.fr): the Z' f f vertices against the Z's, and the UFO (out/zprime);
#   2. MG5: p p > zp > l+ l- (l = e, mu), NNPDF4.0 NLO (LHAPDF 331700, also Pythia's ISR PDF), fixed scales M, no lepton cuts,
#      the Z' width from MadWidth (two-body), 8000 events at each of nine masses 0.5 to 6 TeV (runs m<M>); Pythia 8;
#   3. Delphes 3.5.1 with its ATLAS card (+ RandomSeed 1) on each HepMC file (out/zprime/delphes_m<M>.root), and with the
#      lepton isolation over the tracks only (delphes_trkiso_m<M>.root); MG5's cross sections with m_ll > 225 GeV (runs xs<M>);
#   4. test_zprime.py: the widths and the cross sections against own formulas and own LHAPDF integrals; the selection
#      efficiency and the mass resolution against ATLAS's; the cross-section limits from the published dilepton spectra with
#      the published background function, against the published limits; the SSM mass limit.
# About 20 minutes, 2.4 GB of HepMC and 6 GB of Delphes files in out/zprime.  With --reuse, nothing is made again that exists.
cd "$(dirname "$0")"
HERE=$(pwd)
export ROOTSYS="$HOME/hep/root-6.32.14"
D="$HOME/hep/MG5_aMC_v3_8_1/Delphes"
MASSES="500 1000 2000 3000 4000 4500 5000 5500 6000"
REUSE=0; [ "$1" = "--reuse" ] && REUSE=1
mkdir -p out/zprime
# 1. the model
if [ "$REUSE" = 0 ] || [ ! -d out/zprime/ZpSSM_UFO ]; then
  wolframscript -file zprime/generate_zp.wl "$HERE/out/zprime" > out/zprime/generate_zp.log 2>&1 \
    || { echo "generate_zp.wl failed: out/zprime/generate_zp.log"; exit 1; }
fi
grep "vertices: " out/zprime/generate_zp.log
# 2. the process
if [ "$REUSE" = 0 ] || [ ! -d out/zprime/zp_proc ]; then
  { echo "import model $HERE/out/zprime/ZpSSM_UFO"; echo "define l+ = e+ mu+"; echo "define l- = e- mu-"
    echo "generate p p > zp > l+ l-"; echo "output $HERE/out/zprime/zp_proc -f"; } > out/zprime/zp_output.mg5
  (cd ~/hep/MG5_aMC_v3_8_1 && ~/hep/bin/mg5_aMC "$HERE/out/zprime/zp_output.mg5") > out/zprime/zp_output.log 2>&1 \
    || { echo "MG5 output failed: out/zprime/zp_output.log"; exit 1; }
fi
{ echo "set RandomSeed 1"; cat "$D/cards/delphes_card_ATLAS.tcl"; } > out/zprime/delphes_card_ATLAS_seed.tcl
for M in $MASSES; do
  [ "$REUSE" = 1 ] && [ -s out/zprime/delphes_m$M.root ] && continue
  { echo "launch $HERE/out/zprime/zp_proc -n m$M"; echo "shower=Pythia8"; echo "done"
    echo "set nevents 8000"; echo "set ebeam1 6500"; echo "set ebeam2 6500"; echo "set pdlabel lhapdf"; echo "set lhaid 331700"
    echo "set fixed_ren_scale True"; echo "set fixed_fac_scale True"; echo "set scale $M"; echo "set dsqrt_q2fact1 $M"
    echo "set dsqrt_q2fact2 $M"; echo "set ptl 0"; echo "set etal -1"; echo "set drll 0"; echo "set mmll 0"
    echo "set use_syst False"; echo "set MZp $M"; echo "set WZp Auto"; echo "compute_widths --body_decay=2"
    echo "set PDF:pSet LHAPDF6:NNPDF40_nlo_as_01180"; echo "set HEPMCoutput:file hepmc.gz"; echo "done"; } > out/zprime/zp_m$M.mg5
  (cd ~/hep/MG5_aMC_v3_8_1 && ~/hep/bin/mg5_aMC "$HERE/out/zprime/zp_m$M.mg5") > out/zprime/zp_m$M.log 2>&1 \
    || { echo "MG5 launch failed: out/zprime/zp_m$M.log"; exit 1; }
  HEP=$(ls out/zprime/zp_proc/Events/m$M/*.hepmc.gz | head -1)
  gzip -dc "$HEP" | "$D/DelphesHepMC2" out/zprime/delphes_card_ATLAS_seed.tcl "out/zprime/delphes_m$M.tmp.root" - \
    > out/zprime/delphes_m$M.log 2>&1 || { echo "Delphes failed: out/zprime/delphes_m$M.log"; exit 1; }
  mv "out/zprime/delphes_m$M.tmp.root" "out/zprime/delphes_m$M.root"
  echo "M = $M GeV: $(grep -a 'Cross-section :' out/zprime/zp_m$M.log | tail -1)"
done
# 3b. the same HepMC through the ATLAS card with the electron and muon isolation summed over the tracks only, outside
#     Delta R = 0.01 (the distributed card sums the energy-flow objects, photons included, and loses the electrons with
#     collinear FSR)
python3 - out/zprime/delphes_card_ATLAS_seed.tcl out/zprime/delphes_card_ATLAS_trkiso.tcl <<'PY'
import re, sys
s = open(sys.argv[1]).read()
for mod in ("ElectronIsolation", "MuonIsolation"):
    i = s.index("module Isolation %s {" % mod)
    j = s.index("}", i)
    # the tracks only, without the candidate's own track: Delphes drops an isolation object only when its UniqueID is the
    # candidate's, and the electrons are new objects after the energy flow, so a small inner cone (MiniCone) removes it
    blk = s[i:j].replace("set IsolationInputArray EFlowFilter/eflow",
                         "set IsolationInputArray TrackMerger/tracks\n  set UseMiniCone true\n  set DeltaRMin 0.01")
    assert blk != s[i:j]
    s = s[:i] + blk + s[j:]
open(sys.argv[2], "w").write(s)
PY
for M in $MASSES; do
  [ -s out/zprime/delphes_trkiso_m$M.root ] && [ "$REUSE" = 1 ] && continue
  HEP=$(ls out/zprime/zp_proc/Events/m$M/*.hepmc.gz | head -1)
  gzip -dc "$HEP" | "$D/DelphesHepMC2" out/zprime/delphes_card_ATLAS_trkiso.tcl "out/zprime/delphes_trkiso_m$M.tmp.root" - \
    > out/zprime/delphes_trkiso_m$M.log 2>&1 || { echo "Delphes failed: out/zprime/delphes_trkiso_m$M.log"; exit 1; }
  mv "out/zprime/delphes_trkiso_m$M.tmp.root" "out/zprime/delphes_trkiso_m$M.root"
done
# 3c. the cross sections with m_ll > 225 GeV (the selection's cut, which MG5 applies), for the comparison with own integrals:
#     no events kept beyond the 2000 of the run (runs xs<M>)
for M in $MASSES; do
  [ "$REUSE" = 1 ] && ls out/zprime/zp_proc/Events/xs$M/*banner.txt > /dev/null 2>&1 && continue
  { echo "launch $HERE/out/zprime/zp_proc -n xs$M"; echo "shower=OFF"; echo "done"
    echo "set nevents 2000"; echo "set ebeam1 6500"; echo "set ebeam2 6500"; echo "set pdlabel lhapdf"; echo "set lhaid 331700"
    echo "set fixed_ren_scale True"; echo "set fixed_fac_scale True"; echo "set scale $M"; echo "set dsqrt_q2fact1 $M"
    echo "set dsqrt_q2fact2 $M"; echo "set ptl 0"; echo "set etal -1"; echo "set drll 0"; echo "set mmll 225"
    echo "set use_syst False"; echo "set MZp $M"; echo "set WZp Auto"; echo "compute_widths --body_decay=2"; echo "done"; } > out/zprime/xs_m$M.mg5
  (cd ~/hep/MG5_aMC_v3_8_1 && ~/hep/bin/mg5_aMC "$HERE/out/zprime/xs_m$M.mg5") > out/zprime/xs_m$M.log 2>&1 \
    || { echo "MG5 launch failed: out/zprime/xs_m$M.log"; exit 1; }
done
# 4. the checks
~/hep/opt/lhc/bin/python test_zprime.py
