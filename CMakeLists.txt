cmake_minimum_required(VERSION 3.19)

project(sockets_p VERSION 0.1.0 DESCRIPTION "Sockets Programing Practice" LANGUAGES C CXX)


set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(soc_p soc_p)
#find_package(asio REQUIRED)
#find_package(GTest REQUIRED)




add_subdirectory(${CMAKE_CURRENT_LIST_DIR}/source/client)
add_subdirectory(${CMAKE_CURRENT_LIST_DIR}/source/server)

if(${TargetApp})
    add_subdirectory(${CMAKE_CURRENT_LIST_DIR}/c_app)
endif()

if(${EnableTest})
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/tests)
endif()

#! Todo crete the libs vairables here??!!