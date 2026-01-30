@echo off
chcp 65001 >nul
cls
echo.
echo ========================================
echo   Chess FastAPI Server v2.0 Enhanced
echo ========================================
echo.
echo Запуск улучшенного FastAPI сервера...
echo.
echo Новые возможности:
echo   - Rate limiting (защита от DDoS)
echo   - Кэширование AI ходов
echo   - Улучшенная валидация данных
echo   - Расширенное логирование
echo   - Метрики производительности
echo   - Индикатор загрузки на фронтенде
echo.
echo Сервер будет доступен по адресу:
echo   http://localhost:8000
echo.
echo Нажмите Ctrl+C для остановки сервера
echo ========================================
echo.

py -3.13 -m uvicorn interfaces.fastapi_chess:app --host 0.0.0.0 --port 8000 --reload

pause
