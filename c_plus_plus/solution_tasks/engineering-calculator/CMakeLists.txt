cmake_minimum_required(VERSION 3.14)
project(EngineeringCalculator LANGUAGES CXX)

# Требуем C++17 (для std::stod, удобства и совместимости)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Источники
set(SOURCES
    main.cpp
    Calculator.cpp
    Tokenizer.cpp
)

# Создаём исполняемый файл
add_executable(calc ${SOURCES})

# Подключаем математическую библиотеку (на некоторых системах, например, Linux, требуется явно)
target_link_libraries(calc PRIVATE m)

# Опционально: включаем предупреждения
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    target_compile_options(calc PRIVATE -Wall -Wextra -Wpedantic)
endif()