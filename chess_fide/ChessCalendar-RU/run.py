import os
from app import create_app
from app.utils.updater import updater

app = create_app()

if __name__ == '__main__':
    # Запускаем автоматическое обновление
    updater.start_scheduler()
    
    # Получаем настройки из конфигурации
    debug_mode = app.config.get('DEBUG', False)
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    
    # Запускаем Flask приложение
    print(f"Starting Chess Calendar RU on {host}:{port}")
    print(f"Debug mode: {debug_mode}")
    app.run(debug=debug_mode, host=host, port=port, threaded=True)