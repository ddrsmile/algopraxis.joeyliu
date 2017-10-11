cmake_minimum_required(VERSION 3.8)
project(parser)
set(CMAKE_BUILD_TYPE Release)
set(CMAKE_CXX_STANDARD 11)
#set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_HOME_DIRECTORY}/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_HOME_DIRECTORY}/lib)

include_directories(include)

#add_library(parser SHARED "src/Factory.cpp")
add_library(parser STATIC "src/Factory.cpp")