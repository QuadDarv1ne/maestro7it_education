@echo off
REM 
REM Примеры запуска проекта анализа товаров Ozon
REM 

echo ============================================
echo Примеры запуска проекта анализа товаров Ozon
echo ============================================
echo.

:menu
echo.
echo Выберите действие:
echo 1. Полный анализ (инициализация + аналитика + экспорт)
echo 2. Только инициализация базы данных
echo 3. Только запуск аналитики
echo 4. Только экспорт данных
echo 5. Запуск расширенной аналитики
echo 6. Тестирование установки DuckDB
echo 7. Просмотр содержимого базы данных
echo 0. Выход
echo.

set /p choice="Введите номер (0-7): "

if "%choice%"=="1" goto full_analysis
if "%choice%"=="2" goto init_db
if "%choice%"=="3" goto run_analytics
if "%choice%"=="4" goto export_data
if "%choice%"=="5" goto advanced_analytics
if "%choice%"=="6" goto test_duckdb
if "%choice%"=="7" goto view_db
if "%choice%"=="0" goto exit_script

echo Неверный выбор. Пожалуйста, введите число от 0 до 7.
goto menu

:full_analysis
echo.
echo Запуск полного анализа...
python main.py --full-analysis
pause
goto menu

:init_db
echo.
echo Инициализация базы данных...
python main.py --init-db
pause
goto menu

:run_analytics
echo.
echo Запуск аналитики...
python main.py --run-analytics
pause
goto menu

:export_data
echo.
echo Экспорт данных...
python main.py --export-data
pause
goto menu

:advanced_analytics
echo.
echo Запуск расширенной аналитики...
python analytics.py
pause
goto menu

:test_duckdb
echo.
echo Тестирование установки DuckDB...
python test_duckdb.py
pause
goto menu

:view_db
echo.
echo Просмотр содержимого базы данных...
python -c "import duckdb; con = duckdb.connect('ozon_products.duckdb'); print('Таблицы в базе:'); print(con.execute('SHOW TABLES;').fetchdf()); print('Количество товаров:'); print(con.execute('SELECT COUNT(*) as count FROM ozon_products;').fetchdf()); con.close()"
pause
goto menu

:exit_script
echo.
echo Завершение работы...
exit /b