#!/bin/bash
# Open the p p -> lv+ lv- events in the barrel detector in the Qt session, one event at a time (detector/vlldet.cc,
# detector/view.mac).  Usage: ./run_view.sh [first event, default 0] [--check]
#   The events are the HepMC file of run_workflow.sh (step 2).  The Qt console prints each event's lv+- (momentum,
#   beta, where the track ends, the times at the muon stations).  /run/beamOn 1 shows the next event.
#   --check: no window: the same view drawn off screen (TSG_OFFSCREEN) to out/view/check.png, then exit.
# The window stays open until it is closed; the process is killed above 1.5 GB of memory (only the tracks above 1 GeV
# are kept for drawing: a full event's showers have some 10^5 tracks).  Output in out/view.
cd "$(dirname "$0")"
FIRST=0; CHECK=0
for a in "$@"; do case $a in --check) CHECK=1 ;; [0-9]*) FIRST=$a ;; esac; done
source ~/hep/opt/geant4env.sh
HEP=$PWD/out/vll_proc/Events/run_01/tag_1_pythia8_events.hepmc.gz
[ -s "$HEP" ] || { echo "no events: run ./run_workflow.sh first"; exit 1; }
B=out/detector/build
if [ ! -x $B/vlldet ] || [ -n "$(find detector -newer $B/vlldet \( -name '*.cc' -o -name '*.hh' -o -name CMakeLists.txt \))" ]; then
  (cmake -S detector -B $B -DCMAKE_BUILD_TYPE=Release > out/detector/cmake.log 2>&1 &&
   cmake --build $B -j 4 > out/detector/make.log 2>&1) || { echo "build failed: out/detector/*.log"; exit 1; }
fi
O=out/view
mkdir -p $O
rm -f $O/check.png
if [ $CHECK = 1 ]; then
  export VLLDET_OFFSCREEN=1
  { sed 's|^/vis/open TSG_QT_GLES|/vis/open TSG_OFFSCREEN|' detector/view.mac
    printf '/vis/tsg/offscreen/set/format zb_png\n/vis/tsg/offscreen/set/file check.png\n'
    printf '/vis/tsg/offscreen/set/transparency true\n'; } > $O/view.mac
else
  cp detector/view.mac $O/view.mac
fi
printf '/vlldet/event %s\n/run/beamOn 1\n' $FIRST >> $O/view.mac
[ $CHECK = 1 ] && echo "/vis/viewer/rebuild" >> $O/view.mac   # the off-screen viewer writes its file when it draws the view
(cd $O && exec ../../$B/vlldet "$HEP" > view.log 2>&1) &
pid=$!
echo "vlldet started (pid $pid), first event $FIRST; log in $O/view.log"
peak=0
while ps -p $pid > /dev/null 2>&1; do
  r=$(ps -o rss= -p $pid 2>/dev/null)
  [ -n "$r" ] && [ "$r" -gt $peak ] && peak=$r
  [ -n "$r" ] && [ "$r" -gt 1572864 ] && { echo "MEMORY GUARD: vlldet at $((r / 1024)) MB, killed"; kill -9 $pid; }
  sleep 1
done
echo "vlldet closed (largest memory $((peak / 1024)) MB)"
