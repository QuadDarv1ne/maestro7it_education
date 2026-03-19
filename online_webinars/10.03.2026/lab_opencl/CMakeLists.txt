# =============================================================================
# CMakeLists.txt для проекта "Вычисления на GPU с OpenCL"
# =============================================================================
# Лабораторная работа по использованию технологий вычислений на GPU
# 
# Требования:
#   - CMake 3.10 или выше
#   - Компилятор C (gcc, clang, MSVC)
#   - OpenCL SDK/драйверы
#
# Сборка:
#   mkdir build && cd build
#   cmake ..
#   cmake --build .
#
# Запуск тестов:
#   ctest --verbose
#
# Установка (опционально):
#   cmake --install . --prefix /usr/local
# =============================================================================

cmake_minimum_required(VERSION 3.10)
project(GPU_Lab 
    VERSION 1.1.0
    DESCRIPTION "Лабораторная работа: Вычисления на GPU с OpenCL"
    LANGUAGES C
)

# =============================================================================
# Опции сборки
# =============================================================================
option(BUILD_TESTS "Сборка тестов" ON)
option(BUILD_BENCHMARKS "Сборка бенчмарков" ON)
option(ENABLE_PROFILING "Включить профилирование" ON)
option(USE_STATIC_ANALYSIS "Включить статический анализ" OFF)

# =============================================================================
# Поиск зависимостей
# =============================================================================

# Поиск OpenCL
find_package(OpenCL REQUIRED)

if(OpenCL_FOUND)
    message(STATUS "OpenCL найден: ${OpenCL_INCLUDE_DIRS}")
    message(STATUS "OpenCL библиотеки: ${OpenCL_LIBRARIES}")
else()
    message(FATAL_ERROR "OpenCL не найден! Установите OpenCL SDK или драйверы GPU.")
endif()

# Поиск математической библиотеки (требуется на Unix)
find_library(MATH_LIBRARY m)
if(MATH_LIBRARY)
    message(STATUS "Математическая библиотека: ${MATH_LIBRARY}")
else()
    set(MATH_LIBRARY "")
endif()

# Потоки (pthread для Unix)
if(UNIX AND NOT APPLE)
    find_package(Threads REQUIRED)
endif()

# =============================================================================
# Общие настройки компиляции
# =============================================================================

# Стандарт C99
set(CMAKE_C_STANDARD 99)
set(CMAKE_C_STANDARD_REQUIRED ON)

# Пути к заголовочным файлам
include_directories(${PROJECT_SOURCE_DIR}/include)
include_directories(${OpenCL_INCLUDE_DIRS})

# Флаги компиляции
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wall -Wextra")
set(CMAKE_C_FLAGS_DEBUG "-g -O0 -DDEBUG")
set(CMAKE_C_FLAGS_RELEASE "-O3 -DNDEBUG")

# По умолчанию Release сборка
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

message(STATUS "Тип сборки: ${CMAKE_BUILD_TYPE}")

# =============================================================================
# Общие исходные файлы
# =============================================================================

set(COMMON_SOURCES
    ${PROJECT_SOURCE_DIR}/src/cl_utils.c
)

# =============================================================================
# Цели (targets)
# =============================================================================

# -----------------------------------------------------------------------------
# Решето Эратосфена
# -----------------------------------------------------------------------------
add_executable(sieve
    ${PROJECT_SOURCE_DIR}/sieve/sieve.c
    ${COMMON_SOURCES}
)

target_link_libraries(sieve
    ${OpenCL_LIBRARIES}
    ${MATH_LIBRARY}
)

# Для Windows: shlwapi для PathRemoveFileSpec
if(WIN32)
    target_link_libraries(sieve shlwapi)
endif()

target_compile_definitions(sieve PRIVATE
    $<$<BOOL:${ENABLE_PROFILING}>:CL_PROFILING_ENABLED>
)

# -----------------------------------------------------------------------------
# Параллельное хэширование
# -----------------------------------------------------------------------------
add_executable(hash
    ${PROJECT_SOURCE_DIR}/hashing/hash.c
    ${COMMON_SOURCES}
)

target_link_libraries(hash
    ${OpenCL_LIBRARIES}
    ${MATH_LIBRARY}
)

if(UNIX AND NOT APPLE)
    target_link_libraries(hash Threads::Threads)
endif()

# Для Windows: shlwapi для PathRemoveFileSpec
if(WIN32)
    target_link_libraries(hash shlwapi)
endif()

target_compile_definitions(hash PRIVATE
    $<$<BOOL:${ENABLE_PROFILING}>:CL_PROFILING_ENABLED>
)

# =============================================================================
# Тесты
# =============================================================================

if(BUILD_TESTS)
    enable_testing()

    # Unit-тест SHA-256 (использует только sha256.c без main())
    add_executable(test_sha256
        ${PROJECT_SOURCE_DIR}/tests/test_sha256.c
        ${PROJECT_SOURCE_DIR}/hashing/sha256.c
    )
    target_link_libraries(test_sha256
        ${MATH_LIBRARY}
    )
    target_include_directories(test_sha256 PRIVATE ${PROJECT_SOURCE_DIR}/tests)

    # Unit-тест Sieve (использует только sieve_cpu.c без main())
    add_executable(test_sieve
        ${PROJECT_SOURCE_DIR}/tests/test_sieve.c
        ${PROJECT_SOURCE_DIR}/sieve/sieve_cpu.c
    )
    target_link_libraries(test_sieve
        ${MATH_LIBRARY}
    )
    target_include_directories(test_sieve PRIVATE ${PROJECT_SOURCE_DIR}/tests)

    # Регистрация тестов в CTest
    add_test(NAME SHA256_Unit_Test COMMAND test_sha256)
    add_test(NAME Sieve_Unit_Test COMMAND test_sieve)

    # Интеграционные тесты через запуск основных программ
    # Примечание: unit-тесты требуют рефакторинга для разделения main() и функций
    
    # Интеграционный тест: проверка работы hashing
    add_test(NAME Hash_Integration_Test COMMAND hash 10000 64 256)

    # Интеграционный тест: проверка работы sieve
    add_test(NAME Sieve_Integration_Test COMMAND sieve 1000000 256)
endif()

# =============================================================================
# Бенчмарки (дополнительные цели)
# =============================================================================

if(BUILD_BENCHMARKS)
    # Цель для запуска всех бенчмарков
    add_custom_target(benchmarks
        DEPENDS sieve hash
        COMMENT "Бенчмарки собраны. Запустите './sieve --bench' или './hash --bench'"
    )
endif()

# =============================================================================
# Статический анализ (опционально)
# =============================================================================

if(USE_STATIC_ANALYSIS)
    find_program(CLANG_TIDY_EXE clang-tidy)
    if(CLANG_TIDY_EXE)
        message(STATUS "clang-tidy найден: ${CLANG_TIDY_EXE}")
        set(CMAKE_C_CLANG_TIDY ${CLANG_TIDY_EXE})
    else()
        message(WARNING "clang-tidy не найден, статический анализ отключен")
    endif()
endif()

# =============================================================================
# Установка (install)
# =============================================================================

install(TARGETS sieve hash
    RUNTIME DESTINATION bin
)

install(FILES
    ${PROJECT_SOURCE_DIR}/sieve/sieve.cl
    ${PROJECT_SOURCE_DIR}/hashing/hash.cl
    DESTINATION share/gpu_lab/kernels
)

install(FILES ${PROJECT_SOURCE_DIR}/README.md
    DESTINATION share/doc/gpu_lab
)

# Копирование kernel файлов в директорию сборки для отладки
# Это нужно для того, чтобы программы могли найти .cl файлы при запуске из build/
file(COPY ${PROJECT_SOURCE_DIR}/sieve/sieve.cl
     DESTINATION ${CMAKE_BINARY_DIR}/)
file(COPY ${PROJECT_SOURCE_DIR}/hashing/hash.cl
     DESTINATION ${CMAKE_BINARY_DIR}/)

# =============================================================================
# Вывод информации о сборке
# =============================================================================

message(STATUS "")
message(STATUS "=============================================")
message(STATUS "GPU Lab - сводка конфигурации")
message(STATUS "=============================================")
message(STATUS "  Версия проекта:    ${PROJECT_VERSION}")
message(STATUS "  Тип сборки:        ${CMAKE_BUILD_TYPE}")
message(STATUS "  OpenCL:            ${OpenCL_LIBRARIES}")
message(STATUS "  Сборка тестов:     ${BUILD_TESTS}")
message(STATUS "  Сборка бенчмарков: ${BUILD_BENCHMARKS}")
message(STATUS "  Профилирование:    ${ENABLE_PROFILING}")
message(STATUS "  Стат. анализ:      ${USE_STATIC_ANALYSIS}")
message(STATUS "=============================================")
message(STATUS "")
