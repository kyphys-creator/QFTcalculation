#!/bin/bash
# Geant4's example advanced/composite_calorimeter: the CMS HCAL test beam of 1996 (28 layers of copper and plastic
# scintillator, with or without a 7 x 7 PbWO4 crystal matrix in front), built as distributed.
#   1. test.g4mac (20 events of 100 GeV pi-, ECAL + HCAL, serial); its reference output has no per-event numbers
#   2. HCAL only (dataconf copied with the flag of CrystalMatrixModule set to 0; commenting the line out, as the README
#      says, makes the example build the ECAL with zero size and abort): 20 GeV mu- (2000 events), and e-
#      and pi- of 20, 50, 100, 300 GeV (1000 events each); 8 threads, one run after the other
#   3. test_ccal.py: own sampling fraction from datageom/tbhcal96hcal.geom (minimum and, at 20 GeV, mean ionization
#      loss) against the muons; for e- and pi- the layers weighted by own MIP weights: e/pi (also from the plain sum)
#      and the resolution
# Each run is watched and killed above 3 GB (normal: about 150-400 MB).  Output in ../out/ccal.  About 5 minutes.
cd "$(dirname "$0")"
source ~/hep/opt/geant4env.sh
EX=$HOME/hep/geant4-11.4.3/share/Geant4/examples/advanced/composite_calorimeter
PY=~/hep/opt/lhc/bin/python
O=../out/ccal
rm -rf $O && mkdir -p $O
(cmake -S $EX -B $O/build -DCMAKE_BUILD_TYPE=Release > $O/cmake.log 2>&1 &&
 cmake --build $O/build -j 4 > $O/make.log 2>&1) || { echo "build failed: $O/*.log"; exit 1; }
export CCAL_SENSITIVECONF=g4testbeamhcal96.conf CCAL_GEOMETRYCONF=testbeamhcal96.conf
export CCAL_GLOBALPATH=$EX/dataglobal CCAL_GEOMPATH=$EX/datageom CCAL_VISPATH=$EX/datavis

guarded () {   # guarded <dir> <log> <macro>: run in <dir>, kill above 3 GB
  (cd $1 && exec ../build/CompositeCalorimeter $3 > $2 2>&1) &
  local pid=$! r
  while ps -p $pid > /dev/null 2>&1; do
    r=$(ps -o rss= -p $pid 2>/dev/null)
    [ -n "$r" ] && [ "$r" -gt 3145728 ] && { echo "MEMORY GUARD: CompositeCalorimeter at $((r / 1024)) MB, killed"; kill -9 $pid; }
    sleep 1
  done
  wait $pid || echo "run in $1 failed (exit $?): $1/$2"
}

mkdir -p $O/dist && cp $EX/test.g4mac $O/dist/
CCAL_CONFPATH=$EX/dataconf G4FORCE_RUN_MANAGER_TYPE=Serial guarded $O/dist dist.log test.g4mac
$PY -B test_ccal.py dist $O/dist

mkdir -p $O/dataconf_hcal
for f in g4testbeamhcal96.conf testbeamhcal96.conf; do
  sed -E 's/^("CrystalMatrixModule"[[:space:]]+"tbhcal96xtal"[[:space:]]+)1/\10/' $EX/dataconf/$f > $O/dataconf_hcal/$f
done
export CCAL_CONFPATH=$PWD/$O/dataconf_hcal G4FORCENUMBEROFTHREADS=8
for run in mu_20 e_20 e_50 e_100 e_300 pi_20 pi_50 pi_100 pi_300; do
  p=${run%_*}; e=${run#*_}; n=1000
  case $p in mu) p=mu-; n=2000 ;; e) p=e- ;; pi) p=pi- ;; esac
  mkdir -p $O/$run
  printf '/run/initialize\n/run/printProgress 0\n/gun/position -1380. 0. 0. mm\n/gun/direction 1. 0. 0.\n/gun/particle %s\n/gun/energy %s GeV\n/run/beamOn %s\n' \
    $p $e $n > $O/$run/run.mac
  guarded $O/$run $run.log run.mac
done
$PY -B test_ccal.py scan $EX $O
