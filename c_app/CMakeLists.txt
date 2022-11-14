add_executable(c_app main.cpp)
target_link_libraries(c_app PRIVATE client server)