#!/bin/bash
# =============================================================================
# setup_linux.sh — Скрипт установки зависимостей для Linux
# =============================================================================
# Использование:
#   sudo ./scripts/setup_linux.sh
#
# Поддерживаемые дистрибутивы:
# - Ubuntu/Debian
# - Fedora/RHEL/CentOS
# - Arch Linux/Manjaro
# =============================================================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Проверка root прав
if [ "$EUID" -ne 0 ]; then
    log_error "Требуется запуск от root (sudo)"
    exit 1
fi

# Определение дистрибутива
detect_distro() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        echo "$ID"
    elif [ -f /etc/redhat-release ]; then
        echo "rhel"
    elif [ -f /etc/arch-release ]; then
        echo "arch"
    else
        echo "unknown"
    fi
}

DISTRO=$(detect_distro)
log_info "Обнаружен дистрибутив: $DISTRO"

# =============================================================================
# Установка для Ubuntu/Debian
# =============================================================================
install_ubuntu() {
    log_info "Установка зависимостей для Ubuntu/Debian..."
    
    apt-get update
    
    # Базовые инструменты
    log_info "Установка базовых инструментов..."
    apt-get install -y \
        build-essential \
        cmake \
        git \
        wget \
        curl
    
    # OpenCL (универсальный пакет)
    log_info "Установка OpenCL..."
    apt-get install -y \
        ocl-icd-opencl-dev \
        ocl-icd-libopencl1
    
    # OpenCL для CPU (Mesa - для тестирования без GPU)
    log_info "Установка Mesa OpenCL (CPU backend для тестирования)..."
    apt-get install -y mesa-opencl-icd
    
    # Инструменты для диагностики
    log_info "Установка инструментов диагностики..."
    apt-get install -y clinfo || log_warn "clinfo не доступен"
    
    # Инструменты разработки
    log_info "Установка инструментов разработки..."
    apt-get install -y \
        clang-format \
        clang-tidy \
        cppcheck \
        valgrind
    
    # Python для скриптов
    log_info "Установка Python и библиотек..."
    apt-get install -y \
        python3 \
        python3-pip \
        python3-dev
    
    pip3 install matplotlib pandas numpy || log_warn "Не удалось установить Python библиотеки"
    
    # Doxygen для документации
    log_info "Установка Doxygen..."
    apt-get install -y doxygen graphviz
    
    log_success "Установка завершена!"
    
    # Проверка установки
    echo ""
    log_info "Проверка установки..."
    if command -v clinfo &> /dev/null; then
        echo ""
        log_info "Доступные OpenCL платформы:"
        clinfo | grep -E "Platform Version|Device Name|Device Version" || log_warn "Не удалось получить информацию об OpenCL"
    fi
}

# =============================================================================
# Установка для Fedora/RHEL/CentOS
# =============================================================================
install_fedora() {
    log_info "Установка зависимостей для Fedora/RHEL..."
    
    dnf update -y
    
    # Базовые инструменты
    dnf install -y \
        gcc gcc-c++ \
        cmake \
        git \
        wget
    
    # OpenCL
    dnf install -y \
        ocl-icd-devel \
        ocl-icd
    
    # Mesa OpenCL
    dnf install -y mesa-libOpenCL
    
    # Инструменты разработки
    dnf install -y \
        clang-tools-extra \
        cppcheck
    
    # Python
    dnf install -y \
        python3 \
        python3-pip
    
    pip3 install matplotlib pandas numpy || log_warn "Не удалось установить Python библиотеки"
    
    # Doxygen
    dnf install -y doxygen graphviz
    
    log_success "Установка завершена!"
}

# =============================================================================
# Установка для Arch Linux/Manjaro
# =============================================================================
install_arch() {
    log_info "Установка зависимостей для Arch Linux..."
    
    pacman -Syu --noconfirm
    
    # Базовые инструменты
    pacman -S --noconfirm \
        base-devel \
        cmake \
        git
    
    # OpenCL
    log_info "Установка OpenCL..."
    pacman -S --noconfirm \
        opencl-headers \
        ocl-icd
    
    # Mesa
    pacman -S --noconfirm mesa
    
    # Инструменты
    pacman -S --noconfirm \
        clang \
        cppcheck
    
    # Python
    pacman -S --noconfirm \
        python \
        python-pip
    
    pip3 install matplotlib pandas numpy || log_warn "Не удалось установить Python библиотеки"
    
    # Doxygen
    pacman -S --noconfirm doxygen graphviz
    
    log_success "Установка завершена!"
}

# =============================================================================
# Главная функция
# =============================================================================
main() {
    echo "=============================================="
    echo "  Установка зависимостей GPU Lab"
    echo "  Дистрибутив: $DISTRO"
    echo "=============================================="
    echo ""
    
    case "$DISTRO" in
        ubuntu|debian|linuxmint|pop)
            install_ubuntu
            ;;
        fedora|rhel|centos|rocky|almalinux)
            install_fedora
            ;;
        arch|manjaro|endeavouros)
            install_arch
            ;;
        *)
            log_error "Неподдерживаемый дистрибутив: $DISTRO"
            log_info "Попробуйте установить пакеты вручную:"
            echo "  - ocl-icd-opencl-dev"
            echo "  - ocl-icd-libopencl1"
            echo "  - mesa-opencl-icd"
            echo "  - cmake"
            echo "  - build-essential"
            exit 1
            ;;
    esac
    
    echo ""
    echo "=============================================="
    echo "  Следующие шаги:"
    echo "=============================================="
    echo ""
    echo "1. Соберите проект:"
    echo "   mkdir build && cd build"
    echo "   cmake .."
    echo "   cmake --build ."
    echo ""
    echo "2. Запустите тесты:"
    echo "   ctest --verbose"
    echo ""
    echo "3. Запустите бенчмарки:"
    echo "   ./scripts/benchmark.sh all"
    echo ""
}

main "$@"
