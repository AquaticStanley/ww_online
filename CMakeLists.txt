cmake_minimum_required(VERSION 3.5.0)
project (ww_online)

add_subdirectory(External/Dolphin-memory-engine/Source)
add_executable(ww_online main.cpp)
