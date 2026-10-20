#!/bin/bash
# The stage-3 LHC events (environment.pdf, Sec. 9: p p -> e+ e-, 13 TeV, MG5 + Pythia 8, HepMC 2.06.09) through Geant4's
# example HepMCEx02: a simplified collider detector in a 5 m x 20 m air hall (3 T solenoid field for r < 1 m, |z| < 1 m,
# not bounded by a volume; lead calorimeters from r = 2 m; argon muon chambers).
#   1. the first N events (default 2000) of ../../lhc/out/s3_proc/Events/run_01/tag_1_pythia8_events.hepmc.gz
#   2. HepMCEx02 built from the installed example with the event and stepping actions of this directory
#   3. two runs: Geant4's default accuracy of the field propagation (as in the example) and epsilon = 1e-7
#      (H02_FIELD_EPS, see H02EventAction.cc)
#   4. test_hepmc.py: the Geant4 primaries against the HepMC file; where the primary e+- enter the barrel calorimeter,
#      against own helix-plus-line extrapolation
# Needs the stage-3 output (../../lhc/run_stage3.sh).  Usage: ./run_hepmc.sh [N].  Output in ../out/hepmc.
cd "$(dirname "$0")"
N=${1:-2000}
HEPMC=../../lhc/out/s3_proc/Events/run_01/tag_1_pythia8_events.hepmc.gz
[ -f "$HEPMC" ] || { echo "no stage-3 events: run ../../lhc/run_stage3.sh first"; exit 1; }
source ~/hep/opt/geant4env.sh
EX=$HOME/hep/geant4-11.4.3/share/Geant4/examples/extended/eventgenerator/HepMC/HepMCEx02
PY=~/miniforge3/envs/qft/bin/python
O=../out/hepmc
rm -rf $O && mkdir -p $O
(cmake -S . -B $O/build -DCMAKE_BUILD_TYPE=Release -DEX_DIR=$EX -DHEPMC_DIR=$HOME/hep/MG5_aMC_v3_8_1/HEPTools/hepmc \
   > $O/cmake.log 2>&1 && cmake --build $O/build -j 4 > $O/make.log 2>&1) || { echo "build failed: $O/*.log"; exit 1; }
gzip -dc "$HEPMC" | awk -v N=$N '/^E /{n++} n>N{exit} {print}' > $O/events.hepmc
echo "HepMC::IO_GenEvent-END_EVENT_LISTING" >> $O/events.hepmc
printf '/control/verbose 0\n/run/verbose 1\n/generator/select hepmcAscii\n/generator/hepmcAscii/open ../events.hepmc\n/generator/hepmcAscii/verbose 0\n/run/beamOn %s\n' $N > $O/run.mac
mkdir -p $O/eps_default $O/eps_1e-7
(cd $O/eps_default && ../build/HepMCEx02 ../run.mac > run.log 2>&1) &
(cd $O/eps_1e-7 && H02_FIELD_EPS=1e-7 ../build/HepMCEx02 ../run.mac > run.log 2>&1) &
wait
for d in eps_default eps_1e-7; do
  [ -s $O/$d/events.csv ] || { echo "HepMCEx02 failed: $O/$d/run.log"; exit 1; }
  echo "--- field propagation: ${d#eps_} epsilon ($(($(wc -l < $O/$d/events.csv) - 1)) events)"
  $PY test_hepmc.py $O/events.hepmc $O/$d/primaries.csv $O/$d/calo_entry.csv $O/$d/events.csv |
    { [ $d = eps_default ] && cat || grep '^field'; }
done
