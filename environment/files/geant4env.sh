# Environment for Geant4 11.4.3 (~/hep/geant4-11.4.3) on this Mac. Source it (bash or zsh) before building or running a
# Geant4 application, or before using geant4_pybind from conda env g4. See QFTcalculation/environment/environment.pdf.
G4HOME="$HOME/hep/geant4-11.4.3"
. "$G4HOME/bin/geant4.sh"   # PATH (geant4-config) and GEANT4_DATA_DIR (the 13 data sets; geant4_pybind then never offers to download them)
# CMake: Geant4, and Qt 6 from conda env g4. Only its lib/cmake is added, so that expat, zlib, ... still come from macOS.
export CMAKE_PREFIX_PATH="$G4HOME:$HOME/miniforge3/envs/g4/lib/cmake${CMAKE_PREFIX_PATH:+:$CMAKE_PREFIX_PATH}"
export CC=/usr/bin/clang CXX=/usr/bin/clang++   # Apple clang, as for the Geant4 build (the MESA SDK's gcc is first in PATH)
export SDKROOT="$(env -u SDKROOT xcrun --show-sdk-path)"   # the default SDK, as for the Geant4 build (with MESA's SDKROOT set, xcrun returns the 14.5 SDK)
unset G4HOME
