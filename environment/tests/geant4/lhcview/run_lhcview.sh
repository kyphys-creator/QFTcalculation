#!/bin/bash
# Open the stage-3 LHC events (p p -> e+ e-, 13 TeV) in HepMCEx02's collider detector in the Qt session, one event at a
# time, for the user to look at (lhcview.cc, lhcview.mac).  Usage: ./run_lhcview.sh [N events to take, default 200].
# The events come from ../out/hepmc/events.hepmc (run_hepmc.sh) or else from the stage-3 HepMC file
# (../../lhc/run_stage3.sh).  The window stays open until it is closed; the process is killed above 4 GB of memory.
# Output in ../out/lhcview.
cd "$(dirname "$0")"
N=${1:-200}
source ~/hep/opt/geant4env.sh
EX=$HOME/hep/geant4-11.4.3/share/Geant4/examples/extended/eventgenerator/HepMC/HepMCEx02
O=../out/lhcview
mkdir -p $O
if [ ! -x $O/build/lhcview ] || [ lhcview.cc -nt $O/build/lhcview ]; then
  (cmake -S . -B $O/build -DCMAKE_BUILD_TYPE=Release -DEX_DIR=$EX -DHEPMC_DIR=$HOME/hep/MG5_aMC_v3_8_1/HEPTools/hepmc \
     > $O/cmake.log 2>&1 && cmake --build $O/build -j 4 > $O/make.log 2>&1) || { echo "build failed: $O/*.log"; exit 1; }
fi
SRC=../out/hepmc/events.hepmc
if [ -f $SRC ]; then cat $SRC; else gzip -dc ../../lhc/out/s3_proc/Events/run_01/tag_1_pythia8_events.hepmc.gz; fi |
  awk -v N=$N '/^E /{n++} n>N{exit} {print}' > $O/events.hepmc
echo "HepMC::IO_GenEvent-END_EVENT_LISTING" >> $O/events.hepmc
[ "$(grep -c '^E ' $O/events.hepmc)" -gt 0 ] || { echo "no events: run ../hepmc/run_hepmc.sh or ../../lhc/run_stage3.sh first"; exit 1; }
cp lhcview.mac $O/
nev=$(grep -c '^E ' $O/events.hepmc)
(cd $O && exec ./build/lhcview > lhcview.log 2>&1) &
pid=$!
echo "lhcview started (pid $pid) with $nev events; log in $O/lhcview.log"
while ps -p $pid > /dev/null 2>&1; do
  r=$(ps -o rss= -p $pid 2>/dev/null)
  [ -n "$r" ] && [ "$r" -gt 4194304 ] && { echo "MEMORY GUARD: lhcview at $((r / 1024)) MB, killed"; kill -9 $pid; }
  sleep 2
done
echo "lhcview closed"
