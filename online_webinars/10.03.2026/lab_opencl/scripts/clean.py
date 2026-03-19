#!/usr/bin/env python3
# =============================================================================
# clean.py — Скрипт для очистки build-артефактов проекта
# =============================================================================
# Использование:
#   python scripts/clean.py [options]
#
# Опции:
#   --all         - полная очистка (включая кэш Python)
#   --build       - очистка build директории
#   --cmake       - очистка CMake кэша
#   --make        - очистка Makefile артефактов
#   --test        - очистка тестовых файлов
#   --dry-run     - показать что будет удалено без удаления
#   --verbose     - подробный вывод
#
# Примеры:
#   python scripts/clean.py --build
#   python scripts/clean.py --all --dry-run
# =============================================================================

import os
import sys
import argparse
import shutil
from pathlib import Path
from typing import List, Set

# Цвета для вывода
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def log_info(msg: str):
    print(f"{Colors.BLUE}[INFO]{Colors.END} {msg}")

def log_success(msg: str):
    print(f"{Colors.GREEN}[OK]{Colors.END} {msg}")

def log_warn(msg: str):
    print(f"{Colors.YELLOW}[WARN]{Colors.END} {msg}")

def log_error(msg: str):
    print(f"{Colors.RED}[ERROR]{Colors.END} {msg}")

class ProjectCleaner:
    def __init__(self, project_root: str, dry_run: bool = False, verbose: bool = False):
        self.project_root = Path(project_root)
        self.dry_run = dry_run
        self.verbose = verbose
        self.removed_count = 0
        self.saved_bytes = 0
        
        # Директории для удаления
        self.dirs_to_remove: Set[str] = {
            'build', 'Build', 'BUILD',
            'cmake-build-debug', 'cmake-build-release',
            'bin', 'obj', 'out',
            'docs/html', 'docs/latex',
            'benchmark_results',
            '__pycache__', '.pytest_cache',
            '.vscode', '.idea',
        }
        
        # Файлы для удаления
        self.files_patterns: List[str] = [
            '*.o', '*.obj', '*.a', '*.lib', '*.so', '*.dll', '*.dylib',
            '*.exe', '*.out', '*.ilk', '*.pdb',
            'CMakeCache.txt', 'CMakeFiles', 'cmake_install.cmake',
            'Makefile', '*.make',
            '*.log', '*.tmp', '*.temp',
            '.DS_Store', 'Thumbs.db',
        ]
        
        # Специфичные файлы проекта
        self.project_files: List[str] = [
            'hash', 'hash.exe',
            'sieve', 'sieve.exe',
            'test_sha256', 'test_sha256.exe',
            'test_sieve', 'test_sieve.exe',
            'test_hash_correctness', 'test_hash_correctness.exe',
            'test_sieve_correctness', 'test_sieve_correctness.exe',
        ]

    def get_size(self, path: Path) -> int:
        """Получение размера файла или директории"""
        if path.is_file():
            return path.stat().st_size
        elif path.is_dir():
            return sum(f.stat().st_size for f in path.rglob('*') if f.is_file())
        return 0

    def remove(self, path: Path, description: str = ""):
        """Удаление файла или директории"""
        if not path.exists():
            if self.verbose:
                log_info(f"Пропущено (не найдено): {path}")
            return
        
        size = self.get_size(path)
        
        if self.dry_run:
            log_info(f"Будет удалено: {path} ({description})")
            if size > 0:
                log_info(f"  Размер: {self._format_size(size)}")
        else:
            try:
                if path.is_dir():
                    shutil.rmtree(path)
                else:
                    path.unlink()
                log_success(f"Удалено: {path}")
                self.removed_count += 1
                self.saved_bytes += size
            except Exception as e:
                log_error(f"Не удалось удалить {path}: {e}")

    def _format_size(self, size: int) -> str:
        """Форматирование размера"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"

    def clean_build_dirs(self):
        """Очистка build директорий"""
        log_info("Очистка build директорий...")
        for dir_name in self.dirs_to_remove:
            path = self.project_root / dir_name
            if path.exists():
                self.remove(path, "build directory")

    def clean_makefile_artifacts(self):
        """Очистка артефактов Makefile"""
        log_info("Очистка Makefile артефактов...")
        
        # Рекурсивный поиск Makefile и запуск make clean
        for makefile in self.project_root.rglob('Makefile'):
            if 'build' in str(makefile):
                continue
            log_info(f"Найден Makefile: {makefile}")
            if not self.dry_run:
                os.system(f"make -C {makefile.parent} clean 2>/dev/null")

    def clean_cmake_cache(self):
        """Очистка CMake кэша"""
        log_info("Очистка CMake кэша...")
        cmake_cache = self.project_root / 'CMakeCache.txt'
        cmake_files = self.project_root / 'CMakeFiles'
        
        self.remove(cmake_cache, "CMake cache")
        self.remove(cmake_files, "CMake files")

    def clean_test_artifacts(self):
        """Очистка тестовых файлов"""
        log_info("Очистка тестовых артефактов...")
        
        tests_dir = self.project_root / 'tests'
        if tests_dir.exists():
            for pattern in ['*.exe', '*.o', '*.gcda', '*.gcno', '*.gcov']:
                for file in tests_dir.glob(pattern):
                    self.remove(file, f"test artifact ({pattern})")

    def clean_project_binaries(self):
        """Очистка бинарных файлов проекта"""
        log_info("Очистка бинарных файлов проекта...")
        
        for binary in self.project_files:
            # Корневая директория
            self.remove(self.project_root / binary, "project binary")
            
            # hashing директория
            if binary.startswith('hash'):
                self.remove(self.project_root / 'hashing' / binary, "hashing binary")
            
            # sieve директория
            if binary.startswith('sieve') or binary.startswith('hash'):
                self.remove(self.project_root / 'sieve' / binary, "sieve binary")
            
            # tests директория
            self.remove(self.project_root / 'tests' / binary, "test binary")

    def clean_python_cache(self):
        """Очистка Python кэша"""
        log_info("Очистка Python кэша...")
        
        for pycache in self.project_root.rglob('__pycache__'):
            self.remove(pycache, "Python cache")
        
        for pyc in self.project_root.rglob('*.pyc'):
            self.remove(pyc, "Python compiled")

    def clean_all(self):
        """Полная очистка"""
        self.clean_build_dirs()
        self.clean_cmake_cache()
        self.clean_makefile_artifacts()
        self.clean_test_artifacts()
        self.clean_project_binaries()
        self.clean_python_cache()

    def print_summary(self):
        """Вывод итогов"""
        print()
        print("=" * 50)
        if self.dry_run:
            log_info(f"Режим dry-run: ничего не было удалено")
        else:
            log_success(f"Удалено объектов: {self.removed_count}")
        
        if self.saved_bytes > 0:
            log_info(f"Освобождено места: {self._format_size(self.saved_bytes)}")
        print("=" * 50)


def main():
    parser = argparse.ArgumentParser(
        description='Очистка build-артефактов проекта GPU Lab',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  python scripts/clean.py --build       # Очистка build директории
  python scripts/clean.py --make        # Очистка Makefile артефактов
  python scripts/clean.py --all         # Полная очистка
  python scripts/clean.py --all --dry-run  # Показать что будет удалено
        """
    )
    
    parser.add_argument('--all', action='store_true',
                        help='Полная очистка всех артефактов')
    parser.add_argument('--build', action='store_true',
                        help='Очистка build директории')
    parser.add_argument('--cmake', action='store_true',
                        help='Очистка CMake кэша')
    parser.add_argument('--make', action='store_true',
                        help='Очистка Makefile артефактов (make clean)')
    parser.add_argument('--test', action='store_true',
                        help='Очистка тестовых файлов')
    parser.add_argument('--python', action='store_true',
                        help='Очистка Python кэша')
    parser.add_argument('--dry-run', action='store_true',
                        help='Показать что будет удалено без удаления')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Подробный вывод')
    
    args = parser.parse_args()
    
    # Определение проекта root (2 уровня вверх от скрипта)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent / 'lab_opencl'
    
    if not project_root.exists():
        log_error(f"Директория проекта не найдена: {project_root}")
        sys.exit(1)
    
    log_info(f"Директория проекта: {project_root}")
    log_info(f"Режим: {'dry-run' if args.dry_run else 'удаление'}")
    print()
    
    cleaner = ProjectCleaner(
        str(project_root),
        dry_run=args.dry_run,
        verbose=args.verbose
    )
    
    # Если ни одна опция не указана, показать справку
    if not any([args.all, args.build, args.cmake, args.make, args.test, args.python]):
        parser.print_help()
        print()
        log_info("Ни одна опция не указана. Используйте --help для справки.")
        sys.exit(0)
    
    # Выполнение очистки
    if args.all:
        cleaner.clean_all()
    else:
        if args.build:
            cleaner.clean_build_dirs()
        if args.cmake:
            cleaner.clean_cmake_cache()
        if args.make:
            cleaner.clean_makefile_artifacts()
        if args.test:
            cleaner.clean_test_artifacts()
        if args.python:
            cleaner.clean_python_cache()
    
    cleaner.print_summary()


if __name__ == '__main__':
    main()
