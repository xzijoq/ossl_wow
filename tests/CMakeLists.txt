

set(tst g_tst)
find_package(GTest REQUIRED)
add_executable(${tst} clientTest.cpp serverTest.cpp)
target_link_libraries(${tst} client server GTest::GTest)