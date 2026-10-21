#!/bin/bash
# The stable-lepton workflow (README.md): from a FeynRules model to the detector simulation, each step checked.
#   1. model/generate_vll.wl (FeynRules 2.3.49, VLL.fr on SM.fr): the photon and Z vertices of lv against the right-handed
#      electron's, and the UFO (out/VLL_UFO)
#   2. MG5_aMC 3.8.1: p p > lv+ lv- at 13 TeV, NNPDF4.0 NLO (LHAPDF 331700, also Pythia's), mu_F = mu_R = sqrt(shat);
#      Pythia 8.317 (shower, hadronisation, MPI), decaying only the particles with c tau < 10 mm (Geant4 decays the rest:
#      K0S, Lambda, ...); HepMC 2 (out/vll_proc/Events/run_01)
#   3. detector/vlldet (Geant4 11.4.3, FTFP_BERT + lv+-): all events in the barrel detector, 4 threads at low priority
#      (out/detector/vll.root)
#   4. check_workflow.py: the cross section, the events in Geant4, the energy loss of lv in silicon, the momentum from the
#      tracker, the time of flight to the muon stations, and the mass of lv from both, against own calculations
# Usage: ./run_workflow.sh [N events, default 4000] [--reuse]
#   --reuse: keep what exists (the UFO, the events, the Geant4 run)
# About 7 minutes for 4000 events (Geant4 about 5 with 4 threads).  Output in ./out; the check's figure in figs/.  run_view.sh shows the events in Qt.
cd "$(dirname "$0")"
HERE=$(pwd)
N=4000; REUSE=0
for a in "$@"; do case $a in --reuse) REUSE=1 ;; [0-9]*) N=$a ;; esac; done
mkdir -p out figs
source ~/hep/opt/geant4env.sh   # Geant4, Qt 6 of conda env g4, Apple clang, default SDK

# 1. the model
if [ "$REUSE" = 0 ] || [ ! -d out/VLL_UFO ]; then
  ~/hep/bin/wolframscript -file model/generate_vll.wl "$HERE/out" > out/generate_vll.log 2>&1 \
    || { echo "generate_vll.wl failed: out/generate_vll.log"; exit 1; }
fi
grep "LV vertices" out/generate_vll.log || { echo "no vertex check in out/generate_vll.log"; exit 1; }

# 2. the events
HEP=out/vll_proc/Events/run_01/tag_1_pythia8_events.hepmc.gz
if [ "$REUSE" = 0 ] || [ ! -s $HEP ]; then
  { echo "import model $HERE/out/VLL_UFO"; echo "generate p p > lv+ lv-"; echo "output $HERE/out/vll_proc -f"; } > out/vll_output.mg5
  (cd ~/hep/MG5_aMC_v3_8_1 && ~/hep/bin/mg5_aMC "$HERE/out/vll_output.mg5") > out/vll_output.log 2>&1 \
    || { echo "MG5 output failed: out/vll_output.log"; exit 1; }
  # Pythia's card: MG5's default plus the decays (MG5's set command does not take these)
  { cat out/vll_proc/Cards/pythia8_card_default.dat
    printf '! only the particles with c tau < 10 mm: Geant4 decays the rest (K0S, Lambda, ...) in the detector\n'
    printf 'ParticleDecays:limitTau0 = on\nParticleDecays:tau0Max = 10.0\n'; } > out/vll_proc/Cards/pythia8_card.dat
  { echo "launch $HERE/out/vll_proc -n run_01"; echo "shower=Pythia8"; echo "done"
    echo "set nevents $N"; echo "set iseed 1"; echo "set ebeam1 6500"; echo "set ebeam2 6500"; echo "set pdlabel lhapdf"
    echo "set lhaid 331700"; echo "set dynamical_scale_choice 4"; echo "set use_syst False"
    echo "set PDF:pSet LHAPDF6:NNPDF40_nlo_as_01180"; echo "set HEPMCoutput:file hepmc.gz"; echo "done"; } > out/vll_run.mg5
  (cd ~/hep/MG5_aMC_v3_8_1 && ~/hep/bin/mg5_aMC "$HERE/out/vll_run.mg5") > out/vll_run.log 2>&1 \
    || { echo "MG5 launch failed: out/vll_run.log"; exit 1; }
fi
echo "MG5: $(grep -a 'Cross-section :' out/vll_run.log | tail -1 | sed 's/^ *//'), $(gzip -dc $HEP | grep -c '^E ') events after Pythia"

# 3. the detector simulation
O=out/detector
mkdir -p $O
if [ ! -x $O/build/vlldet ] || [ -n "$(find detector -newer $O/build/vlldet \( -name '*.cc' -o -name '*.hh' -o -name CMakeLists.txt \))" ]; then
  (cmake -S detector -B $O/build -DCMAKE_BUILD_TYPE=Release > $O/cmake.log 2>&1 && cmake --build $O/build -j 4 > $O/make.log 2>&1) \
    || { echo "build failed: $O/*.log"; exit 1; }
fi
if [ "$REUSE" = 0 ] || [ ! -s $O/vll.root ]; then
  rm -f $O/vll.root
  (cd $O && exec nice -n 10 ./build/vlldet ../vll_proc/Events/run_01/tag_1_pythia8_events.hepmc.gz --batch vll.root --threads 4 \
     > vlldet.log 2>&1) &
  pid=$!
  peak=0
  while ps -p $pid > /dev/null 2>&1; do   # the memory guard
    r=$(ps -o rss= -p $pid 2>/dev/null)
    [ -n "$r" ] && [ "$r" -gt $peak ] && peak=$r
    [ -n "$r" ] && [ "$r" -gt 3145728 ] && { echo "MEMORY GUARD: vlldet at $((r / 1024)) MB, killed"; kill -9 $pid; }
    sleep 2
  done
  wait $pid || { echo "vlldet failed: $O/vlldet.log"; exit 1; }
  echo "Geant4: done (largest memory $((peak / 1024)) MB); tracks stopped by the step guard: $(grep -c 'killed after' $O/vlldet.log)"
fi

# 4. the checks
~/hep/opt/lhc/bin/python check_workflow.py
