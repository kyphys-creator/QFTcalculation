#!/bin/bash
# Geant4 11.4.3 (environment.pdf): the distributed examples against the reference outputs that come with them
# (made by the Geant4 team with 11.4.3 and the serial run manager), the data files, and known values.
#   1. geant4-config: version, multithreading and its TLS model, Qt; the 13 data sets on disk
#   2. builds B1, TestEm0, Hadr00 and rdecay01 from the installed examples into out/build
#   3. TestEm0 (TestEm0.in, serial): EM cross sections, stopping powers and ranges from G4EmCalculator, no random
#      numbers: every number against TestEm0.out
#   4. Hadr00 (hadr00.in, FTFP_BERT, serial): the 800-bin cross-section table of p on Al against hadr00.out;
#      hadr00_thermal.mac: neutron capture at 0.0253 eV with QGSP_BIC_HP (G4NDL) against the G4NDL file and the Atlas of
#      Neutron Resonances, and with QGSP_BIC; hadr00_tendl.mac: p + Al with QGSP_BIC_AllHP (G4TENDL) against the
#      G4TENDL file, and with QGSP_BIC
#   5. B1 (exampleB1.in): the dose of 10000 6 MeV gammas and of 10000 210 MeV protons, serial and with 8 threads,
#      against exampleB1.out within the statistical errors
#   6. rdecay01 (rdecay01.in, serial): the particle counts of each run against rdecay01.out; Co60's half-life and
#      branching against ENSDF
#   7. geant4_pybind (conda env g4): TestEm0's numbers recomputed from Python, against step 3's C++ run, and 100 events
#   8. with --hepmc only: the stage-3 LHC events through HepMCEx02 (hepmc/run_hepmc.sh: the imported primaries against
#      the HepMC file, the e+- in the 3 T field against own helix; about 4 minutes; needs ../lhc/out from run_stage3.sh)
#   9. with --qt only: B1's geometry and 10 events in the Qt session (an OpenGL and a ToolsSG viewer), exported to out/qt/qt_ogl_0000.png, qt_tsg.png;
#      the window opens on the screen for about 12 s and closes itself
# Output in ./out.  About 35 s (the first run of each new executable takes about 10 s longer: macOS scans it).
cd "$(dirname "$0")"
HERE=$(pwd)
QT=0; HEPMC=0
for a in "$@"; do [ "$a" = --qt ] && QT=1; [ "$a" = --hepmc ] && HEPMC=1; done
G4=$HOME/hep/geant4-11.4.3
EX=$G4/share/Geant4/examples
source ~/hep/opt/geant4env.sh   # geant4.sh, CMAKE_PREFIX_PATH with Qt, Apple clang, default SDK
PY=~/miniforge3/envs/qft/bin/python
mkdir -p out/build out/run

echo "geant4-config: $(geant4-config --version); multithreading $(geant4-config --has-feature multithreading)" \
     "(TLS model $(grep -o 'geant4_tls_model="[^"]*"' $G4/bin/geant4-config | head -1 | cut -d'"' -f2)), qt $(geant4-config --has-feature qt)"
echo "data sets: $(geant4-config --check-datasets | grep -c INSTALLED) of $(geant4-config --datasets | wc -l | tr -d ' ') installed"
geant4-config --check-datasets | grep -v INSTALLED

build () {   # build <name> <path under examples/>
  (cmake -S "$EX/$2" -B "out/build/$1" -DCMAKE_BUILD_TYPE=Release > "out/build/$1.cmake.log" 2>&1 &&
   cmake --build "out/build/$1" -j 4 > "out/build/$1.make.log" 2>&1) || { echo "build of $1 failed: out/build/$1.*.log"; exit 1; }
}
build B1 basic/B1
build TestEm0 extended/electromagnetic/TestEm0
build Hadr00 extended/hadronic/Hadr00
build rdecay01 extended/radioactivedecay/rdecay01
echo "built B1, TestEm0, Hadr00, rdecay01"

run () {     # run <name> <log> [args...]: in its build directory, which has the example's macros
  local name=$1 log=$2 exe=$1; shift 2
  [ "$name" = B1 ] && exe=exampleB1
  (cd "out/build/$name" && "./$exe" "$@") > "out/run/$log" 2>&1 || echo "$name $* failed: out/run/$log"
}
export G4FORCE_RUN_MANAGER_TYPE=Serial
run TestEm0 TestEm0.out TestEm0.in
$PY test_geant4.py table TestEm0 out/run/TestEm0.out "$EX/extended/electromagnetic/TestEm0/TestEm0.out" "### Run 0 starts"

run Hadr00 hadr00.out hadr00.in
$PY test_geant4.py table Hadr00 out/run/hadr00.out "$EX/extended/hadronic/Hadr00/hadr00.out" "### Fill Cross Sections"
unset G4FORCE_RUN_MANAGER_TYPE
cp hadr00_thermal.mac hadr00_tendl.mac out/build/Hadr00/
run Hadr00 thermal_HP.out hadr00_thermal.mac QGSP_BIC_HP 1
run Hadr00 thermal_noHP.out hadr00_thermal.mac QGSP_BIC 1
$PY test_geant4.py thermal out/run/thermal_HP.out out/run/thermal_noHP.out
run Hadr00 tendl_AllHP.out hadr00_tendl.mac QGSP_BIC_AllHP 1
run Hadr00 tendl_noHP.out hadr00_tendl.mac QGSP_BIC 1
grep -h 'G4ParticleHPInelasticData instantiated for particle proton' out/run/tendl_AllHP.out | sed 's/.*pointing to /QGSP_BIC_AllHP reads protons from /'
$PY test_geant4.py tendl out/run/tendl_AllHP.out out/run/tendl_noHP.out

G4FORCE_RUN_MANAGER_TYPE=Serial run B1 B1_serial.out exampleB1.in
G4FORCENUMBEROFTHREADS=8 run B1 B1_mt8.out exampleB1.in
echo "B1 with 8 threads: $(grep -c 'End of Local Run' out/run/B1_mt8.out) local runs ended (2 runs x 8 threads)"
$PY test_geant4.py b1 "$EX/basic/B1/exampleB1.out" out/run/B1_serial.out out/run/B1_mt8.out

G4FORCE_RUN_MANAGER_TYPE=Serial run rdecay01 rdecay01.out rdecay01.in
$PY test_geant4.py rdecay01 out/run/rdecay01.out "$EX/extended/radioactivedecay/rdecay01/rdecay01.out"

if ~/miniforge3/envs/g4/bin/python -c "import geant4_pybind" 2> /dev/null; then
  (cd out/run && ~/miniforge3/envs/g4/bin/python "$HERE/test_pybind.py" TestEm0.out) 2>&1 | grep -E '^pybind|Error|G4Exception'
else
  echo "geant4_pybind is not installed in conda env g4"
fi

if [ "$HEPMC" = 1 ]; then
  ./hepmc/run_hepmc.sh
fi

if [ "$QT" = 1 ]; then
  rm -rf out/qt && mkdir -p out/qt
  (cmake -S qt -B out/qt/build -DCMAKE_BUILD_TYPE=Release -DB1_DIR="$EX/basic/B1" > out/qt/cmake.log 2>&1 &&
   cmake --build out/qt/build -j 4 > out/qt/make.log 2>&1) || { echo "build of qtcheck failed: out/qt/*.log"; exit 1; }
  cp qt/qtcheck.mac out/qt/
  (cd out/qt && ./build/qtcheck > qtcheck.log 2>&1); echo "qtcheck exit status $?"
  grep -E 'Available UI session|viewer-[01] \(|not of type|session closed' out/qt/qtcheck.log | sort -u | head -6
  $PY -c "
import os, matplotlib.image as im, numpy as np
for f in ('qt_ogl_0000.png', 'qt_tsg.png'):
    p = 'out/qt/' + f
    if not os.path.exists(p):
        print(f + ': not written'); continue
    a = im.imread(p)[..., :3]
    print(f'{f}: {a.shape[1]} x {a.shape[0]} pixels, {len(np.unique(a.reshape(-1, 3), axis=0))} colours')"
fi
