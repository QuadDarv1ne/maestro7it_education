cmake_minimum_required(VERSION 3.10)
project(ChessEngine VERSION 1.0.0 LANGUAGES CXX)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Compiler-specific flags
if(MSVC)
    add_compile_options(/W4)
else()
    add_compile_options(-Wall -Wextra -pedantic)
endif()

# Source files
set(SOURCES
    src/main.cpp
    src/board/board.cpp
    src/board/piece.cpp
    src/logic/move_generator.cpp
    src/logic/game_rules.cpp
    src/engine/minimax.cpp
    src/engine/position_evaluator.cpp
    src/ui/console_ui.cpp
)

# Header files
set(HEADERS
    include/board.hpp
    include/piece.hpp
    include/move_generator.hpp
    include/game_rules.hpp
    include/minimax.hpp
    include/position_evaluator.hpp
    include/console_ui.hpp
)

# Create executables
add_executable(chess_engine ${SOURCES} ${HEADERS})
add_executable(test_chess src/test_chess.cpp src/board/board.cpp src/board/piece.cpp src/logic/move_generator.cpp src/logic/game_rules.cpp src/ui/console_ui.cpp ${HEADERS})
add_executable(comprehensive_test src/comprehensive_test.cpp src/board/board.cpp src/board/piece.cpp src/logic/move_generator.cpp src/logic/game_rules.cpp ${HEADERS})

# Include directories
target_include_directories(chess_engine PRIVATE include)

# Platform-specific settings
if(WIN32)
    target_compile_definitions(chess_engine PRIVATE WIN32_CONSOLE)
endif()