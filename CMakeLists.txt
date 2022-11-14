cmake_minimum_required(VERSION 3.19)

project(sockets_p VERSION 0.1.0 DESCRIPTION "Sockets Programing Practice" LANGUAGES C CXX)


set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(soc_p soc_p)

add_subdirectory(${CMAKE_CURRENT_LIST_DIR}/source/client)
add_subdirectory(${CMAKE_CURRENT_LIST_DIR}/source/server)
add_subdirectory(${CMAKE_CURRENT_LIST_DIR}/c_app)