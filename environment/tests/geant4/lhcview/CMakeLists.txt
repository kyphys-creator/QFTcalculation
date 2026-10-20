# lhcview (run_lhcview.sh): Geant4's example HepMCEx02 (EX_DIR) with lhcview.cc as main, to look at the stage-3 LHC events
# in the Qt session.  HEPMC_DIR: HepMC 2.06.09 of MG5's HEPTools.
cmake_minimum_required(VERSION 3.16)
project(lhcview)
find_package(Geant4 REQUIRED ui_all vis_all)
include(${Geant4_USE_FILE})
find_package(HepMC REQUIRED)
file(GLOB sources ${EX_DIR}/src/*.cc)
add_executable(lhcview lhcview.cc ${sources})
target_include_directories(lhcview PRIVATE ${EX_DIR}/include ${HEPMC_INCLUDE_DIR})
target_link_libraries(lhcview PRIVATE ${Geant4_LIBRARIES} ${HEPMC_LIBRARIES} ${HEPMC_FIO_LIBRARIES})
set_target_properties(lhcview PROPERTIES BUILD_RPATH ${HEPMC_LIBRARY_DIR})
