add_executable(c_app main.cpp)
target_link_libraries(c_app PRIVATE client server)
target_compile_options(c_app PRIVATE -g -o0 -Wall )

#http://127.0.0.1:5000/