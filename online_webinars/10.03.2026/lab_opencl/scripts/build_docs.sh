#!/bin/bash
# =============================================================================
# build_docs.sh — Скрипт автоматической генерации документации
# =============================================================================
# Использование:
#   ./scripts/build_docs.sh [output_dir]
#
# Требования:
#   - Doxygen
#   - Graphviz (для графиков зависимостей)
#   - LaTeX (опционально, для PDF)
#
# Примеры:
#   ./scripts/build_docs.sh              # Генерация в docs/html
#   ./scripts/build_docs.sh /tmp/docs    # Генерация в указанную директорию
# =============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
OUTPUT_DIR="${1:-$PROJECT_DIR/docs}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# =============================================================================
# Проверка зависимостей
# =============================================================================
check_dependencies() {
    log_info "Проверка зависимостей..."
    
    local missing=0
    
    # Doxygen
    if command -v doxygen &> /dev/null; then
        echo "  [OK] Doxygen: $(doxygen --version)"
    else
        echo "  [MISSING] Doxygen не найден"
        missing=1
    fi
    
    # Graphviz
    if command -v dot &> /dev/null; then
        echo "  [OK] Graphviz: $(dot -V 2>&1 | head -1)"
    else
        echo "  [WARN] Graphviz не найден (графики не будут генерироваться)"
    fi
    
    # LaTeX (опционально)
    if command -v pdflatex &> /dev/null; then
        echo "  [OK] LaTeX: доступен"
    else
        echo "  [INFO] LaTeX не найден (PDF документация не будет генерироваться)"
    fi
    
    if [ $missing -eq 1 ]; then
        log_error "Отсутствуют критические зависимости"
        echo ""
        echo "Установка в Ubuntu/Debian:"
        echo "  sudo apt install doxygen graphviz texlive-latex-base"
        echo ""
        exit 1
    fi
    
    echo ""
}

# =============================================================================
# Генерация Doxygen документации
# =============================================================================
generate_doxygen() {
    local doxyfile="$PROJECT_DIR/Doxyfile"
    
    if [ ! -f "$doxyfile" ]; then
        log_error "Doxyfile не найден: $doxyfile"
        return 1
    fi
    
    log_info "Генерация Doxygen документации..."
    
    # Создание временной копии Doxyfile с нашими настройками
    local temp_doxyfile=$(mktemp)
    cp "$doxyfile" "$temp_doxyfile"
    
    # Обновление настроек
    echo "OUTPUT_DIRECTORY = $OUTPUT_DIR" >> "$temp_doxyfile"
    echo "GENERATE_HTML = YES" >> "$temp_doxyfile"
    echo "GENERATE_LATEX = NO" >> "$temp_doxyfile"
    echo "HAVE_DOT = $(command -v dot &> /dev/null && echo YES || echo NO)" >> "$temp_doxyfile"
    echo "CALL_GRAPH = YES" >> "$temp_doxyfile"
    echo "CALLER_GRAPH = YES" >> "$temp_doxyfile"
    echo "EXTRACT_ALL = YES" >> "$temp_doxyfile"
    echo "EXTRACT_PRIVATE = NO" >> "$temp_doxyfile"
    echo "EXTRACT_STATIC = YES" >> "$temp_doxyfile"
    echo "SOURCE_BROWSER = YES" >> "$temp_doxyfile"
    echo "INLINE_SOURCES = YES" >> "$temp_doxyfile"
    echo "STRIP_CODE_COMMENTS = NO" >> "$temp_doxyfile"
    echo "ALPHABETICAL_INDEX = YES" >> "$temp_doxyfile"
    echo "GENERATE_TREEVIEW = YES" >> "$temp_doxyfile"
    
    # Запуск Doxygen
    cd "$PROJECT_DIR"
    if doxygen "$temp_doxyfile" 2>&1 | tee "$OUTPUT_DIR/doxygen.log"; then
        log_success "Doxygen документация сгенерирована"
    else
        log_warn "Doxygen завершился с предупреждениями"
    fi
    
    # Очистка
    rm -f "$temp_doxyfile"
    
    echo ""
}

# =============================================================================
# Генерация README в различных форматах
# =============================================================================
generate_readme_formats() {
    log_info "Генерация документации из README..."
    
    if [ ! -f "$PROJECT_DIR/README.md" ]; then
        log_warn "README.md не найден"
        return 1
    fi
    
    # Pandoc для конвертации (если доступен)
    if command -v pandoc &> /dev/null; then
        log_info "Конвертация README в различные форматы..."
        
        # HTML
        pandoc "$PROJECT_DIR/README.md" -o "$OUTPUT_DIR/readme.html" \
            --metadata title="GPU Lab - README" \
            --css="$PROJECT_DIR/scripts/github-markdown.css" 2>/dev/null || true
        
        # PDF (требуется LaTeX)
        if command -v pdflatex &> /dev/null; then
            pandoc "$PROJECT_DIR/README.md" -o "$OUTPUT_DIR/readme.pdf" 2>/dev/null || true
        fi
        
        log_success "README сконвертирован"
    else
        log_warn "Pandoc не найден, пропускаем конвертацию README"
    fi
    
    echo ""
}

# =============================================================================
# Генерация отчёта о проекте
# =============================================================================
generate_project_report() {
    log_info "Генерация отчёта о проекте..."
    
    local report_file="$OUTPUT_DIR/project_report.txt"
    
    {
        echo "=============================================="
        echo "ОТЧЁТ О ПРОЕКТЕ GPU Lab"
        echo "Дата: $(date '+%Y-%m-%d %H:%M:%S')"
        echo "=============================================="
        echo ""
        
        echo "1. СТАТИСТИКА КОДА"
        echo "----------------------------------------------"
        echo "C файлы:"
        find "$PROJECT_DIR" -name "*.c" -not -path "*/build/*" -not -path "*/docs/*" | wc -l
        echo "H файлы:"
        find "$PROJECT_DIR" -name "*.h" -not -path "*/build/*" -not -path "*/docs/*" | wc -l
        echo "OpenCL kernel файлы:"
        find "$PROJECT_DIR" -name "*.cl" -not -path "*/build/*" -not -path "*/docs/*" | wc -l
        echo ""
        
        echo "2. СТРОКИ КОДА (примерно)"
        echo "----------------------------------------------"
        local c_lines=$(find "$PROJECT_DIR" -name "*.c" -not -path "*/build/*" -not -path "*/docs/*" -exec cat {} \; | wc -l)
        local h_lines=$(find "$PROJECT_DIR" -name "*.h" -not -path "*/build/*" -not -path "*/docs/*" -exec cat {} \; | wc -l)
        local cl_lines=$(find "$PROJECT_DIR" -name "*.cl" -not -path "*/build/*" -not -path "*/docs/*" -exec cat {} \; | wc -l)
        echo "C код: $c_lines строк"
        echo "H код: $h_lines строк"
        echo "OpenCL kernel: $cl_lines строк"
        echo "Всего: $((c_lines + h_lines + cl_lines)) строк"
        echo ""
        
        echo "3. ФАЙЛЫ ПРОЕКТА"
        echo "----------------------------------------------"
        find "$PROJECT_DIR" -type f -not -path "*/build/*" -not -path "*/docs/*" -not -path "*/.git/*" | wc -l
        echo ""
        
        echo "4. ДОКУМЕНТАЦИЯ"
        echo "----------------------------------------------"
        echo "CHANGELOG.md: $(wc -l < "$PROJECT_DIR/CHANGELOG.md" 2>/dev/null || echo 0) строк"
        echo "CONTRIBUTING.md: $(wc -l < "$PROJECT_DIR/CONTRIBUTING.md" 2>/dev/null || echo 0) строк"
        echo "README.md: $(wc -l < "$PROJECT_DIR/README.md" 2>/dev/null || echo 0) строк"
        echo ""
        
        echo "5. ВЕРСИИ ИНСТРУМЕНТОВ"
        echo "----------------------------------------------"
        echo "GCC: $(gcc --version 2>/dev/null | head -1 || echo 'не найден')"
        echo "CMake: $(cmake --version 2>/dev/null | head -1 || echo 'не найден')"
        echo "Doxygen: $(doxygen --version 2>/dev/null || echo 'не найден')"
        echo "Git: $(git --version 2>/dev/null || echo 'не найден')"
        echo ""
        
        echo "=============================================="
    } > "$report_file"
    
    log_success "Отчёт сохранён: $report_file"
    echo ""
}

# =============================================================================
# Создание index.html с навигацией
# =============================================================================
create_index() {
    log_info "Создание навигационной страницы..."
    
    local index_file="$OUTPUT_DIR/index.html"
    
    cat > "$index_file" << 'EOF'
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GPU Lab Documentation</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            background: white;
            border-radius: 8px;
            padding: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
        h2 { color: #34495e; margin-top: 30px; }
        .links {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .link-card {
            background: #ecf0f1;
            padding: 20px;
            border-radius: 6px;
            text-decoration: none;
            color: #2c3e50;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .link-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }
        .link-card h3 { margin: 0 0 10px 0; color: #3498db; }
        .link-card p { margin: 0; color: #7f8c8d; font-size: 14px; }
        .footer {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ecf0f1;
            color: #7f8c8d;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📚 GPU Lab Documentation</h1>
        <p>Документация проекта "Вычисления на GPU с OpenCL"</p>
        
        <h2>📖 Разделы документации</h2>
        <div class="links">
            <a href="html/index.html" class="link-card">
                <h3>📋 API Reference</h3>
                <p>Полная документация API, сгенерированная Doxygen</p>
            </a>
            <a href="readme.html" class="link-card">
                <h3>📄 README</h3>
                <p>Основная документация проекта</p>
            </a>
            <a href="../CHANGELOG.md" class="link-card">
                <h3>📝 Changelog</h3>
                <p>История изменений проекта</p>
            </a>
            <a href="../CONTRIBUTING.md" class="link-card">
                <h3>🤝 Contributing</h3>
                <p>Руководство для контрибьюторов</p>
            </a>
            <a href="project_report.txt" class="link-card">
                <h3>📊 Project Report</h3>
                <p>Статистика и отчёт о проекте</p>
            </a>
        </div>
        
        <h2>🔧 Быстрые ссылки</h2>
        <ul>
            <li><a href="../">🏠 Главная страница проекта</a></li>
            <li><a href="https://github.com/your-repo/gpu-lab" target="_blank">🌐 GitHub репозиторий</a></li>
        </ul>
        
        <div class="footer">
            <p>Сгенерировано: <script>document.write(new Date().toLocaleString('ru-RU'))</script></p>
            <p>GPU Lab v1.1.0 | Вычисления на GPU с OpenCL</p>
        </div>
    </div>
</body>
</html>
EOF
    
    log_success "Навигационная страница создана: $index_file"
    echo ""
}

# =============================================================================
# Главная функция
# =============================================================================
main() {
    echo "=============================================="
    echo "  Генерация документации GPU Lab"
    echo "  Выходная директория: $OUTPUT_DIR"
    echo "=============================================="
    echo ""
    
    # Создание директории
    mkdir -p "$OUTPUT_DIR"
    
    # Проверка зависимостей
    check_dependencies
    
    # Генерация документации
    generate_doxygen
    generate_readme_formats
    generate_project_report
    create_index
    
    # Итог
    echo "=============================================="
    echo "  Документация сгенерирована!"
    echo "=============================================="
    echo ""
    echo "Файлы для просмотра:"
    echo "  - $OUTPUT_DIR/index.html (главная)"
    echo "  - $OUTPUT_DIR/html/index.html (API)"
    echo "  - $OUTPUT_DIR/project_report.txt (отчёт)"
    echo ""
    echo "Для просмотра откройте в браузере:"
    echo "  file://$OUTPUT_DIR/index.html"
    echo ""
}

main "$@"
