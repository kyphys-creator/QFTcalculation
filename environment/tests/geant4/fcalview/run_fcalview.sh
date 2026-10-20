#!/bin/bash
# Open showers in the ATLAS FCAL of the lAr_calorimeter test-beam example in the Qt session (fcalview.cc, fcalview.mac).
# Usage: ./run_fcalview.sh [energy in GeV, default 20] [particle, default e-] [--skip N, default 2] [--check]
#   The beam positions and directions come from the example's track file of that energy (20, 40, 60, 80, 120 or 200 GeV;
#   read once per process), cleaned as in ../fcal/run_fcal.sh (the first line of tracks-120GeV.dat has cosZ = NaN).
#   --skip N: simulate the first N particles without drawing them (the serial run is the same every time; at 20 GeV
#   the first two shower upstream of the FCAL, the next three reach it cleanly).
#   --check: export the first shower to ../out/fcalview/check.png once the window is up, then close (about 10 s).
# The window stays open until it is closed; the process is killed above 4 GB of memory.  Output in ../out/fcalview.
cd "$(dirname "$0")"
E=20; P=e-; CHECK=0; SKIP=2
while [ $# -gt 0 ]; do
  case $1 in --check) CHECK=1 ;; --skip) SKIP=$2; shift ;; [0-9]*) E=$1 ;; *) P=$1 ;; esac
  shift
done
source ~/hep/opt/geant4env.sh
EX=$HOME/hep/geant4-11.4.3/share/Geant4/examples/advanced/lAr_calorimeter
O=../out/fcalview
mkdir -p $O
if [ ! -x $O/build/fcalview ] || [ fcalview.cc -nt $O/build/fcalview ]; then
  (cmake -S . -B $O/build -DCMAKE_BUILD_TYPE=Release -DEX_DIR=$EX > $O/cmake.log 2>&1 &&
   cmake --build $O/build -j 4 > $O/make.log 2>&1) || { echo "build failed: $O/*.log"; exit 1; }
fi
[ -d $O/data-tracks ] || ~/miniforge3/envs/qft/bin/python ../fcal/clean_tracks.py $EX/data-tracks $O/data-tracks > /dev/null
ln -sfn $EX/geom_data $O/geom_data
{ cat fcalview.mac; printf '/gun/particle %s\n/gun/energy %s GeV\n' $P $E
  [ "$SKIP" -gt 0 ] && printf '/vis/disable\n/run/beamOn %s\n/vis/enable\n' $SKIP
  printf '/run/beamOn 1\n'; } > $O/fcalview.mac
rm -f $O/check.png
if [ $CHECK = 1 ]; then export FCALVIEW_EXPORT=check.png; fi
(cd $O && exec ./build/fcalview > fcalview.log 2>&1) &
pid=$!
echo "fcalview started (pid $pid): $P of $E GeV, first $SKIP not drawn; log in $O/fcalview.log"
peak=0
while ps -p $pid > /dev/null 2>&1; do
  r=$(ps -o rss= -p $pid 2>/dev/null)
  [ -n "$r" ] && [ "$r" -gt $peak ] && peak=$r
  [ -n "$r" ] && [ "$r" -gt 4194304 ] && { echo "MEMORY GUARD: fcalview at $((r / 1024)) MB, killed"; kill -9 $pid; }
  sleep 1
done
echo "fcalview closed (largest memory $((peak / 1024)) MB)"
