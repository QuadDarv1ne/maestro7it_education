# =============================================================================
# CMakeLists.txt — Проект "Вычисления на GPU с OpenCL"
# =============================================================================
# Версия: 1.1.0
# 
# Требования:
#   - CMake 3.16 или выше
#   - Компилятор C с поддержкой C99
#   - OpenCL 1.2+ SDK/драйверы
#
# Сборка:
#   mkdir build && cd build
#   cmake .. -DCMAKE_BUILD_TYPE=Release
#   cmake --build .
#
# Установка:
#   cmake --install . --prefix /usr/local
#
# Запуск тестов:
#   ctest --verbose
# =============================================================================

cmake_minimum_required(VERSION 3.16)

# =============================================================================
# Проект
# =============================================================================
project(GPU_Lab
    VERSION 1.1.0
    DESCRIPTION "Лабораторная работа: Вычисления на GPU с OpenCL"
    HOMEPAGE_URL "https://github.com/your-repo/gpu-lab"
    LANGUAGES C
)

# =============================================================================
# Опции сборки
# =============================================================================
option(BUILD_SHARED_LIBS "Сборка общих библиотек" OFF)
option(BUILD_TESTS "Сборка тестов" ON)
option(BUILD_BENCHMARKS "Сборка бенчмарков" ON)
option(ENABLE_PROFILING "Включить профилирование" ON)
option(USE_STATIC_ANALYSIS "Включить статический анализ" OFF)
option(ENABLE_COVERAGE "Включить покрытие кода" OFF)
option(INSTALL_DOCS "Установка документации" ON)

# =============================================================================
# Глобальные настройки
# =============================================================================
set(CMAKE_C_STANDARD 99)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS OFF)

# Позиционно-независимый код
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# Экспорт символов
set(CMAKE_C_VISIBILITY_PRESET hidden)
set(CMAKE_VISIBILITY_INLINES_HIDDEN ON)

# Пути
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

# =============================================================================
# Поиск зависимостей
# =============================================================================

# OpenCL через pkg-config (предпочтительно)
find_package(PkgConfig QUIET)
if(PkgConfig_FOUND)
    pkg_check_modules(OPENCL OpenCL)
endif()

# Fallback на стандартный поиск
if(NOT OPENCL_FOUND)
    find_package(OpenCL REQUIRED)
endif()

message(STATUS "OpenCL найден: ${OpenCL_INCLUDE_DIRS}")
message(STATUS "OpenCL версии: ${OpenCL_VERSION}")

# Математическая библиотека
find_library(MATH_LIBRARY m)
if(NOT MATH_LIBRARY)
    set(MATH_LIBRARY "")
endif()

# Потоки
find_package(Threads REQUIRED)

# =============================================================================
# Определение флагов компиляции
# =============================================================================
if(CMAKE_C_COMPILER_ID MATCHES "GNU|Clang")
    add_compile_options(
        -Wall
        -Wextra
        -Wpedantic
        -Wshadow
        -Wconversion
        -Wsign-conversion
        -Wnull-dereference
        -Wdouble-promotion
        -Wformat=2
    )
    
    if(CMAKE_BUILD_TYPE STREQUAL "Debug")
        add_compile_options(-g3 -O0 -DDEBUG)
        add_compile_options(-fno-omit-frame-pointer)
        if(ENABLE_COVERAGE)
            add_compile_options(--coverage -fprofile-arcs -ftest-coverage)
            add_link_options(--coverage)
        endif()
    else()
        add_compile_options(-O3 -DNDEBUG)
        if(CMAKE_C_COMPILER_ID STREQUAL "GNU")
            add_compile_options(-flto)
            add_link_options(-flto)
        endif()
    endif()
    
elseif(MSVC)
    add_compile_options(/W4 /WX- /permissive-)
    if(CMAKE_BUILD_TYPE STREQUAL "Debug")
        add_compile_options(/Od /Zi)
    else()
        add_compile_options(/O2 /GL)
        add_link_options(/LTCG)
    endif()
endif()

# =============================================================================
# Исходные файлы
# =============================================================================
set(COMMON_SOURCES
    ${CMAKE_SOURCE_DIR}/src/cl_utils.c
)

set(COMMON_HEADERS
    ${CMAKE_SOURCE_DIR}/include/cl_common.h
)

# =============================================================================
# Цели: sieve
# =============================================================================
add_executable(sieve 
    ${CMAKE_SOURCE_DIR}/sieve/sieve.c
    ${COMMON_SOURCES}
)

target_include_directories(sieve PRIVATE
    ${CMAKE_SOURCE_DIR}/include
    ${OpenCL_INCLUDE_DIRS}
)

target_link_libraries(sieve PRIVATE
    ${OpenCL_LIBRARIES}
    ${MATH_LIBRARY}
)

target_compile_definitions(sieve PRIVATE
    $<$<BOOL:${ENABLE_PROFILING}>:CL_PROFILING_ENABLED>
)

# =============================================================================
# Цели: hash
# =============================================================================
add_executable(hash
    ${CMAKE_SOURCE_DIR}/hashing/hash.c
    ${COMMON_SOURCES}
)

target_include_directories(hash PRIVATE
    ${CMAKE_SOURCE_DIR}/include
    ${OpenCL_INCLUDE_DIRS}
)

target_link_libraries(hash PRIVATE
    ${OpenCL_LIBRARIES}
    ${MATH_LIBRARY}
    Threads::Threads
)

target_compile_definitions(hash PRIVATE
    $<$<BOOL:${ENABLE_PROFILING}>:CL_PROFILING_ENABLED>
)

# =============================================================================
# Тесты
# =============================================================================
if(BUILD_TESTS)
    enable_testing()
    
    # Тест SHA-256
    add_executable(test_sha256
        ${CMAKE_SOURCE_DIR}/tests/test_sha256.c
        ${CMAKE_SOURCE_DIR}/hashing/hash.c
        ${COMMON_SOURCES}
    )
    target_include_directories(test_sha256 PRIVATE
        ${CMAKE_SOURCE_DIR}/include
        ${CMAKE_SOURCE_DIR}/tests
        ${OpenCL_INCLUDE_DIRS}
    )
    target_link_libraries(test_sha256 PRIVATE
        ${OpenCL_LIBRARIES}
        ${MATH_LIBRARY}
    )

    # Тест Sieve
    add_executable(test_sieve
        ${CMAKE_SOURCE_DIR}/tests/test_sieve.c
        ${CMAKE_SOURCE_DIR}/sieve/sieve.c
        ${COMMON_SOURCES}
    )
    target_include_directories(test_sieve PRIVATE
        ${CMAKE_SOURCE_DIR}/include
        ${CMAKE_SOURCE_DIR}/tests
        ${OpenCL_INCLUDE_DIRS}
    )
    target_link_libraries(test_sieve PRIVATE
        ${OpenCL_LIBRARIES}
        ${MATH_LIBRARY}
    )

    # Интеграционный тест: hash CPU vs GPU
    add_executable(test_hash_correctness
        ${CMAKE_SOURCE_DIR}/tests/test_hash_correctness.c
        ${CMAKE_SOURCE_DIR}/hashing/hash.c
        ${COMMON_SOURCES}
    )
    target_include_directories(test_hash_correctness PRIVATE
        ${CMAKE_SOURCE_DIR}/include
        ${CMAKE_SOURCE_DIR}/tests
        ${OpenCL_INCLUDE_DIRS}
    )
    target_link_libraries(test_hash_correctness PRIVATE
        ${OpenCL_LIBRARIES}
        ${MATH_LIBRARY}
    )

    # Интеграционный тест: sieve CPU vs GPU
    add_executable(test_sieve_correctness
        ${CMAKE_SOURCE_DIR}/tests/test_sieve_correctness.c
        ${CMAKE_SOURCE_DIR}/sieve/sieve.c
        ${COMMON_SOURCES}
    )
    target_include_directories(test_sieve_correctness PRIVATE
        ${CMAKE_SOURCE_DIR}/include
        ${CMAKE_SOURCE_DIR}/tests
        ${OpenCL_INCLUDE_DIRS}
    )
    target_link_libraries(test_sieve_correctness PRIVATE
        ${OpenCL_LIBRARIES}
        ${MATH_LIBRARY}
    )

    # Регистрация тестов
    add_test(NAME SHA256_Unit_Tests COMMAND test_sha256)
    add_test(NAME Sieve_Unit_Tests COMMAND test_sieve 1000000)
    add_test(NAME Hash_Integration_Tests COMMAND test_hash_correctness)
    add_test(NAME Sieve_Integration_Tests COMMAND test_sieve_correctness 1000000)
    
    # НастройкаCTest для вывода результатов
    set(CTEST_CUSTOM_TESTS_IGNORE
        "test_sieve_correctness"  # Игнорировать если нет GPU
    )
endif()

# =============================================================================
# Бенчмарки
# =============================================================================
if(BUILD_BENCHMARKS)
    add_custom_target(benchmarks
        DEPENDS sieve hash
        COMMENT "Бенчмарки собраны. Запустите './scripts/benchmark.sh all'"
    )
endif()

# =============================================================================
# Статический анализ
# =============================================================================
if(USE_STATIC_ANALYSIS)
    find_program(CLANG_TIDY_EXE clang-tidy)
    if(CLANG_TIDY_EXE)
        message(STATUS "clang-tidy найден: ${CLANG_TIDY_EXE}")
        set(CMAKE_C_CLANG_TIDY ${CLANG_TIDY_EXE}
            -header-filter=${CMAKE_SOURCE_DIR}/include
            -checks=bugprone-*,cert-*,clang-analyzer-*,misc-*,modernize-*,performance-*,portability-*
        )
    else()
        message(WARNING "clang-tidy не найден, статический анализ отключен")
    endif()
endif()

# =============================================================================
# Установка
# =============================================================================
include(GNUInstallDirs)
include(CMakePackageConfigHelpers)

# Установка бинарных файлов
install(TARGETS sieve hash
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)

# Установка kernel файлов
install(FILES 
    ${CMAKE_SOURCE_DIR}/sieve/sieve.cl
    ${CMAKE_SOURCE_DIR}/hashing/hash.cl
    DESTINATION ${CMAKE_INSTALL_DATADIR}/gpu_lab/kernels
)

# Установка заголовочных файлов
install(FILES ${COMMON_HEADERS}
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/gpu_lab
)

# Установка документации
if(INSTALL_DOCS)
    install(FILES 
        ${CMAKE_SOURCE_DIR}/README.md
        ${CMAKE_SOURCE_DIR}/CHANGELOG.md
        ${CMAKE_SOURCE_DIR}/CONTRIBUTING.md
        DESTINATION ${CMAKE_INSTALL_DOCDIR}
    )
    
    if(EXISTS ${CMAKE_BINARY_DIR}/docs/html)
        install(DIRECTORY ${CMAKE_BINARY_DIR}/docs/html
            DESTINATION ${CMAKE_INSTALL_DOCDIR}/api
        )
    endif()
endif()

# CMake конфигурация для поиска пакета
configure_package_config_file(
    ${CMAKE_SOURCE_DIR}/cmake/GPU_LabConfig.cmake.in
    ${CMAKE_BINARY_DIR}/GPU_LabConfig.cmake
    INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/GPU_Lab
)

write_basic_package_version_file(
    ${CMAKE_BINARY_DIR}/GPU_LabConfigVersion.cmake
    VERSION ${PROJECT_VERSION}
    COMPATIBILITY SameMajorVersion
)

install(FILES
    ${CMAKE_BINARY_DIR}/GPU_LabConfig.cmake
    ${CMAKE_BINARY_DIR}/GPU_LabConfigVersion.cmake
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/GPU_Lab
)

# =============================================================================
# Вывод информации о сборке
# =============================================================================
message(STATUS "")
message(STATUS "=============================================")
message(STATUS "GPU Lab v${PROJECT_VERSION} - конфигурация")
message(STATUS "=============================================")
message(STATUS "  Сборка:              ${CMAKE_BUILD_TYPE}")
message(STATUS "  Компилятор:          ${CMAKE_C_COMPILER_ID} ${CMAKE_C_COMPILER_VERSION}")
message(STATUS "  OpenCL:              ${OpenCL_VERSION}")
message(STATUS "  Тесты:               ${BUILD_TESTS}")
message(STATUS "  Бенчмарки:           ${BUILD_BENCHMARKS}")
message(STATUS "  Профилирование:      ${ENABLE_PROFILING}")
message(STATUS "  Стат. анализ:        ${USE_STATIC_ANALYSIS}")
message(STATUS "  Покрытие кода:       ${ENABLE_COVERAGE}")
message(STATUS "  Установка docs:      ${INSTALL_DOCS}")
message(STATUS "=============================================")
message(STATUS "")

# =============================================================================
# Пользовательские цели
# =============================================================================

# Цель для форматирования кода
find_program(CLANG_FORMAT_EXE clang-format)
if(CLANG_FORMAT_EXE)
    add_custom_target(format
        COMMAND ${CLANG_FORMAT_EXE} -i
            ${CMAKE_SOURCE_DIR}/hashing/hash.c
            ${CMAKE_SOURCE_DIR}/sieve/sieve.c
            ${CMAKE_SOURCE_DIR}/src/cl_utils.c
            ${CMAKE_SOURCE_DIR}/include/cl_common.h
        WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
        COMMENT "Форматирование кода..."
    )
endif()

# Цель для очистки
add_custom_target(clean-all
    COMMAND ${CMAKE_COMMAND} -E remove_directory ${CMAKE_BINARY_DIR}
    COMMENT "Полная очистка build директории"
)
