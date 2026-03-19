@echo off
REM =============================================================================
REM setup_windows.bat — Скрипт установки зависимостей для Windows
REM =============================================================================
REM Использование:
REM   scripts\setup_windows.bat [admin]
REM
REM Примечание: Запуск от имени администратора рекомендуется
REM =============================================================================

setlocal enabledelayedexpansion

echo ==============================================
echo   Установка зависимостей GPU Lab (Windows)
echo ==============================================
echo.

REM Проверка прав администратора
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [WARN] Рекомендуется запуск от имени администратора
    echo       Перезапустите скрипт с правами администратора
    echo.
)

REM =============================================================================
REM Проверка winget
REM =============================================================================
:check_winget
where winget >nul 2>&1
if %errorLevel% neq 0 (
    echo [WARN] winget не найден
    echo       Установите App Installer из Microsoft Store
    echo       https://aka.ms/winget
    echo.
    goto :manual_install
)

echo [INFO] winget найден
echo.

REM =============================================================================
REM Установка Visual Studio Build Tools
REM =============================================================================
:install_vs_build
echo [INFO] Проверка установки Visual Studio Build Tools...
where cl >nul 2>&1
if %errorLevel% equ 0 (
    echo [OK] Visual C++ компилятор найден
) else (
    echo [INFO] Установка Visual Studio Build Tools...
    winget install --id Microsoft.VisualStudio.2022.BuildTools --silent --override "--wait --quiet --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended"
    if %errorLevel% equ 0 (
        echo [OK] Visual Studio Build Tools установлен
    ) else (
        echo [WARN] Не удалось установить через winget
    )
)
echo.

REM =============================================================================
REM Установка CMake
REM =============================================================================
:install_cmake
echo [INFO] Проверка установки CMake...
where cmake >nul 2>&1
if %errorLevel% equ 0 (
    echo [OK] CMake найден
) else (
    echo [INFO] Установка CMake...
    winget install --id Kitware.CMake --silent
    if %errorLevel% equ 0 (
        echo [OK] CMake установлен
    ) else (
        echo [WARN] Не удалось установить CMake через winget
        echo       Скачайте с https://cmake.org/download/
    )
)
echo.

REM =============================================================================
REM Установка Git
REM =============================================================================
:install_git
echo [INFO] Проверка установки Git...
where git >nul 2>&1
if %errorLevel% equ 0 (
    echo [OK] Git найден
) else (
    echo [INFO] Установка Git...
    winget install --id Git.Git --silent
    if %errorLevel% equ 0 (
        echo [OK] Git установлен
    ) else (
        echo [WARN] Не удалось установить Git
    )
)
echo.

REM =============================================================================
REM Установка OpenCL
REM =============================================================================
:install_opencl
echo [INFO] Проверка OpenCL...
REM OpenCL обычно устанавливается с драйверами GPU
echo [INFO] OpenCL поставляется с драйверами GPU:
echo       - NVIDIA: https://www.nvidia.com/Download/index.aspx
echo       - AMD: https://www.amd.com/en/support
echo       - Intel: https://www.intel.com/content/www/us/en/download-center/
echo.

REM Проверка наличия OpenCL.dll
if exist "C:\Windows\System32\OpenCL.dll" (
    echo [OK] OpenCL.dll найден в System32
) else (
    echo [WARN] OpenCL.dll не найден
    echo       Установите драйверы вашего GPU
)
echo.

REM =============================================================================
REM Установка Python
REM =============================================================================
:install_python
echo [INFO] Проверка установки Python...
where python >nul 2>&1
if %errorLevel% equ 0 (
    echo [OK] Python найден
) else (
    echo [INFO] Установка Python 3...
    winget install --id Python.Python.3.11 --silent
    if %errorLevel% equ 0 (
        echo [OK] Python установлен
    ) else (
        echo [WARN] Не удалось установить Python
    )
)
echo.

REM Установка Python библиотек
:install_python_libs
echo [INFO] Установка Python библиотек для графиков...
pip install matplotlib pandas numpy --quiet
if %errorLevel% equ 0 (
    echo [OK] Python библиотеки установлены
) else (
    echo [WARN] Не удалось установить Python библиотеки
    echo       Попробуйте: pip install matplotlib pandas numpy
)
echo.

REM =============================================================================
REM Ручная установка
REM =============================================================================
:manual_install
echo ==============================================
echo   Ручная установка (если автоматическая не сработала)
echo ==============================================
echo.
echo 1. Visual Studio Build Tools:
echo    https://visualstudio.microsoft.com/downloads/
echo    Выберите "Build Tools for Visual Studio"
echo.
echo 2. CMake:
echo    https://cmake.org/download/
echo.
echo 3. Git:
echo    https://git-scm.com/download/win
echo.
echo 4. Драйверы GPU (содержат OpenCL):
echo    - NVIDIA: https://www.nvidia.com/Download/index.aspx
echo    - AMD: https://www.amd.com/en/support
echo    - Intel: https://www.intel.com/content/www/us/en/download-center/
echo.
echo 5. Python 3:
echo    https://www.python.org/downloads/
echo    Затем: pip install matplotlib pandas numpy
echo.

REM =============================================================================
REM Проверка установки
REM =============================================================================
:verify_install
echo ==============================================
echo   Проверка установки
echo ==============================================
echo.

echo [INFO] Проверка компилятора...
where cl >nul 2>&1 && echo   [OK] Visual C++ компилятор || echo   [ ] Visual C++ компилятор

echo [INFO] Проверка CMake...
where cmake >nul 2>&1 && echo   [OK] CMake || echo   [ ] CMake

echo [INFO] Проверка Git...
where git >nul 2>&1 && echo   [OK] Git || echo   [ ] Git

echo [INFO] Проверка Python...
where python >nul 2>&1 && echo   [OK] Python || echo   [ ] Python

echo [INFO] Проверка OpenCL...
if exist "C:\Windows\System32\OpenCL.dll" (echo   [OK] OpenCL) else (echo   [ ] OpenCL)

echo.
echo ==============================================
echo   Следующие шаги
echo ==============================================
echo.
echo 1. Откройте Command Prompt в директории проекта
echo 2. Выполните:
echo    mkdir build
echo    cd build
echo    cmake .. -G "Visual Studio 17 2022" -A x64
echo    cmake --build . --config Release
echo.
echo 3. Запустите тесты:
echo    ctest -C Release --verbose
echo.

echo [OK] Установка завершена!
pause
