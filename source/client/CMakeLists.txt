set(client client)

find_package(asio REQUIRED)
add_library(${client} src/client.cpp)
target_include_directories(${client} PUBLIC includes)
target_link_libraries(${client} PUBLIC asio::asio)


set_target_properties(${client} PROPERTIES PUBLIC_HEADER "includes/client.h")
install(TARGETS ${client})