include_directories(${CMAKE_SOURCE_DIR}/src)
add_executable(helloworld helloworld.c)
target_link_libraries(helloworld callback)

