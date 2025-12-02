cmake_minimum_required(VERSION 3.10)
project(PCMetrics VERSION 1.0.0 DESCRIPTION "PC Metrics Monitoring Tool" LANGUAGES CXX)

# Установка стандарта C++
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Опции компиляции
if(MSVC)
    add_compile_options(/W4 /WX- /utf-8)
    # Отключаем предупреждения о небезопасных функциях
    add_compile_definitions(_CRT_SECURE_NO_WARNINGS)
else()
    add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Включение режима отладки по умолчанию
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Debug)
endif()

message(STATUS "Build type: ${CMAKE_BUILD_TYPE}")

# Включаемые директории
include_directories(${PROJECT_SOURCE_DIR}/include)

# Директории для дополнительных библиотек
set(LIBS_DIR ${PROJECT_SOURCE_DIR}/libs)

# Опциональные включаемые директории для GPU библиотек
if(EXISTS ${LIBS_DIR}/nvml)
    include_directories(${LIBS_DIR}/nvml)
endif()
if(EXISTS ${LIBS_DIR}/adl)
    include_directories(${LIBS_DIR}/adl)
endif()
if(EXISTS ${LIBS_DIR}/intel)
    include_directories(${LIBS_DIR}/intel)
endif()

# Автоматический поиск всех исходников в src
file(GLOB SOURCES
    "${PROJECT_SOURCE_DIR}/src/*.cpp"
)

# Создание исполняемого файла
add_executable(pcmetrics ${SOURCES})

# Линковка библиотек Windows
if(WIN32)
    target_link_libraries(pcmetrics PRIVATE pdh iphlpapi)
    message(STATUS "Linking Windows PDH and IPHLPAPI libraries")
endif()

# Опции сборки
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

# Установка
install(TARGETS pcmetrics DESTINATION bin)

# Опциональная поддержка NVIDIA NVML
option(ENABLE_NVML "Enable NVIDIA NVML support" OFF)
if(ENABLE_NVML)
    # Проверяем наличие библиотек NVML
    if(EXISTS ${LIBS_DIR}/nvml/nvml.lib)
        target_link_libraries(pcmetrics ${LIBS_DIR}/nvml/nvml.lib)
        message(STATUS "NVIDIA NVML library found and linked")
    else()
        message(WARNING "NVIDIA NVML library not found in libs/nvml/")
    endif()
    target_compile_definitions(pcmetrics PRIVATE ENABLE_NVML)
    message(STATUS "NVIDIA NVML support enabled")
else()
    message(STATUS "NVIDIA NVML support disabled")
endif()

# Опциональная поддержка AMD ADL
option(ENABLE_ADL "Enable AMD ADL support" OFF)
if(ENABLE_ADL)
    # Проверяем наличие библиотек ADL
    if(EXISTS ${LIBS_DIR}/adl/ADL.lib)
        target_link_libraries(pcmetrics ${LIBS_DIR}/adl/ADL.lib)
        message(STATUS "AMD ADL library found and linked")
    else()
        message(WARNING "AMD ADL library not found in libs/adl/")
    endif()
    target_compile_definitions(pcmetrics PRIVATE ENABLE_ADL)
    message(STATUS "AMD ADL support enabled")
else()
    message(STATUS "AMD ADL support disabled")
endif()

# Опциональная поддержка Intel GPA
option(ENABLE_INTEL_GPA "Enable Intel GPA support" OFF)
if(ENABLE_INTEL_GPA)
    # Проверяем наличие библиотек Intel GPA
    if(EXISTS ${LIBS_DIR}/intel/igpa.lib)
        target_link_libraries(pcmetrics ${LIBS_DIR}/intel/igpa.lib)
        message(STATUS "Intel GPA library found and linked")
    else()
        message(WARNING "Intel GPA library not found in libs/intel/")
    endif()
    target_compile_definitions(pcmetrics PRIVATE ENABLE_INTEL_GPA)
    message(STATUS "Intel GPA support enabled")
else()
    message(STATUS "Intel GPA support disabled")
endif()

# Создание тестового исполняемого файла
add_executable(pcmetrics_test 
    ${PROJECT_SOURCE_DIR}/tests/simple_test.cpp
    ${PROJECT_SOURCE_DIR}/src/logger.cpp
    ${PROJECT_SOURCE_DIR}/src/memory_monitor.cpp
    ${PROJECT_SOURCE_DIR}/src/cpu_monitor.cpp
    ${PROJECT_SOURCE_DIR}/src/disk_monitor.cpp
    ${PROJECT_SOURCE_DIR}/src/network_monitor.cpp
)
target_link_libraries(pcmetrics_test PRIVATE pdh iphlpapi)

# Копируем заголовочные файлы тестового фреймворка
target_include_directories(pcmetrics_test PRIVATE ${PROJECT_SOURCE_DIR}/tests)