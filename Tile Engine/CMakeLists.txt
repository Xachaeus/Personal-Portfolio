cmake_minimum_required(VERSION 3.26)
project(Winter2024GameProject)

set(CMAKE_CXX_STANDARD 17)

set(SDL2_INCLUDE_DIR C:/Libraries/SDL/include)
set(SDL2_LIB_DIR C:/Libraries/SDL/lib)

include_directories(${SDL2_INCLUDE_DIR})
link_directories(${SDL2_LIB_DIR})

add_executable(Winter2024GameProject
        src/Display.cpp
        src/Display.hpp
        src/main.cpp
        src/Texture.cpp
        src/Texture.hpp
        src/World.cpp
        src/World.hpp
        src/World.cpp
        src/Camera.cpp
        src/Camera.hpp
        src/BoundingBox.cpp
        src/BoundingBox.hpp
        src/Math.cpp
        src/Math.hpp)

target_link_libraries(${PROJECT_NAME} SDL2main SDL2)
