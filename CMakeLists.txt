cmake_minimum_required(VERSION 3.5.0)
project (ww_online)

add_subdirectory(External/pybind/pybind11)
add_subdirectory(External/Dolphin-memory-engine/Source)

add_executable(ww_online main.cpp)
target_link_libraries(ww_online PRIVATE dme-library)

pybind11_add_module(dme dme_bindings.cpp)
target_link_libraries(dme PRIVATE dme-library)
