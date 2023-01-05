cmake_minimum_required(VERSION 3.19)

project(net_template VERSION 0.1.0 DESCRIPTION "network_template" LANGUAGES C CXX)


set(CMAKE_EXPORT_COMPILE_COMMANDS ON)


include (${CMAKE_CURRENT_LIST_DIR}/var.cmake)

include_directories(${CMAKE_SOURCE_DIR}/global_includes)
set(CMAKE_CXX_STANDARD 20)


add_subdirectory(${CMAKE_CURRENT_LIST_DIR}/source/client)
add_subdirectory(${CMAKE_CURRENT_LIST_DIR}/source/server)

if(${TargetApp})
    add_subdirectory(${CMAKE_CURRENT_LIST_DIR}/c_app)
endif()

if(${EnableTest})   
   add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/tests)
endif()

#! Todo crete the libs vairables here??!!