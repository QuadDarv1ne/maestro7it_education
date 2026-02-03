# -*- coding: utf-8 -*-
"""
Точка входа для приложения ProfiTest
Запускает Flask-приложение в режиме разработки
"""
from app import create_app

app = create_app()

if __name__ == '__main__':
    # Запуск приложения в режиме разработки
    app.run(debug=True, host='127.0.0.1', port=5000)