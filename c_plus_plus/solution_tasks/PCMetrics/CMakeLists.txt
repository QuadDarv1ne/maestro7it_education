cmake_minimum_required(VERSION 3.10)
project(PCMetrics VERSION 1.0.0)

# Установка стандарта C++
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Включаемые директории
include_directories(${PROJECT_SOURCE_DIR}/include)

# Исходные файлы
set(SOURCES
    src/main.cpp
)

# Создание исполняемого файла
add_executable(pcmetrics ${SOURCES})

# Линковка библиотек Windows
if(WIN32)
    target_link_libraries(pcmetrics pdh)
endif()

# Установка
install(TARGETS pcmetrics DESTINATION bin)