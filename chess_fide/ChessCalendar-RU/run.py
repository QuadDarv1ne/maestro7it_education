import os
from app import create_app
from app.utils.updater import updater

app = create_app()

if __name__ == '__main__':
    # Запускаем автоматическое обновление
    updater.start_scheduler()
    
    # Получаем настройки из конфигурации
    debug_mode = app.config.get('DEBUG', False)
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_PORT', 5000))
    
    # Запускаем Flask приложение
    app.run(debug=debug_mode, host=host, port=port)