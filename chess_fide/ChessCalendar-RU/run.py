from app import create_app
from app.utils.updater import updater

app = create_app()

if __name__ == '__main__':
    # Запускаем автоматическое обновление
    updater.start_scheduler()
    
    # Запускаем Flask приложение
    app.run(debug=True, host='127.0.0.1', port=5000)