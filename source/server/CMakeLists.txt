set(server server)

add_library(${server} src/server.cpp)
target_include_directories(${server} PUBLIC includes)

set_target_properties(${server} PROPERTIES PUBLIC_HEADER "includes/server.h")
install(TARGETS ${server})