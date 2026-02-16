import sys
import os

# Добавляем текущую директорию в путь Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app import db
from app.models.tournament import Tournament

def test_app():
    """Тестовый запуск приложения"""
    app = create_app()
    
    with app.app_context():
        # Проверяем создание таблиц
        db.create_all()
        print("✓ База данных инициализирована")
        
        # Проверяем наличие турниров
        tournament_count = Tournament.query.count()
        print(f"✓ Найдено турниров в базе: {tournament_count}")
        
    return app

if __name__ == '__main__':
    app = test_app()
    print("✓ Приложение готово к запуску")
    print("Запустите: python run.py")