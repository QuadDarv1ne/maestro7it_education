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
echo 8. Проверка качества данных
echo 9. Мониторинг производительности
echo 10. Резервное копирование
echo 11. Полная демонстрация проекта
echo 12. Оптимизация запросов
echo 13. Визуализация данных
echo 14. Восстановление после ошибок
echo 15. Миграции базы данных
echo 0. Выход
echo.

set /p choice="Введите номер (0-15): "

if "%choice%"=="1" goto full_analysis
if "%choice%"=="2" goto init_db
if "%choice%"=="3" goto run_analytics
if "%choice%"=="4" goto export_data
if "%choice%"=="5" goto advanced_analytics
if "%choice%"=="6" goto test_duckdb
if "%choice%"=="7" goto view_db
if "%choice%"=="8" goto data_validation
if "%choice%"=="9" goto perf_monitor
if "%choice%"=="10" goto backup_manager
if "%choice%"=="11" goto demo_complete
if "%choice%"=="12" goto query_opt
if "%choice%"=="13" goto data_viz
if "%choice%"=="14" goto error_recov
if "%choice%"=="15" goto db_migrate
if "%choice%"=="0" goto exit_script

echo Неверный выбор. Пожалуйста, введите число от 0 до 15.
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

:data_validation
echo.
echo Проверка качества данных...
python data_validator.py
pause
goto menu

:perf_monitor
echo.
echo Мониторинг производительности...
python performance_monitor.py
pause
goto menu

:backup_manager
echo.
echo Резервное копирование...
python backup_manager.py
pause
goto menu

:demo_complete
echo.
echo Полная демонстрация проекта...
python demo_complete.py
pause
goto menu

:query_opt
echo.
echo Оптимизация запросов...
python query_optimizer.py
pause
goto menu

:data_viz
echo.
echo Визуализация данных...
python data_visualizer.py
pause
goto menu

:error_recov
echo.
echo Восстановление после ошибок...
python error_recovery.py
pause
goto menu

:db_migrate
echo.
echo Миграции базы данных...
python db_migration.py
pause
goto menu

:exit_script
echo.
echo Завершение работы...
exit /b