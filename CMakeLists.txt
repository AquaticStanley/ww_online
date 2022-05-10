project (ww_online)
cmake_minimum_required(VERSION 3.1)

add_subdirectory(External)


ADD_EXECUTABLE(ww_online main.cpp)

target_link_libraries(ww_online PUBLIC DME_LIBRARY)
