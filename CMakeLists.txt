project (ww_online)
cmake_minimum_required(VERSION 3.1)

find_library(MEMORY_ENGINE dme)

ADD_LIBRARY(DolphinAccess
	dolphin_access.cpp
)

target_link_libraries(DolphinAccess MEMORY_ENGINE)
ADD_EXECUTABLE(ww_online main.cpp)
target_link_libraries(ww_online DolphinAccess)