# Qt check of the Geant4 11.4.3 build (run_geant4.sh --qt): example B1's geometry and actions with qtcheck.cc as main.
# B1_DIR = the installed example (~/hep/geant4-11.4.3/share/Geant4/examples/basic/B1).
cmake_minimum_required(VERSION 3.16)
project(qtcheck)
find_package(Geant4 REQUIRED ui_all vis_all)
find_package(Qt6 REQUIRED COMPONENTS Core Widgets)
file(GLOB sources ${B1_DIR}/src/*.cc)
add_executable(qtcheck qtcheck.cc ${sources})
target_include_directories(qtcheck PRIVATE ${B1_DIR}/include)
target_link_libraries(qtcheck PRIVATE ${Geant4_LIBRARIES} Qt6::Core Qt6::Widgets)
