#!/bin/bash
# =============================================================================
# Скрипт автоматической сборки, тестирования и бенчмарка проекта GPU Lab
# =============================================================================
# Использование:
#   ./build_and_test.sh [опции]
#
# Опции:
#   -c, --clean       Очистить сборку перед сборкой
#   -d, --debug       Debug сборка (по умолчанию Release)
#   -t, --test        Запустить тесты (по умолчанию да)
#   -b, --benchmark   Запустить бенчмарки
#   -h, --help        Показать эту справку
#
# Примеры:
#   ./build_and_test.sh              # Сборка + тесты
#   ./build_and_test.sh -c -b        # Очистка + сборка + бенчмарки
#   ./build_and_test.sh --debug      # Debug сборка + тесты
# =============================================================================

set -e  # Выход при ошибке

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # Без цвета

# Переменные
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build"
CLEAN_BUILD=false
RUN_TESTS=true
RUN_BENCHMARKS=false
BUILD_TYPE="Release"

# =============================================================================
# Функции
# =============================================================================

print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

show_help() {
    head -20 "$0" | tail -17 | sed 's/^# //'
    exit 0
}

clean_build() {
    print_header "Очистка сборки"
    if [ -d "$BUILD_DIR" ]; then
        rm -rf "$BUILD_DIR"
        print_success "Директория build удалена"
    else
        print_info "Директория build не существует"
    fi
}

configure() {
    print_header "Конфигурация проекта (CMake)"
    cd "$PROJECT_DIR"

    cmake -S . -B "$BUILD_DIR" \
        -DCMAKE_BUILD_TYPE="$BUILD_TYPE" \
        -DBUILD_TESTS=ON \
        -DBUILD_BENCHMARKS=ON \
        -DENABLE_PROFILING=ON

    print_success "CMake конфигурация завершена"
}

build() {
    print_header "Сборка проекта"
    cd "$BUILD_DIR"

    # Определение количества ядер для параллельной сборки
    if command -v nproc &> /dev/null; then
        JOBS=$(nproc)
    elif command -v sysctl &> /dev/null; then
        JOBS=$(sysctl -n hw.ncpu)
    else
        JOBS=4
    fi

    cmake --build . --parallel "$JOBS"

    print_success "Сборка завершена"
}

run_tests() {
    if [ "$RUN_TESTS" = false ]; then
        return
    fi

    print_header "Запуск тестов (CTest)"
    cd "$BUILD_DIR"

    # Запуск всех тестов с выводом результатов
    ctest --output-on-failure --verbose

    # Проверка результатов
    TOTAL=$(ctest --show-only | grep -c "Test #" || true)
    if [ "$TOTAL" -eq 0 ]; then
        print_info "Тесты не найдены"
        return
    fi

    print_success "Все тесты пройдены"
}

run_benchmarks() {
    if [ "$RUN_BENCHMARKS" = false ]; then
        return
    fi

    print_header "Запуск бенчмарков"
    cd "$BUILD_DIR"

    # Проверка наличия исполняемых файлов
    if [ ! -x "./sieve" ]; then
        print_error "sieve не найден или не исполняемый"
        return
    fi

    if [ ! -x "./hash" ]; then
        print_error "hash не найден или не исполняемый"
        return
    fi

    # Бенчмарк решета Эратосфена
    echo -e "\n${YELLOW}Бенчмарк: Решето Эратосфена${NC}"
    ./sieve 10000000 256

    # Бенчмарк хэширования
    echo -e "\n${YELLOW}Бенчмарк: Параллельное хэширование${NC}"
    ./hash 100000 64 256

    print_success "Бенчмарки завершены"
}

generate_docs() {
    print_header "Генерация документации"
    cd "$BUILD_DIR"

    if command -v doxygen &> /dev/null; then
        cmake --build . --target docs
        print_success "Документация сгенерирована в $BUILD_DIR/docs"
    else
        print_info "Doxygen не найден, документация не сгенерирована"
    fi
}

summary() {
    print_header "Итоги сборки"

    echo "Директория сборки: $BUILD_DIR"
    echo "Тип сборки:        $BUILD_TYPE"

    if [ -d "$BUILD_DIR" ]; then
        echo -e "\n${GREEN}Собранные файлы:${NC}"
        find "$BUILD_DIR" -maxdepth 1 -type f -executable -name "*" | while read -r file; do
            echo "  - $(basename "$file")"
        done
    fi

    echo -e "\n${YELLOW}Для запуска тестов:${NC}"
    echo "  cd $BUILD_DIR && ctest --verbose"

    echo -e "\n${YELLOW}Для запуска бенчмарков:${NC}"
    echo "  cd $BUILD_DIR && ./sieve 10000000 256"
    echo "  cd $BUILD_DIR && ./hash 100000 64 256"

    if [ -d "$BUILD_DIR/docs" ]; then
        echo -e "\n${YELLOW}Документация:${NC}"
        echo "  Откройте $BUILD_DIR/docs/html/index.html"
    fi
}

# =============================================================================
# Парсинг аргументов командной строки
# =============================================================================

while [[ $# -gt 0 ]]; do
    case $1 in
        -c|--clean)
            CLEAN_BUILD=true
            shift
            ;;
        -d|--debug)
            BUILD_TYPE="Debug"
            shift
            ;;
        -t|--test)
            RUN_TESTS=true
            shift
            ;;
        -b|--benchmark)
            RUN_BENCHMARKS=true
            shift
            ;;
        -h|--help)
            show_help
            ;;
        *)
            print_error "Неизвестная опция: $1"
            show_help
            ;;
    esac
done

# =============================================================================
# Основной процесс
# =============================================================================

print_header "GPU Lab - Автоматическая сборка и тесты"
echo "Проект: $PROJECT_DIR"
echo "Сборка: $BUILD_DIR"
echo "Тип:    $BUILD_TYPE"

if [ "$CLEAN_BUILD" = true ]; then
    clean_build
fi

configure
build
run_tests
run_benchmarks
generate_docs
summary

print_success "\nВсе операции завершены успешно!"
