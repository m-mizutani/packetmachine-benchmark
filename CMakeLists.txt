CMAKE_MINIMUM_REQUIRED(VERSION 2.6)
PROJECT(packetmachine-pref)

IF(NOT CMAKE_BUILD_TYPE)
    message(STATUS "No build type selected, default to Release")
    SET(CMAKE_BUILD_TYPE "Release")
ENDIF()

IF(POLICY CMP0042)
    cmake_policy(SET CMP0042 NEW)
ENDIF()
IF(POLICY CMP0015)
    cmake_policy(SET CMP0015 NEW)
ENDIF()

SET(CMAKE_CXX_FLAGS_RELEASE "-Wall -O3 -std=c++0x")
SET(CMAKE_CXX_FLAGS_DEBUG   "-Wall -O0 -std=c++0x -g -DPACKETMACHINE_DEBUG")
SET(CMAKE_SHARED_LINKER_FLAGS "-lpcap -dynamiclib")

INCLUDE_DIRECTORIES(external/packetmachine/src/)
ADD_SUBDIRECTORY(external/packetmachine)
INCLUDE_DIRECTORIES(external/libtins/include/)
ADD_SUBDIRECTORY(external/libtins)


SET(EXECUTABLE_OUTPUT_PATH ${PROJECT_BINARY_DIR}/bin)
SET(LIBRARY_OUTPUT_PATH ${PROJECT_BINARY_DIR}/lib)

INCLUDE_DIRECTORIES(${INC_DIR} ./src)
LINK_DIRECTORIES(${LIB_DIR})
IF(${CMAKE_SYSTEM_NAME} MATCHES "Darwin")
    INCLUDE_DIRECTORIES(/usr/local/include)
    LINK_DIRECTORIES(/usr/local/lib)
ENDIF()


ADD_EXECUTABLE(pm-task1   "src/task1/pm.cc")
ADD_EXECUTABLE(pm-task2   "src/task2/pm.cc")
ADD_EXECUTABLE(pm-task3   "src/task3/pm.cc")
TARGET_LINK_LIBRARIES(pm-task1 pm-shared)
TARGET_LINK_LIBRARIES(pm-task2 pm-shared)
TARGET_LINK_LIBRARIES(pm-task3 pm-shared)

ADD_EXECUTABLE(tins-task1 "src/task1/tins.cc")
ADD_EXECUTABLE(tins-task2 "src/task2/tins.cc")
TARGET_LINK_LIBRARIES(tins-task1 tins)
TARGET_LINK_LIBRARIES(tins-task2 tins)
