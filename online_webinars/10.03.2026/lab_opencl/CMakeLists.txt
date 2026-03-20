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

cmake_minimum_required(VERSION 3.16)
project(GPU_Lab
    VERSION 1.5.0
    DESCRIPTION "GPU Lab: OpenCL parallel computing laboratory"
    LANGUAGES C
)

# =============================================================================
# Опции сборки
# =============================================================================
option(BUILD_TESTS "Сборка тестов" ON)
option(BUILD_BENCHMARKS "Сборка бенчмарков" ON)
option(ENABLE_PROFILING "Включить профилирование" ON)
option(USE_STATIC_ANALYSIS "Включить статический анализ" OFF)
option(ENABLE_COVERAGE "Включить покрытие кода" OFF)
option(ENABLE_LTO "Включить Link Time Optimization для Release сборок" ON)
option(BUILD_SHARED_LIBS "Построить общие библиотеки" OFF)
option(ENABLE_WERROR "Трактировать предупреждения как ошибки" OFF)

# =============================================================================
# Поиск зависимостей
# =============================================================================

# Поиск OpenCL
# Для MinGW/MSYS2 используем find_package с указанием имён библиотек
if(WIN32 AND CMAKE_C_COMPILER_ID MATCHES "GNU|Clang")
    # MinGW: ищем libOpenCL.dll.a
    find_library(OpenCL_LIBRARY
        NAMES OpenCL libOpenCL.dll.a
        PATHS
            C:/msys64/ucrt64/lib
            C:/msys64/mingw64/lib
            $ENV{OCL_ROOT}/lib
    )
    find_path(OpenCL_INCLUDE_DIR
        NAMES CL/cl.h
        PATHS
            C:/msys64/ucrt64/include
            C:/msys64/mingw64/include
            $ENV{OCL_ROOT}/include
    )
    set(OpenCL_LIBRARIES ${OpenCL_LIBRARY})
    set(OpenCL_INCLUDE_DIRS ${OpenCL_INCLUDE_DIR})
else()
    find_package(OpenCL REQUIRED)
endif()

if(OpenCL_LIBRARY AND OpenCL_INCLUDE_DIR)
    message(STATUS "OpenCL найден: ${OpenCL_INCLUDE_DIR}")
    message(STATUS "OpenCL библиотеки: ${OpenCL_LIBRARY}")
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

# Поиск Doxygen для генерации документации
find_package(Doxygen QUIET)
if(DOXYGEN_FOUND)
    message(STATUS "Doxygen найден: ${DOXYGEN_EXECUTABLE}")
    set(DOXYGEN_AVAILABLE TRUE)
else()
    message(STATUS "Doxygen не найден, документация не будет сгенерирована")
    set(DOXYGEN_AVAILABLE FALSE)
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
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wall -Wextra -Wpedantic")
set(CMAKE_C_FLAGS_DEBUG "-g -O0 -DDEBUG")
set(CMAKE_C_FLAGS_RELEASE "-O3 -DNDEBUG")

# Дополнительные предупреждения для gcc/clang
if(CMAKE_C_COMPILER_ID MATCHES "GNU|Clang")
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wformat -Wformat-security -Wconversion -Wshadow")
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wnull-dereference -Wstack-protector")
    # Улучшенная генерация кода для современных CPU
    set(CMAKE_C_FLAGS_RELEASE "${CMAKE_C_FLAGS_RELEASE} -march=native -mtune=native")
endif()

# Link Time Optimization для Release сборок
if(ENABLE_LTO AND CMAKE_BUILD_TYPE STREQUAL "Release")
    if(CMAKE_C_COMPILER_ID MATCHES "GNU|Clang")
        message(STATUS "LTO включено для Release сборки")
        set(CMAKE_C_FLAGS_RELEASE "${CMAKE_C_FLAGS_RELEASE} -flto")
        set(CMAKE_EXE_LINKER_FLAGS_RELEASE "${CMAKE_EXE_LINKER_FLAGS_RELEASE} -flto")
    endif()
endif()

# -Werror для строгой компиляции
if(ENABLE_WERROR)
    if(CMAKE_C_COMPILER_ID MATCHES "GNU|Clang")
        set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Werror")
        message(STATUS "Предупреждения включены как ошибки (-Werror)")
    endif()
endif()

# Для Windows: дополнительные флаги
if(WIN32)
    add_definitions(-D_CRT_SECURE_NO_WARNINGS)
    add_definitions(-DNOMINMAX)
endif()

# По умолчанию Release сборка
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

message(STATUS "Тип сборки: ${CMAKE_BUILD_TYPE}")

# =============================================================================
# Покрытие кода (опционально)
# =============================================================================

if(ENABLE_COVERAGE)
    if(CMAKE_C_COMPILER_ID MATCHES "GNU|Clang")
        message(STATUS "Покрытие кода включено")
        set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} --coverage -fprofile-arcs -ftest-coverage")
        set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} --coverage")
    else()
        message(WARNING "Покрытие кода поддерживается только для gcc/clang")
    endif()
endif()

# =============================================================================
# AddressSanitizer (опционально)
# =============================================================================

if(ENABLE_ASAN)
    if(CMAKE_C_COMPILER_ID MATCHES "GNU|Clang")
        message(STATUS "AddressSanitizer включён")
        set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fsanitize=address -fno-omit-frame-pointer")
        set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -fsanitize=address")
        if(CMAKE_BUILD_TYPE STREQUAL "Release")
            message(WARNING "AddressSanitizer не рекомендуется использовать в Release сборке")
        endif()
    elseif(MSVC)
        # MSVC имеет встроенный AddressSanitizer (начиная с VS 2019 16.9)
        message(STATUS "AddressSanitizer включён (MSVC)")
        add_compile_options(/fsanitize=address)
    else()
        message(WARNING "AddressSanitizer не поддерживается для этого компилятора")
    endif()
endif()

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
    ${PROJECT_SOURCE_DIR}/hashing/sha256.c
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

# -----------------------------------------------------------------------------
# Криптография: Argon2 (memory-hard хэширование)
# -----------------------------------------------------------------------------
add_executable(argon2
    ${PROJECT_SOURCE_DIR}/crypto/argon2/argon2.c
    ${PROJECT_SOURCE_DIR}/crypto/argon2/argon2_main.c
    ${COMMON_SOURCES}
)

target_include_directories(argon2 PRIVATE ${PROJECT_SOURCE_DIR}/crypto/argon2)

target_link_libraries(argon2
    ${OpenCL_LIBRARIES}
    ${MATH_LIBRARY}
)

if(WIN32)
    target_link_libraries(argon2 shlwapi)
endif()

target_compile_definitions(argon2 PRIVATE
    $<$<BOOL:${ENABLE_PROFILING}>:CL_PROFILING_ENABLED>
)

# -----------------------------------------------------------------------------
# Криптография: SHA-3 (Keccak) — NIST стандарт 2015
# -----------------------------------------------------------------------------
add_executable(sha3
    ${PROJECT_SOURCE_DIR}/crypto/sha3/sha3.c
    ${PROJECT_SOURCE_DIR}/crypto/sha3/sha3_main.c
    ${COMMON_SOURCES}
)

target_include_directories(sha3 PRIVATE ${PROJECT_SOURCE_DIR}/crypto/sha3)

target_link_libraries(sha3
    ${OpenCL_LIBRARIES}
    ${MATH_LIBRARY}
)

if(WIN32)
    target_link_libraries(sha3 shlwapi)
endif()

target_compile_definitions(sha3 PRIVATE
    $<$<BOOL:${ENABLE_PROFILING}>:CL_PROFILING_ENABLED>
)

# -----------------------------------------------------------------------------
# Криптография: BLAKE3 — самый быстрый хэш
# -----------------------------------------------------------------------------
add_executable(blake3
    ${PROJECT_SOURCE_DIR}/crypto/blake3/blake3.c
    ${PROJECT_SOURCE_DIR}/crypto/blake3/blake3_main.c
    ${COMMON_SOURCES}
)

target_include_directories(blake3 PRIVATE ${PROJECT_SOURCE_DIR}/crypto/blake3)

target_link_libraries(blake3
    ${OpenCL_LIBRARIES}
    ${MATH_LIBRARY}
)

if(WIN32)
    target_link_libraries(blake3 shlwapi)
endif()

target_compile_definitions(blake3 PRIVATE
    $<$<BOOL:${ENABLE_PROFILING}>:CL_PROFILING_ENABLED>
)

# -----------------------------------------------------------------------------
# Криптография: AES-256-GCM — стандарт шифрования
# -----------------------------------------------------------------------------
add_executable(aes
    ${PROJECT_SOURCE_DIR}/crypto/aes/aes.c
    ${PROJECT_SOURCE_DIR}/crypto/aes/aes_main.c
    ${COMMON_SOURCES}
)

target_include_directories(aes PRIVATE ${PROJECT_SOURCE_DIR}/crypto/aes)

target_link_libraries(aes
    ${OpenCL_LIBRARIES}
    ${MATH_LIBRARY}
)

if(WIN32)
    target_link_libraries(aes shlwapi)
endif()

target_compile_definitions(aes PRIVATE
    $<$<BOOL:${ENABLE_PROFILING}>:CL_PROFILING_ENABLED>
)

# -----------------------------------------------------------------------------
# Криптография: ChaCha20-Poly1305 — AEAD шифрование
# -----------------------------------------------------------------------------
add_executable(chacha20
    ${PROJECT_SOURCE_DIR}/crypto/chacha20/chacha20.c
    ${PROJECT_SOURCE_DIR}/crypto/chacha20/chacha20_main.c
    ${COMMON_SOURCES}
)

target_include_directories(chacha20 PRIVATE ${PROJECT_SOURCE_DIR}/crypto/chacha20)

target_link_libraries(chacha20
    ${OpenCL_LIBRARIES}
    ${MATH_LIBRARY}
)

if(WIN32)
    target_link_libraries(chacha20 shlwapi)
endif()

target_compile_definitions(chacha20 PRIVATE
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

    # Unit-тест Argon2
    add_executable(test_argon2
        ${PROJECT_SOURCE_DIR}/tests/test_argon2.c
        ${PROJECT_SOURCE_DIR}/crypto/argon2/argon2.c
    )
    target_link_libraries(test_argon2
        ${MATH_LIBRARY}
    )
    target_include_directories(test_argon2 PRIVATE ${PROJECT_SOURCE_DIR}/tests)

    # Unit-тест SHA-3
    add_executable(test_sha3
        ${PROJECT_SOURCE_DIR}/tests/test_sha3.c
        ${PROJECT_SOURCE_DIR}/crypto/sha3/sha3.c
    )
    target_link_libraries(test_sha3
        ${MATH_LIBRARY}
    )
    target_include_directories(test_sha3 PRIVATE ${PROJECT_SOURCE_DIR}/tests)

    # Unit-тест BLAKE3
    add_executable(test_blake3
        ${PROJECT_SOURCE_DIR}/tests/test_blake3.c
        ${PROJECT_SOURCE_DIR}/crypto/blake3/blake3.c
    )
    target_link_libraries(test_blake3
        ${MATH_LIBRARY}
    )
    target_include_directories(test_blake3 PRIVATE ${PROJECT_SOURCE_DIR}/tests)

    # Unit-тест AES-256-GCM
    add_executable(test_aes
        ${PROJECT_SOURCE_DIR}/tests/test_aes.c
        ${PROJECT_SOURCE_DIR}/crypto/aes/aes.c
    )
    target_link_libraries(test_aes
        ${MATH_LIBRARY}
    )
    target_include_directories(test_aes PRIVATE ${PROJECT_SOURCE_DIR}/tests)

    # Unit-тест ChaCha20-Poly1305
    add_executable(test_chacha20
        ${PROJECT_SOURCE_DIR}/tests/test_chacha20.c
        ${PROJECT_SOURCE_DIR}/crypto/chacha20/chacha20.c
    )
    target_link_libraries(test_chacha20
        ${MATH_LIBRARY}
    )
    target_include_directories(test_chacha20 PRIVATE ${PROJECT_SOURCE_DIR}/tests)

    # Регистрация тестов в CTest
    add_test(NAME SHA256_Unit_Test COMMAND test_sha256)
    add_test(NAME Sieve_Unit_Test COMMAND test_sieve)
    add_test(NAME Argon2_Unit_Test COMMAND test_argon2)
    add_test(NAME SHA3_Unit_Test COMMAND test_sha3)
    add_test(NAME BLAKE3_Unit_Test COMMAND test_blake3)
    add_test(NAME AES_Unit_Test COMMAND test_aes)
    add_test(NAME ChaCha20_Unit_Test COMMAND test_chacha20)

    # Интеграционные тесты через запуск основных программ
    # Примечание: unit-тесты требуют рефакторинга для разделения main() и функций

    # Интеграционный тест: проверка работы hashing
    add_test(NAME Hash_Integration_Test COMMAND hash 10000 64 256)

    # Интеграционный тест: проверка работы sieve
    add_test(NAME Sieve_Integration_Test COMMAND sieve 1000000 256)

    # Интеграционный тест: проверка работы argon2
    add_test(NAME Argon2_Integration_Test COMMAND argon2)
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
    ${PROJECT_SOURCE_DIR}/crypto/argon2/argon2.cl
    ${PROJECT_SOURCE_DIR}/crypto/sha3/sha3.cl
    ${PROJECT_SOURCE_DIR}/crypto/blake3/blake3.cl
    ${PROJECT_SOURCE_DIR}/crypto/aes/aes.cl
    ${PROJECT_SOURCE_DIR}/crypto/chacha20/chacha20.cl
    DESTINATION share/gpu_lab/kernels
)

install(FILES
    ${PROJECT_SOURCE_DIR}/hashing/sha256.h
    ${PROJECT_SOURCE_DIR}/include/cl_common.h
    ${PROJECT_SOURCE_DIR}/crypto/argon2/argon2.h
    ${PROJECT_SOURCE_DIR}/crypto/sha3/sha3.h
    ${PROJECT_SOURCE_DIR}/crypto/blake3/blake3.h
    ${PROJECT_SOURCE_DIR}/crypto/aes/aes.h
    ${PROJECT_SOURCE_DIR}/crypto/chacha20/chacha20.h
    DESTINATION include/gpu_lab
)

install(FILES ${PROJECT_SOURCE_DIR}/README.md
    DESTINATION share/doc/gpu_lab
)

# Копирование kernel файлов в директорию сборки для отладки
file(COPY ${PROJECT_SOURCE_DIR}/sieve/sieve.cl
     DESTINATION ${CMAKE_BINARY_DIR}/)
file(COPY ${PROJECT_SOURCE_DIR}/hashing/hash.cl
     DESTINATION ${CMAKE_BINARY_DIR}/)
file(COPY ${PROJECT_SOURCE_DIR}/crypto/argon2/argon2.cl
     DESTINATION ${CMAKE_BINARY_DIR}/)
file(COPY ${PROJECT_SOURCE_DIR}/crypto/sha3/sha3.cl
     DESTINATION ${CMAKE_BINARY_DIR}/)
file(COPY ${PROJECT_SOURCE_DIR}/crypto/blake3/blake3.cl
     DESTINATION ${CMAKE_BINARY_DIR}/)
file(COPY ${PROJECT_SOURCE_DIR}/crypto/aes/aes.cl
     DESTINATION ${CMAKE_BINARY_DIR}/)
file(COPY ${PROJECT_SOURCE_DIR}/crypto/chacha20/chacha20.cl
     DESTINATION ${CMAKE_BINARY_DIR}/)

# =============================================================================
# Генерация документации (опционально)
# =============================================================================

if(DOXYGEN_AVAILABLE)
    set(DOXYGEN_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/docs)
    set(DOXYGEN_GENERATE_HTML YES)
    set(DOXYGEN_GENERATE_MAN NO)

    doxygen_add_docs(docs
        ${PROJECT_SOURCE_DIR}/include
        ${PROJECT_SOURCE_DIR}/src
        ${PROJECT_SOURCE_DIR}/hashing
        ${PROJECT_SOURCE_DIR}/sieve
        ${PROJECT_SOURCE_DIR}/crypto
        COMMENT "Генерация документации Doxygen"
    )
endif()

# =============================================================================
# Цель для очистки всех артефактов сборки
# =============================================================================

add_custom_target(clean_all
    COMMAND ${CMAKE_BUILD_TOOL} clean
    COMMAND ${CMAKE_COMMAND} -E remove_directory ${CMAKE_BINARY_DIR}/CMakeFiles
    COMMAND ${CMAKE_COMMAND} -E remove_directory ${CMAKE_BINARY_DIR}/Testing
    COMMAND ${CMAKE_COMMAND} -E remove ${CMAKE_BINARY_DIR}/CMakeCache.txt
    COMMAND ${CMAKE_COMMAND} -E remove ${CMAKE_BINARY_DIR}/cmake_install.cmake
    COMMAND ${CMAKE_COMMAND} -E remove ${CMAKE_BINARY_DIR}/Makefile
    COMMENT "Полная очистка артефактов сборки"
    VERBATIM
)

# =============================================================================
# Цель для очистки проекта от мусора (через скрипт)
# =============================================================================

add_custom_target(clean_project
    COMMAND ${CMAKE_COMMAND} -E echo "Запуск очистки проекта..."
    COMMAND ${CMAKE_COMMAND} -E chdir ${PROJECT_SOURCE_DIR} ${PROJECT_SOURCE_DIR}/scripts/clean.bat
    COMMENT "Очистка проекта от мусора (с сохранением .exe)"
    VERBATIM
)

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
message(STATUS "  Компилятор:        ${CMAKE_C_COMPILER_ID} ${CMAKE_C_COMPILER_VERSION}")
message(STATUS "  Сборка тестов:     ${BUILD_TESTS}")
message(STATUS "  Сборка бенчмарков: ${BUILD_BENCHMARKS}")
message(STATUS "  Профилирование:    ${ENABLE_PROFILING}")
message(STATUS "  Стат. анализ:      ${USE_STATIC_ANALYSIS}")
message(STATUS "  Покрытие кода:     ${ENABLE_COVERAGE}")
message(STATUS "  Doxygen:           ${DOXYGEN_AVAILABLE}")
message(STATUS "=============================================")
message(STATUS "")
message(STATUS "Цели для сборки:")
message(STATUS "  cmake --build .           - собрать все цели")
message(STATUS "  cmake --build . --target sieve/hash")
message(STATUS "  cmake --build . --target test_sha256/test_sieve")
message(STATUS "  cmake --build . --target docs  - генерация документации")
message(STATUS "")
message(STATUS "Запуск тестов:")
message(STATUS "  ctest --verbose           - все тесты")
message(STATUS "  ctest -R SHA256           - только SHA-256 тесты")
message(STATUS "  ctest -R Sieve            - только Sieve тесты")
message(STATUS "=============================================")
message(STATUS "")
