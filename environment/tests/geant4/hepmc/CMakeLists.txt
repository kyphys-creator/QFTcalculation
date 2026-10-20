# The stage-3 LHC events through Geant4's example HepMCEx02 (run_hepmc.sh): the example's sources from the installed
# examples (EX_DIR) with H02EventAction.cc and H02SteppingAction.cc replaced by the ones here, which write the imported
# primaries and the entry points of the primary e+- into the barrel calorimeter.  HEPMC_DIR: HepMC 2.06.09 of MG5's HEPTools.
cmake_minimum_required(VERSION 3.16)
project(HepMCEx02check)
find_package(Geant4 REQUIRED ui_all vis_all)
include(${Geant4_USE_FILE})     # also puts Geant4's Modules (FindHepMC.cmake) on CMAKE_MODULE_PATH
find_package(HepMC REQUIRED)
file(GLOB sources ${EX_DIR}/src/*.cc)
list(FILTER sources EXCLUDE REGEX "/H02(EventAction|SteppingAction)\\.cc$")
add_executable(HepMCEx02 ${EX_DIR}/HepMCEx02.cc ${sources} H02EventAction.cc H02SteppingAction.cc)
target_include_directories(HepMCEx02 PRIVATE ${EX_DIR}/include ${HEPMC_INCLUDE_DIR})
target_link_libraries(HepMCEx02 PRIVATE ${Geant4_LIBRARIES} ${HEPMC_LIBRARIES} ${HEPMC_FIO_LIBRARIES})
set_target_properties(HepMCEx02 PROPERTIES BUILD_RPATH ${HEPMC_LIBRARY_DIR})
