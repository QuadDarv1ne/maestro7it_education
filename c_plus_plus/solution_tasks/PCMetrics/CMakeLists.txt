cmake_minimum_required(VERSION 3.10)
project(PCMetrics VERSION 1.0.0 DESCRIPTION "PC Metrics Monitoring Tool")

# Установка стандарта C++
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Включаемые директории
include_directories(${PROJECT_SOURCE_DIR}/include)

# Автоматический поиск всех исходников в src
file(GLOB SOURCES
    "${PROJECT_SOURCE_DIR}/src/*.cpp"
)

# Создание исполняемого файла
add_executable(pcmetrics ${SOURCES})

# Линковка библиотек Windows
if(WIN32)
    target_link_libraries(pcmetrics pdh)
endif()

# Опции сборки
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

# Установка
install(TARGETS pcmetrics DESTINATION bin)

# Опциональная поддержка NVIDIA NVML
option(ENABLE_NVML "Enable NVIDIA NVML support" OFF)

if(ENABLE_NVML)
    # Здесь можно добавить пути к библиотекам NVML если они установлены
    target_compile_definitions(pcmetrics PRIVATE ENABLE_NVML)
    message(STATUS "NVIDIA NVML support enabled")
else()
    message(STATUS "NVIDIA NVML support disabled")
endif()