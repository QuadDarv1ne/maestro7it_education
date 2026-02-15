import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-for-chess-calendar'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///chess_calendar.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FIDE_CALENDAR_URL = 'https://calendar.fide.com/calendar.php'
    CFR_URL = 'https://ruchess.ru/'