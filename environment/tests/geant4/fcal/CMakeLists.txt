# Geant4's example advanced/lAr_calorimeter (the ATLAS FCAL in its test beam) for run_fcal.sh: the example's sources from
# the installed examples (EX_DIR), with FCALEMModuleSD.cc replaced by the one here (it also prints FCAL1's visible energy).
cmake_minimum_required(VERSION 3.16)
project(lArCalCheck)
find_package(Geant4 REQUIRED ui_all vis_all)
include(${Geant4_USE_FILE})
file(GLOB sources ${EX_DIR}/src/*.cc)
list(FILTER sources EXCLUDE REGEX "/FCALEMModuleSD\\.cc$")
add_executable(lArCal ${EX_DIR}/lArCal.cc ${sources} FCALEMModuleSD.cc)
target_include_directories(lArCal PRIVATE ${EX_DIR}/include ${EX_DIR}/src)   # src: the *.input parameter files
target_link_libraries(lArCal PRIVATE ${Geant4_LIBRARIES})
