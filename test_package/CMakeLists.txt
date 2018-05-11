# Test for easy_profiler Conan package
# Dmitriy Vetutnev, Odant, 2018


project(PackageTest CXX)
cmake_minimum_required(VERSION 3.0)


include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)


enable_testing()

# easy_profiler imported targets

find_package(easy_profiler REQUIRED)
if(EASY_PROFILER_STUB_MODE)
    find_package(Threads)
endif()

add_executable(example example.cpp)
target_link_libraries(example easy_profiler)
if(EASY_PROFILER_STUB_MODE)
    target_link_libraries(example Threads::Threads)
endif()
add_test(
    NAME example
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/bin
    COMMAND example
)
set_property(TEST example PROPERTY TIMEOUT 30)


# CONAN_PKG imported targets

add_executable(example_CONAN_PKG example.cpp)
target_link_libraries(example_CONAN_PKG CONAN_PKG::easy_profiler)
if(EASY_PROFILER_STUB_MODE)
    target_link_libraries(example_CONAN_PKG Threads::Threads)
endif()
add_test(
    NAME example_CONAN_PKG
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/bin
    COMMAND example_CONAN_PKG
)
set_property(TEST example_CONAN_PKG PROPERTY TIMEOUT 30)


