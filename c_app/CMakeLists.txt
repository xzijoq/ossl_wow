
find_package(asio REQUIRED)
find_package(botan REQUIRED)


add_executable(c_app main.cpp)
target_link_libraries(c_app PRIVATE client server asio::asio  botan::botan)
#target_compile_options(c_app PRIVATE -g -o0 -Wall )

add_executable(c_client c_client.cpp)
target_link_libraries(c_client PRIVATE client server)
#target_compile_options(c_client PRIVATE -g -o0 -Wall )

add_executable(c_server c_server.cpp)
target_link_libraries(c_server PRIVATE client server)
#target_compile_options(c_server PRIVATE -g -o0 -Wall )




#http://127.0.0.1:5000/