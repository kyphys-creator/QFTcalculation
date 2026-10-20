#!/bin/bash
# Geant4's example advanced/lAr_calorimeter: the ATLAS forward calorimeter (FCAL1 copper/LAr, FCAL2 tungsten/LAr, tilted
# by 2.83 deg) in its CERN test beam, with the beam positions and directions of data-tracks/.  Built from the installed
# example with FCALEMModuleSD.cc replaced (it also prints FCAL1's visible energy, the sum over its liquid-argon gaps).
#   1. run1.mac (18 events of 20 GeV e-) against the reference output lAr_calorimeter.out
#   2. 20 GeV mu- and e- of 20, 40, 60, 80, 120, 200 GeV, N events each (default 500), one serial process per run, run
#      side by side (the example makes its sensitive detector in Construct(), so worker threads have none, and it reads
#      the track file of the first energy only)
#   3. test_fcal.py: own MIP sampling fraction from the electrode lattice, the muons against it; for the electrons the
#      containment in FCAL1, e/mip, and the resolution of the visible energy, fitted and shown next to the ATLAS result
# The first line of the example's data-tracks/tracks-120GeV.dat has cosX = 12.68, cosY = 9.28, cosZ = NaN: the first
# 120 GeV event then ran away to 178 GB of memory (macOS killed it, 2026-10-20).  So the runs read copies of the track
# files without such lines (clean_tracks.py), and a guard kills any lArCal above 2 GB (normal: about 180 MB).
# Output in ../out/fcal.  About 10 minutes for N = 500 (7 processes, about 180 MB each).
cd "$(dirname "$0")"
N=${1:-500}
source ~/hep/opt/geant4env.sh
EX=$HOME/hep/geant4-11.4.3/share/Geant4/examples/advanced/lAr_calorimeter
PY=~/miniforge3/envs/qft/bin/python
O=../out/fcal
rm -rf $O && mkdir -p $O
(cmake -S . -B $O/build -DCMAKE_BUILD_TYPE=Release -DEX_DIR=$EX > $O/cmake.log 2>&1 &&
 cmake --build $O/build -j 4 > $O/make.log 2>&1) || { echo "build failed: $O/*.log"; exit 1; }
export G4FORCE_RUN_MANAGER_TYPE=Serial
$PY clean_tracks.py $EX/data-tracks $O/data-tracks
rundir () { mkdir -p $O/$1 && ln -sf ../data-tracks $O/$1/data-tracks && ln -sf $EX/geom_data $O/$1/geom_data; }
guard () {   # guard <pid>...: wait for the processes, killing any whose resident memory exceeds 2 GB
  local alive=1 p r
  while [ $alive = 1 ]; do
    alive=0
    for p in "$@"; do
      r=$(ps -o rss= -p $p 2>/dev/null) || continue
      alive=1
      [ "$r" -gt 2097152 ] && { echo "MEMORY GUARD: lArCal (pid $p) at $((r / 1024)) MB, killed"; kill -9 $p; }
    done
    sleep 1
  done
}

rundir ref && cp $EX/run1.mac $O/ref/
(cd $O/ref && exec ../build/lArCal run1.mac > ref.log 2>&1) & guard $!
$PY test_fcal.py ref $O/ref/ref.log $EX/lAr_calorimeter.out

for run in mu_20 e_20 e_40 e_60 e_80 e_120 e_200; do
  p=${run%_*}; e=${run#*_}; [ $p = mu ] && p=mu- || p=e-
  rundir $run
  printf '/run/initialize\n/run/verbose 1\n/gun/particle %s\n/gun/energy %s GeV\n/run/printProgress 0\n/run/beamOn %s\n' \
    $p $e $N > $O/$run/run.mac
  (cd $O/$run && exec ../build/lArCal run.mac > $run.log 2>&1) &
  pids="$pids $!"
done
guard $pids
$PY test_fcal.py scan $EX/geom_data/FCal1Electrodes.dat $O/data-tracks $O/mu_20/mu_20.log \
  $O/e_20/e_20.log $O/e_40/e_40.log $O/e_60/e_60.log $O/e_80/e_80.log $O/e_120/e_120.log $O/e_200/e_200.log
