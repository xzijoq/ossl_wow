set(server server)
find_package(asio REQUIRED)

add_library(${server} src/server.cpp)
target_include_directories(${server} PUBLIC includes)
target_link_libraries(${server} PUBLIC asio::asio)

set_target_properties(${server} PROPERTIES PUBLIC_HEADER "includes/server.h")
install(TARGETS ${server})
