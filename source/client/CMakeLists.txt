set(client client)

add_library(${client} src/client.cpp)
target_include_directories(${client} PUBLIC includes)