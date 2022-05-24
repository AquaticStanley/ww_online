cmake_minimum_required(VERSION 3.5.0)
project (ww_online)

set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC")

add_subdirectory(External/pybind/pybind11)
add_subdirectory(External/Dolphin-memory-engine/Source)

if(WIN32)
    set(DolphinProcessSrc External/Dolphin-memory-engine/Source/DolphinProcess/Windows/WindowsDolphinProcess.cpp)
endif(WIN32)

if(UNIX)
   set(DolphinProcessSrc External/Dolphin-memory-engine/Source/DolphinProcess/Linux/LinuxDolphinProcess.cpp)
endif(UNIX)

set(LIB_SRCS ${DolphinProcessSrc}
	         External/Dolphin-memory-engine/Source/DolphinProcess/DolphinAccessor.cpp  
	         External/Dolphin-memory-engine/Source/Common/MemoryCommon.cpp
	         External/Dolphin-memory-engine/Source/MemoryScanner/MemoryScanner.cpp)

add_library(dme-library ${LIB_SRCS})

pybind11_add_module(dme dme_bindings.cpp)
target_link_libraries(dme PRIVATE dme-library)
