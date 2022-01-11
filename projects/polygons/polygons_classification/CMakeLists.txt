cmake_minimum_required(VERSION 3.0.0)

project(classify_polygons VERSION 0.1)
set (CMAKE_CXX_STANDARD 17)

add_executable (${PROJECT_NAME} "classify_polygons.cpp")

set(OpenCV_LIBS opencv_core opencv_imgproc opencv_calib3d opencv_video opencv_features2d opencv_ml opencv_highgui opencv_objdetect)

set(OpenCV_DIR $ENV{OpenCV_HOME}/build/${CMAKE_BUILD_TYPE}/install)
set(OpenCV_INCLUDE_DIRS ${OpenCV_DIR}/include)
set(OpenCV_LIBS_DIR ${OpenCV_DIR}/x64/vc16/lib)

find_package(OpenCV REQUIRED)
add_library(OpenCV STATIC IMPORTED)
include_directories(${OpenCV_INCLUDE_DIRS})
link_directories(${OpenCV_LIBS_DIR})

TARGET_LINK_LIBRARIES(${PROJECT_NAME} ${OpenCV_LIBS})

set_target_properties(${PROJECT_NAME} PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/build/${CMAKE_BUILD_TYPE} )
