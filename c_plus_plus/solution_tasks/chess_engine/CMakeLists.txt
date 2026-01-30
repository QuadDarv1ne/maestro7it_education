cmake_minimum_required(VERSION 3.10)
project(ChessEngine VERSION 1.0.0 LANGUAGES CXX)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Compiler-specific flags
if(MSVC)
    add_compile_options(/W4)
    # Add UTF-8 support for MSVC
    add_compile_options(/utf-8)
    add_compile_options(/D_WIN32_WINNT=0x0601)
else()
    add_compile_options(-Wall -Wextra -pedantic)
    # Add UTF-8 encoding support
    add_compile_options(-finput-charset=UTF-8 -fexec-charset=UTF-8)
endif()

# Add Windows-specific definitions for encoding
if(WIN32)
    add_definitions(-DUNICODE -D_UNICODE)
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
    src/engine/opening_book.cpp
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

# Only add test executables if the source files exist
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/src/encoding_test.cpp")
    add_executable(encoding_test src/encoding_test.cpp)
endif()

if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/src/utf8_test.cpp")
    add_executable(utf8_test src/utf8_test.cpp)
endif()

if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/src/test_chess.cpp")
    add_executable(test_chess src/test_chess.cpp src/board/board.cpp src/board/piece.cpp src/logic/move_generator.cpp src/logic/game_rules.cpp src/ui/console_ui.cpp ${HEADERS})
endif()

if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/src/comprehensive_test.cpp")
    add_executable(comprehensive_test src/comprehensive_test.cpp src/board/board.cpp src/board/piece.cpp src/logic/move_generator.cpp src/logic/game_rules.cpp ${HEADERS})
endif()

# Include directories
target_include_directories(chess_engine PRIVATE include)

# Platform-specific settings
if(WIN32)
    target_compile_definitions(chess_engine PRIVATE WIN32_CONSOLE)
endif()