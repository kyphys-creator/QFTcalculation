# fcalview (run_fcalview.sh): Geant4's example advanced/lAr_calorimeter (EX_DIR) with fcalview.cc as main, to look at
# showers in the ATLAS FCAL in the Qt session.
cmake_minimum_required(VERSION 3.16)
project(fcalview)
find_package(Geant4 REQUIRED ui_all vis_all)
include(${Geant4_USE_FILE})
find_package(Qt6 REQUIRED COMPONENTS Core Widgets)
file(GLOB sources ${EX_DIR}/src/*.cc)
add_executable(fcalview fcalview.cc ${sources})
target_include_directories(fcalview PRIVATE ${EX_DIR}/include ${EX_DIR}/src)   # src: the *.input parameter files
target_link_libraries(fcalview PRIVATE ${Geant4_LIBRARIES} Qt6::Core Qt6::Widgets)
