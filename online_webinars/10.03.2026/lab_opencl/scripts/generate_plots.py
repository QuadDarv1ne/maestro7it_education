#!/usr/bin/env python3
# =============================================================================
# generate_plots.py — Генерация графиков производительности
# =============================================================================
# Использование:
#   python scripts/generate_plots.py [output_dir]
#
# Требования:
#   pip install matplotlib pandas numpy
# =============================================================================

import os
import sys
import glob
from datetime import datetime

try:
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
except ImportError:
    print("Ошибка: требуется установить matplotlib и pandas")
    print("  pip install matplotlib pandas")
    sys.exit(1)

# Настройка стиля графиков
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['legend.fontsize'] = 9
plt.rcParams['figure.titlesize'] = 14

def find_latest_benchmark_file(output_dir, prefix):
    """Поиск последнего файла бенчмарка по префиксу"""
    pattern = os.path.join(output_dir, f'{prefix}_benchmark_*.csv')
    files = glob.glob(pattern)
    if not files:
        return None
    return max(files, key=os.path.getctime)

def plot_hash_performance(output_dir, hash_file):
    """Генерация графиков для хэширования"""
    if not hash_file or not os.path.exists(hash_file):
        print(f"  [WARN] Файл бенчмарка хэширования не найден")
        return
    
    print(f"  Чтение: {os.path.basename(hash_file)}")
    
    try:
        df = pd.read_csv(hash_file)
    except Exception as e:
        print(f"  [ERROR] Ошибка чтения файла: {e}")
        return
    
    if df.empty:
        print("  [WARN] Пустой файл бенчмарка")
        return
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    # График 1: Время выполнения
    ax1 = axes[0]
    colors = {'CPU': '#e74c3c', 'GPU': '#3498db'}
    
    for wg in sorted(df['local_size'].unique()):
        subset = df[df['local_size'] == wg]
        ax1.plot(subset['num_hashes'], subset['cpu_time_ms'], 
                marker='o', linewidth=2, markersize=6,
                color=colors['CPU'], label=f'CPU (wg={wg})', alpha=0.8)
        ax1.plot(subset['num_hashes'], subset['gpu_time_ms'], 
                marker='s', linewidth=2, markersize=6,
                color=colors['GPU'], label=f'GPU (wg={wg})', alpha=0.8)
    
    ax1.set_xlabel('Количество хэшей')
    ax1.set_ylabel('Время выполнения (мс)')
    ax1.set_title('Сравнение производительности CPU vs GPU\n(хеширование SHA-256)')
    ax1.legend(loc='upper left')
    ax1.grid(True, alpha=0.3)
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    
    # Форматирование чисел
    ax1.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f'{x:.0f}'))
    ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f'{x:.1f}'))
    
    # График 2: Ускорение
    ax2 = axes[1]
    
    for wg in sorted(df['local_size'].unique()):
        subset = df[df['local_size'] == wg]
        ax2.plot(subset['num_hashes'], subset['speedup'], 
                marker='o', linewidth=2, markersize=6,
                label=f'wg={wg}', alpha=0.8)
    
    ax2.set_xlabel('Количество хэшей')
    ax2.set_ylabel('Ускорение (CPU time / GPU time)')
    ax2.set_title('Ускорение GPU относительно CPU')
    ax2.legend(loc='upper left')
    ax2.grid(True, alpha=0.3)
    ax2.set_xscale('log')
    
    # Линия y=1 (без ускорения)
    ax2.axhline(y=1, color='red', linestyle='--', alpha=0.5, label='Без ускорения')
    
    # График 3: Тепловая карта ускорения
    ax3 = axes[2]
    
    pivot_data = df.pivot_table(values='speedup', index='num_hashes', columns='local_size')
    im = ax3.imshow(pivot_data.values, cmap='YlOrRd', aspect='auto')
    
    ax3.set_xlabel('Work-group size')
    ax3.set_ylabel('Количество хэшей')
    ax3.set_title('Тепловая карта ускорения')
    ax3.set_xticks(range(len(pivot_data.columns)))
    ax3.set_xticklabels(pivot_data.columns)
    ax3.set_yticks(range(len(pivot_data.index)))
    ax3.set_yticklabels([f'{x:.0f}' for x in pivot_data.index])
    
    # Добавление значений на тепловую карту
    for i in range(len(pivot_data.index)):
        for j in range(len(pivot_data.columns)):
            value = pivot_data.values[i, j]
            if not pd.isna(value):
                ax3.text(j, i, f'{value:.2f}', ha='center', va='center', 
                        fontsize=8, color='black' if value < 5 else 'white')
    
    plt.colorbar(im, ax=ax3, label='Ускорение (x)')
    
    plt.tight_layout()
    
    output_file = os.path.join(output_dir, 'hash_performance.png')
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"  Сохранён: {os.path.basename(output_file)}")
    plt.close()

def plot_sieve_performance(output_dir, sieve_file):
    """Генерация графиков для решета Эратосфена"""
    if not sieve_file or not os.path.exists(sieve_file):
        print(f"  [WARN] Файл бенчмарка решета не найден")
        return
    
    print(f"  Чтение: {os.path.basename(sieve_file)}")
    
    try:
        df = pd.read_csv(sieve_file)
    except Exception as e:
        print(f"  [ERROR] Ошибка чтения файла: {e}")
        return
    
    if df.empty:
        print("  [WARN] Пустой файл бенчмарка")
        return
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    # График 1: Время выполнения (log-log)
    ax1 = axes[0]
    colors = {'CPU': '#e74c3c', 'GPU': '#3498db'}
    
    for wg in sorted(df['local_size'].unique()):
        subset = df[df['local_size'] == wg]
        ax1.loglog(subset['limit'], subset['cpu_time_ms'], 
                  marker='o', linewidth=2, markersize=6,
                  color=colors['CPU'], label=f'CPU (wg={wg})', alpha=0.8,
                  basex=10, basey=10)
        ax1.loglog(subset['limit'], subset['gpu_time_ms'], 
                  marker='s', linewidth=2, markersize=6,
                  color=colors['GPU'], label=f'GPU (wg={wg})', alpha=0.8,
                  basex=10, basey=10)
    
    ax1.set_xlabel('N (верхняя граница)')
    ax1.set_ylabel('Время выполнения (мс)')
    ax1.set_title('Сравнение производительности CPU vs GPU\n(решето Эратосфена)')
    ax1.legend(loc='upper left')
    ax1.grid(True, alpha=0.3, which='both')
    
    # График 2: Ускорение
    ax2 = axes[1]
    
    for wg in sorted(df['local_size'].unique()):
        subset = df[df['local_size'] == wg]
        ax2.semilogx(subset['limit'], subset['speedup'], 
                    marker='o', linewidth=2, markersize=6,
                    label=f'wg={wg}', alpha=0.8, base=10)
    
    ax2.set_xlabel('N (верхняя граница)')
    ax2.set_ylabel('Ускорение (CPU time / GPU time)')
    ax2.set_title('Ускорение GPU относительно CPU')
    ax2.legend(loc='upper left')
    ax2.grid(True, alpha=0.3)
    
    # Линия y=1
    ax2.axhline(y=1, color='red', linestyle='--', alpha=0.5, label='Без ускорения')
    
    # График 3: Эффективность работы (хэшей/мс)
    ax3 = axes[2]
    
    df['hashes_per_ms'] = df['num_hashes'] / df['gpu_time_ms'].replace(0, 1)
    
    for wg in sorted(df['local_size'].unique()):
        subset = df[df['local_size'] == wg]
        ax3.plot(subset['num_hashes'], subset['hashes_per_ms'], 
                marker='^', linewidth=2, markersize=6,
                label=f'wg={wg}', alpha=0.8)
    
    ax3.set_xlabel('Количество хэшей')
    ax3.set_ylabel('Производительность (хэшей/мс)')
    ax3.set_title('Пропускная способность GPU')
    ax3.legend(loc='upper left')
    ax3.grid(True, alpha=0.3)
    ax3.set_xscale('log')
    ax3.set_yscale('log')
    
    plt.tight_layout()
    
    output_file = os.path.join(output_dir, 'sieve_performance.png')
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"  Сохранён: {os.path.basename(output_file)}")
    plt.close()

def generate_summary_report(output_dir, hash_file, sieve_file):
    """Генерация текстового отчёта"""
    report_file = os.path.join(output_dir, f'benchmark_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')
    
    with open(report_file, 'w') as f:
        f.write("=" * 60 + "\n")
        f.write("ОТЧЁТ ПО БЕНЧМАРКУ GPU Lab\n")
        f.write(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")
        
        if hash_file and os.path.exists(hash_file):
            df = pd.read_csv(hash_file)
            f.write("ХЕШИРОВАНИЕ SHA-256\n")
            f.write("-" * 40 + "\n")
            f.write(f"Всего тестов: {len(df)}\n")
            f.write(f"Диапазон хэшей: {df['num_hashes'].min()} - {df['num_hashes'].max()}\n")
            f.write(f"Work-group sizes: {sorted(df['local_size'].unique())}\n")
            
            if not df['speedup'].empty:
                f.write(f"Среднее ускорение: {df['speedup'].mean():.2f}x\n")
                f.write(f"Максимальное ускорение: {df['speedup'].max():.2f}x\n")
                f.write(f"Минимальное ускорение: {df['speedup'].min():.2f}x\n")
            f.write("\n")
        
        if sieve_file and os.path.exists(sieve_file):
            df = pd.read_csv(sieve_file)
            f.write("\nРЕШЕТО ЭРАТОСФЕНА\n")
            f.write("-" * 40 + "\n")
            f.write(f"Всего тестов: {len(df)}\n")
            f.write(f"Диапазон N: {df['limit'].min():,} - {df['limit'].max():,}\n")
            f.write(f"Work-group sizes: {sorted(df['local_size'].unique())}\n")
            
            if not df['speedup'].empty:
                f.write(f"Среднее ускорение: {df['speedup'].mean():.2f}x\n")
                f.write(f"Максимальное ускорение: {df['speedup'].max():.2f}x\n")
                f.write(f"Минимальное ускорение: {df['speedup'].min():.2f}x\n")
            f.write("\n")
        
        f.write("=" * 60 + "\n")
    
    print(f"  Сохранён: {os.path.basename(report_file)}")

def main():
    output_dir = sys.argv[1] if len(sys.argv) > 1 else 'benchmark_results'
    
    if not os.path.isdir(output_dir):
        print(f"[ERROR] Директория не найдена: {output_dir}")
        sys.exit(1)
    
    print("=" * 50)
    print("  Генерация графиков производительности")
    print(f"  Директория: {output_dir}")
    print("=" * 50)
    print()
    
    # Поиск файлов бенчмарков
    hash_file = find_latest_benchmark_file(output_dir, 'hash')
    sieve_file = find_latest_benchmark_file(output_dir, 'sieve')
    
    print("[INFO] Найденные файлы:")
    print(f"  Хэширование: {os.path.basename(hash_file) if hash_file else 'не найден'}")
    print(f"  Решето:      {os.path.basename(sieve_file) if sieve_file else 'не найден'}")
    print()
    
    # Генерация графиков
    print("[INFO] Генерация графиков...")
    plot_hash_performance(output_dir, hash_file)
    plot_sieve_performance(output_dir, sieve_file)
    
    # Генерация отчёта
    print()
    print("[INFO] Генерация отчёта...")
    generate_summary_report(output_dir, hash_file, sieve_file)
    
    print()
    print("[OK] Готово!")
    print()
    print("Файлы для просмотра:")
    for f in glob.glob(os.path.join(output_dir, '*.png')):
        print(f"  - {os.path.basename(f)}")

if __name__ == '__main__':
    main()
