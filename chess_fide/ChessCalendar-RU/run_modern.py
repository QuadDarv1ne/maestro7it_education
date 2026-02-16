"""
Скрипт для запуска улучшенного ChessCalendar-RU с новыми страницами
"""
from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    """Главная страница с новым дизайном"""
    return render_template('index_modern.html')

@app.route('/calendar')
def calendar():
    """Страница календаря"""
    return render_template('calendar_modern.html')

@app.route('/tournaments')
def tournaments():
    """Страница турниров"""
    # Пока используем главную страницу
    return render_template('index_modern.html')

@app.route('/test-responsive-cards')
def test_responsive_cards():
    """Тестовая страница для проверки адаптивных карточек"""
    return render_template('test/test_responsive_cards.html')

@app.route('/test-layout')
def test_layout():
    """Тестовая страница для проверки layout (хедер, футер, spacing)"""
    return render_template('test/test_layout.html')

@app.route('/about')
def about():
    """Страница о проекте"""
    return render_template('base_modern.html')

@app.route('/profile')
def profile():
    """Страница профиля пользователя"""
    return render_template('profile_modern.html')

@app.route('/recommendations')
def recommendations():
    """Страница рекомендаций"""
    return render_template('recommendations_modern.html')

@app.route('/api/tournaments')
def api_tournaments():
    """API для получения турниров"""
    # Тестовые данные
    tournaments = [
        {
            "id": 1,
            "name": "Чемпионат России по шахматам 2026",
            "start_date": "2026-03-15",
            "end_date": "2026-03-25",
            "location": "Москва",
            "category": "National Championship",
            "status": "Scheduled",
            "description": "Ежегодный чемпионат России по классическим шахматам",
            "prize_fund": "2 000 000 руб.",
            "organizer": "Федерация шахмат России"
        },
        {
            "id": 2,
            "name": "Открытый турнир памяти Александра Алехина",
            "start_date": "2026-04-10",
            "end_date": "2026-04-20",
            "location": "Санкт-Петербург",
            "category": "Open Tournament",
            "status": "Scheduled",
            "description": "Международный открытый турнир по классическим шахматам",
            "prize_fund": "1 500 000 руб.",
            "organizer": "Петербургская шахматная федерация"
        }
    ]
    
    return jsonify(tournaments)

if __name__ == '__main__':
    print("🚀 Запуск улучшенного ChessCalendar-RU...")
    print("🌐 Доступные страницы:")
    print("   Главная: http://localhost:5000")
    print("   Календарь: http://localhost:5000/calendar")
    print("   Турниры: http://localhost:5000/tournaments")
    print("   О проекте: http://localhost:5000/about")
    print("\n🧪 Тестовые страницы:")
    print("   Адаптивные карточки: http://localhost:5000/test-responsive-cards")
    print("   Layout (хедер/футер): http://localhost:5000/test-layout")
    print("\n🔧 Разработка в режиме отладки")
    print("   Нажмите Ctrl+C для остановки\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)