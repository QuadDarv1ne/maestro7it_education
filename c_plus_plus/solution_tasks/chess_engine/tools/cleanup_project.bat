@echo off
chcp 65001 >nul
title Очистка проекта шахмат
cls

echo ========================================
echo    ОЧИСТКА ПРОЕКТА ШАХМАТ
echo ========================================
echo.

echo 🧹 Удаление временных и устаревших файлов...
echo.

rem Удаление старых Python файлов
echo Удаляю устаревшие Python файлы...
del /Q pro_chess.py 2>nul
del /Q stable_chess.py 2>nul
del /Q fixed_pygame.py 2>nul

echo Удаляю временные файлы...
if exist build rmdir /s /q build
if exist build_gui rmdir /s /q build_gui
if exist __pycache__ rmdir /s /q __pycache__
for /d %%i in (*.__pycache__) do rmdir /s /q "%%i"
del /q *.pyc 2>nul
del /q *.pyo 2>nul
del /q *.log 2>nul

echo Удаляю старые исполняемые файлы...
del /q engine_demo_latin.exe 2>nul
del /q test_chess_latin.exe 2>nul

echo Удаляю старые bat-файлы...
del /Q main_menu.bat 2>nul
del /Q run_pygame.bat 2>nul
del /Q run_stable.bat 2>nul
del /Q run_web.bat 2>nul

echo Удаляю файлы сборки C++...
del /q *.obj 2>nul
del /q *.dll 2>nul
del /q *.lib 2>nul

echo.
echo ✅ Очистка завершена!
echo.
echo 📋 Что было удалено:
echo    • Устаревшие Python файлы (pro_chess.py, stable_chess.py, fixed_pygame.py)
echo    • Директории сборки (build, build_gui)
echo    • Файлы кэша Python (__pycache__)
echo    • Старые исполняемые файлы
echo    • Устаревшие bat-файлы
echo    • Временные файлы компиляции
echo.
echo 📁 Остались только необходимые файлы:
echo    • chess_launcher.py - главное меню
echo    • full_chess_game.py - консольная версия
echo    • pygame_chess.py - графическая версия
echo    • chess_engine_wrapper.py - C++ движок
echo    • run_chess.bat - запуск меню
echo    • run_full_chess.bat - прямой запуск
echo.
pause