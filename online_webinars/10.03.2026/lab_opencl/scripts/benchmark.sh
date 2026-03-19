#!/bin/bash
# =============================================================================
# benchmark.sh — Скрипт для запуска бенчмарков с генерацией данных
# =============================================================================
# Использование:
#   ./scripts/benchmark.sh [hash|sieve|all] [output_dir]
#
# Примеры:
#   ./scripts/benchmark.sh all results/
#   ./scripts/benchmark.sh hash results/
#   ./scripts/benchmark.sh sieve results/
# =============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
OUTPUT_DIR="${2:-$PROJECT_DIR/benchmark_results}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Создание директории для результатов
mkdir -p "$OUTPUT_DIR"

# =============================================================================
# Бенчмарк хэширования
# =============================================================================
run_hash_benchmark() {
    local output_file="$OUTPUT_DIR/hash_benchmark_$TIMESTAMP.csv"
    local sieve_exe="$PROJECT_DIR/build/hash"
    
    # Если нет сборки через CMake, пробуем Makefile
    if [ ! -f "$sieve_exe" ]; then
        sieve_exe="$PROJECT_DIR/hashing/hash"
    fi
    
    if [ ! -f "$sieve_exe" ]; then
        log_error "hash executable not found. Please build the project first."
        return 1
    fi
    
    log_info "Запуск бенчмарка хэширования..."
    echo "num_hashes,data_len,local_size,cpu_time_ms,gpu_time_ms,speedup,correct" > "$output_file"
    
    # Тест с разным количеством хэшей
    for num in 1000 10000 50000 100000 250000 500000; do
        log_info "  num_hashes=$num"
        
        # Запуск с разными work-group sizes
        for wg in 64 128 256 512; do
            # Запуск программы и парсинг JSON вывода
            result=$("$sieve_exe" "$num" 64 "$wg" --json 2>/dev/null) || true
            
            # Парсинг JSON (простой вариант)
            cpu_time=$(echo "$result" | grep -o '"cpu_time_ms": [0-9.]*' | grep -o '[0-9.]*' || echo "0")
            gpu_time=$(echo "$result" | grep -o '"gpu_kernel_time_ms": [0-9.]*' | grep -o '[0-9.]*' || echo "0")
            correct=$(echo "$result" | grep -o '"correct": [a-z]*' | grep -o 'true\|false' || echo "false")
            
            if [ -n "$cpu_time" ] && [ -n "$gpu_time" ]; then
                speedup=$(echo "scale=2; $cpu_time / $gpu_time" | bc 2>/dev/null || echo "0")
            else
                speedup="0"
            fi
            
            echo "$num,64,$wg,$cpu_time,$gpu_time,$speedup,$correct" >> "$output_file"
        done
    done
    
    log_success "Результаты сохранены в $output_file"
    echo ""
    cat "$output_file"
}

# =============================================================================
# Бенчмарк решета Эратосфена
# =============================================================================
run_sieve_benchmark() {
    local output_file="$OUTPUT_DIR/sieve_benchmark_$TIMESTAMP.csv"
    local sieve_exe="$PROJECT_DIR/build/sieve"
    
    # Если нет сборки через CMake, пробуем Makefile
    if [ ! -f "$sieve_exe" ]; then
        sieve_exe="$PROJECT_DIR/sieve/sieve"
    fi
    
    if [ ! -f "$sieve_exe" ]; then
        log_error "sieve executable not found. Please build the project first."
        return 1
    fi
    
    log_info "Запуск бенчмарка решета Эратосфена..."
    echo "limit,local_size,cpu_time_ms,gpu_time_ms,speedup,primes_found,correct" > "$output_file"
    
    # Тест с разным N
    for n in 100000 500000 1000000 5000000 10000000; do
        log_info "  N=$n"
        
        # Запуск с разными work-group sizes
        for wg in 64 128 256 512; do
            # Запуск программы и парсинг JSON вывода
            result=$("$sieve_exe" "$n" "$wg" --json 2>/dev/null) || true
            
            # Парсинг JSON
            cpu_time=$(echo "$result" | grep -o '"cpu_time_ms": [0-9.]*' | grep -o '[0-9.]*' || echo "0")
            gpu_time=$(echo "$result" | grep -o '"gpu_kernel_time_ms": [0-9.]*' | grep -o '[0-9.]*' || echo "0")
            gpu_total=$(echo "$result" | grep -o '"gpu_total_time_ms": [0-9.]*' | grep -o '[0-9.]*' || echo "0")
            correct=$(echo "$result" | grep -o '"correct": [a-z]*' | grep -o 'true\|false' || echo "false")
            cpu_count=$(echo "$result" | grep -o '"count": [0-9]*' | head -1 | grep -o '[0-9]*' || echo "0")
            
            if [ -n "$cpu_time" ] && [ -n "$gpu_time" ]; then
                speedup=$(echo "scale=2; $cpu_time / $gpu_time" | bc 2>/dev/null || echo "0")
            else
                speedup="0"
            fi
            
            echo "$n,$wg,$cpu_time,$gpu_time,$speedup,$cpu_count,$correct" >> "$output_file"
        done
    done
    
    log_success "Результаты сохранены в $output_file"
    echo ""
    cat "$output_file"
}

# =============================================================================
# Генерация графиков (требует Python + matplotlib)
# =============================================================================
generate_plots() {
    local hash_file="$1"
    local sieve_file="$2"
    
    if ! command -v python3 &> /dev/null; then
        log_warn "Python3 не найден. Пропускаем генерацию графиков."
        return 1
    fi
    
    # Проверка matplotlib
    if ! python3 -c "import matplotlib" 2>/dev/null; then
        log_warn "matplotlib не установлен. Пропускаем генерацию графиков."
        log_info "Установите: pip install matplotlib pandas"
        return 1
    fi
    
    log_info "Генерация графиков..."
    
    python3 << EOF
import pandas as pd
import matplotlib.pyplot as plt
import os

output_dir = "$OUTPUT_DIR"

# График для хэширования
try:
    hash_files = [f for f in os.listdir(output_dir) if f.startswith('hash_benchmark') and f.endswith('.csv')]
    if hash_files:
        df = pd.read_csv(os.path.join(output_dir, hash_files[-1]))
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Время выполнения
        ax1 = axes[0]
        for wg in df['local_size'].unique():
            subset = df[df['local_size'] == wg]
            ax1.plot(subset['num_hashes'], subset['cpu_time_ms'], marker='o', label=f'CPU (wg={wg})')
            ax1.plot(subset['num_hashes'], subset['gpu_time_ms'], marker='s', label=f'GPU (wg={wg})')
        ax1.set_xlabel('Количество хэшей')
        ax1.set_ylabel('Время (мс)')
        ax1.set_title('Производительность хэширования')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Ускорение
        ax2 = axes[1]
        for wg in df['local_size'].unique():
            subset = df[df['local_size'] == wg]
            ax2.plot(subset['num_hashes'], subset['speedup'], marker='o', label=f'wg={wg}')
        ax2.set_xlabel('Количество хэшей')
        ax2.set_ylabel('Ускорение (CPU/GPU)')
        ax2.set_title('Ускорение GPU')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'hash_performance.png'), dpi=150)
        print(f"  Сохранён: hash_performance.png")
except Exception as e:
    print(f"  Ошибка при построении hash графиков: {e}")

# График для решета
try:
    sieve_files = [f for f in os.listdir(output_dir) if f.startswith('sieve_benchmark') and f.endswith('.csv')]
    if sieve_files:
        df = pd.read_csv(os.path.join(output_dir, sieve_files[-1]))
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Время выполнения
        ax1 = axes[0]
        for wg in df['local_size'].unique():
            subset = df[df['local_size'] == wg]
            ax1.loglog(subset['limit'], subset['cpu_time_ms'], marker='o', label=f'CPU (wg={wg})')
            ax1.loglog(subset['limit'], subset['gpu_time_ms'], marker='s', label=f'GPU (wg={wg})')
        ax1.set_xlabel('N (верхняя граница)')
        ax1.set_ylabel('Время (мс)')
        ax1.set_title('Производительность решета Эратосфена')
        ax1.legend()
        ax1.grid(True, alpha=0.3, which='both')
        
        # Ускорение
        ax2 = axes[1]
        for wg in df['local_size'].unique():
            subset = df[df['local_size'] == wg]
            ax2.semilogx(subset['limit'], subset['speedup'], marker='o', label=f'wg={wg}')
        ax2.set_xlabel('N (верхняя граница)')
        ax2.set_ylabel('Ускорение (CPU/GPU)')
        ax2.set_title('Ускорение GPU')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'sieve_performance.png'), dpi=150)
        print(f"  Сохранён: sieve_performance.png")
except Exception as e:
    print(f"  Ошибка при построении sieve графиков: {e}")

print("Генерация графиков завершена.")
EOF
}

# =============================================================================
# Главная функция
# =============================================================================
main() {
    local mode="${1:-all}"
    
    echo "=============================================="
    echo "  Бенчмарк проекта GPU Lab"
    echo "  Результаты: $OUTPUT_DIR"
    echo "=============================================="
    echo ""
    
    case "$mode" in
        hash)
            run_hash_benchmark
            ;;
        sieve)
            run_sieve_benchmark
            ;;
        all)
            run_hash_benchmark
            run_sieve_benchmark
            ;;
        plots)
            generate_plots
            ;;
        *)
            echo "Использование: $0 [hash|sieve|all|plots] [output_dir]"
            echo ""
            echo "  hash   - бенчмарк хэширования"
            echo "  sieve  - бенчмарк решета"
            echo "  all    - все бенчмарки"
            echo "  plots  - генерация графиков (требует Python)"
            exit 1
            ;;
    esac
    
    # Попытка генерации графиков
    if [ "$mode" != "plots" ]; then
        echo ""
        generate_plots "$OUTPUT_DIR/hash_benchmark_$TIMESTAMP.csv" "$OUTPUT_DIR/sieve_benchmark_$TIMESTAMP.csv" || true
    fi
    
    echo ""
    log_success "Бенчмарк завершён!"
}

main "$@"
