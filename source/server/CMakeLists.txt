set(server server)

add_library(${server} src/server.cpp)
target_include_directories(${server} PUBLIC includes)