# vlldet (vlldet.hh): the stable-lepton events in a simplified barrel detector, batch (ROOT ntuples) or in the Qt session.
cmake_minimum_required(VERSION 3.16)
project(vlldet CXX)
set(CMAKE_CXX_STANDARD 17)
find_package(Geant4 REQUIRED ui_all vis_all)
include(${Geant4_USE_FILE})
find_package(ZLIB REQUIRED)
add_executable(vlldet vlldet.cc Events.cc Detector.cc Physics.cc Actions.cc)
target_link_libraries(vlldet PRIVATE ${Geant4_LIBRARIES} ZLIB::ZLIB)
