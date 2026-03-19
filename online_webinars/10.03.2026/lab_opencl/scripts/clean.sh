#!/bin/bash
# =============================================================================
# Скрипт очистки проекта от мусора (с сохранением .exe файлов)
# =============================================================================
# Использование:
#   ./clean.sh [--dry-run]
#
# Опции:
#   --dry-run    Показать, что будет удалено, но не удалять
# =============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
DRY_RUN=false
DELETED=0

# Цвета
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Парсинг аргументов
if [ "$1" == "--dry-run" ]; then
    DRY_RUN=true
fi

print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

print_deleted() {
    if [ "$DRY_RUN" = true ]; then
        echo -e "${YELLOW}[ПРОСМОТР]${NC} $1"
    else
        echo -e "${GREEN}[УДАЛЕНО]${NC} $1"
    fi
    ((DELETED++)) || true
}

print_preserved() {
    echo -e "${GREEN}[СОХРАНЕНО]${NC} $1"
}

print_header "Очистка проекта GPU Lab"
echo "Проект: $PROJECT_DIR"
if [ "$DRY_RUN" = true ]; then
    echo -e "Режим: ${YELLOW}ПРОСМОТР (без удаления)${NC}"
else
    echo -e "Режим: ${GREEN}ОЧИСТКА${NC}"
fi
echo "========================================"
echo ""

# =============================================================================
# Удаление файлов по расширениям
# =============================================================================

echo "Удаление временных файлов..."

for ext in o obj a lib so dll dylib gcda gcno gcov log tmp temp bak swp swn swo pdb; do
    while IFS= read -r -d '' file; do
        if [ "$DRY_RUN" = true ]; then
            print_deleted "$file"
        else
            rm -f "$file" && print_deleted "$file"
        fi
    done < <(find "$PROJECT_DIR" -type f -name "*.$ext" -print0 2>/dev/null)
done

# =============================================================================
# Удаление директорий
# =============================================================================

echo ""
echo "Удаление директорий сборки..."

DIRS_TO_DELETE="CMakeFiles _CPack_Packages Testing test_results benchmark_results bin obj CMakeTmp"

for dir in $DIRS_TO_DELETE; do
    if [ -d "$PROJECT_DIR/$dir" ]; then
        if [ "$DRY_RUN" = true ]; then
            print_deleted "$PROJECT_DIR/$dir"
        else
            rm -rf "$PROJECT_DIR/$dir" && print_deleted "$PROJECT_DIR/$dir"
        fi
    fi
done

# Файлы CMake в корне проекта
for file in CMakeCache.txt cmake_install.cmake Makefile compile_commands.json; do
    if [ -f "$PROJECT_DIR/$file" ]; then
        if [ "$DRY_RUN" = true ]; then
            print_deleted "$PROJECT_DIR/$file"
        else
            rm -f "$PROJECT_DIR/$file" && print_deleted "$PROJECT_DIR/$file"
        fi
    fi
done

# =============================================================================
# Python кэш
# =============================================================================

echo ""
echo "Удаление Python кэша..."

if [ -d "$PROJECT_DIR/__pycache__" ]; then
    if [ "$DRY_RUN" = true ]; then
        print_deleted "$PROJECT_DIR/__pycache__"
    else
        rm -rf "$PROJECT_DIR/__pycache__" && print_deleted "$PROJECT_DIR/__pycache__"
    fi
fi

while IFS= read -r -d '' file; do
    if [ "$DRY_RUN" = true ]; then
        print_deleted "$file"
    else
        rm -f "$file" && print_deleted "$file"
    fi
done < <(find "$PROJECT_DIR" -type f \( -name "*.pyc" -o -name "*.pyo" -o -name "*$py.class" \) -print0 2>/dev/null)

# =============================================================================
# Сохранённые файлы
# =============================================================================

echo ""
echo "========================================"
echo -e "${GREEN}СОХРАНЁННЫЕ файлы (.exe):${NC}"
echo "========================================"

while IFS= read -r -d '' file; do
    print_preserved "$file"
done < <(find "$PROJECT_DIR" -type f -name "*.exe" -print0 2>/dev/null)

# =============================================================================
# Итоги
# =============================================================================

echo ""
echo "========================================"
echo "Всего удалено: $DELETED"
echo "========================================"
echo ""

if [ "$DRY_RUN" = true ]; then
    echo "Для фактического удаления запустите: ./clean.sh (без --dry-run)"
fi
