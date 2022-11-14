set(client client)

add_library(${client} src/client.cpp)
target_include_directories(${client} PUBLIC includes)

set_target_properties(${client} PROPERTIES PUBLIC_HEADER "includes/client.h")
install(TARGETS ${client})