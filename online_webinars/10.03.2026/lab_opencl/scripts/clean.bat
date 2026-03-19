@echo off
chcp 65001 >nul
REM =============================================================================
REM GPU Lab Clean Script - Очистка от мусора (с сохранением .exe)
REM =============================================================================
REM Использование: clean.bat [--dry-run]
REM   --dry-run  - показать что будет удалено, но не удалять
REM =============================================================================

setlocal enabledelayedexpansion

set SCRIPT_DIR=%~dp0
set PROJECT_DIR=%SCRIPT_DIR:~0,-1%
if "%SCRIPT_DIR:~-8%"=="scripts\" set PROJECT_DIR=%SCRIPT_DIR:~0,-9%
set DRY_RUN=%1
set DELETED=0

if "%DRY_RUN%"=="--dry-run" (
    echo [DRY-RUN MODE]
    echo.
)

echo ========================================
echo GPU Lab Clean
echo ========================================
echo Project: %PROJECT_DIR%
echo.

REM Очистка расширений
for %%e in (o obj a lib so dll dylib gcda gcno gcov log tmp temp bak swp swn swo pdb pyc pyo) do (
    for /f "delims=" %%f in ('dir /s /b *.%%e 2^>nul') do (
        if "%DRY_RUN%"=="--dry-run" (
            echo [SKIP] %%f
            set /a DELETED+=1
        ) else (
            del /q "%%f" >nul 2>&1 && (
                echo [DEL] %%f
                set /a DELETED+=1
            )
        )
    )
)

REM Очистка директорий
for %%d in (CMakeFiles _CPack_Packages Testing test_results benchmark_results bin obj CMakeTmp __pycache__) do (
    if exist "%PROJECT_DIR%\%%d" (
        if "%DRY_RUN%"=="--dry-run" (
            echo [SKIP DIR] %%d
            set /a DELETED+=1
        ) else (
            rmdir /s /q "%PROJECT_DIR%\%%d" 2>nul && (
                echo [DEL DIR] %%d
                set /a DELETED+=1
            )
        )
    )
)

REM Файлы CMake
for %%f in (CMakeCache.txt cmake_install.cmake Makefile compile_commands.json) do (
    if exist "%PROJECT_DIR%\%%f" (
        if "%DRY_RUN%"=="--dry-run" (
            echo [SKIP] %%f
            set /a DELETED+=1
        ) else (
            del /q "%PROJECT_DIR%\%%f" >nul 2>&1 && (
                echo [DEL] %%f
                set /a DELETED+=1
            )
        )
    )
)

REM Сохранённые файлы
echo.
echo ========================================
echo PRESERVED (.exe files):
echo ========================================
for /f "delims=" %%f in ('dir /s /b *.exe 2^>nul') do (
    echo [KEEP] %%f
)

echo.
echo ========================================
echo Total: %DELETED%
echo ========================================
if "%DRY_RUN%"=="--dry-run" echo (Run without --dry-run to actually delete)
echo.

endlocal
