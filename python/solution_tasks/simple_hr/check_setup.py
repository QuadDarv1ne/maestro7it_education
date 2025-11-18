"""
Быстрый тест для проверки корректности настройки проекта Simple HR.
Запустите этот скрипт перед первым запуском приложения.
"""

import sys
import os
from pathlib import Path

# Цвета для вывода
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_success(msg):
    print(f"{GREEN}✓ {msg}{RESET}")

def print_error(msg):
    print(f"{RED}✗ {msg}{RESET}")

def print_warning(msg):
    print(f"{YELLOW}⚠ {msg}{RESET}")

def print_info(msg):
    print(f"{BLUE}ℹ {msg}{RESET}")

def check_python_version():
    """Проверка версии Python"""
    print_info("Проверка версии Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print_success(f"Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print_error(f"Python {version.major}.{version.minor} - требуется Python 3.8+")
        return False

def check_required_packages():
    """Проверка установленных пакетов"""
    print_info("\nПроверка необходимых пакетов...")
    required_packages = [
        'flask',
        'flask_sqlalchemy',
        'flask_login',
        'flask_migrate',
        'flask_wtf',
        'flask_limiter',
        'flask_caching',
        'flask_cors',
        'werkzeug',
        'sqlalchemy',
        'pandas',
        'matplotlib',
        'plotly',
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print_success(f"{package}")
        except ImportError:
            print_error(f"{package} - НЕ УСТАНОВЛЕН")
            missing_packages.append(package)
    
    if missing_packages:
        print_warning(f"\nУстановите отсутствующие пакеты: pip install -r requirements.txt")
        return False
    return True

def check_config_files():
    """Проверка конфигурационных файлов"""
    print_info("\nПроверка конфигурационных файлов...")
    
    files_to_check = {
        'instance/config.py': 'Конфигурация приложения',
        '.env': 'Переменные окружения',
        'requirements.txt': 'Зависимости Python',
        'app/__init__.py': 'Инициализация приложения',
        'app/models.py': 'Модели данных',
        'run.py': 'Точка входа',
    }
    
    all_exist = True
    for file_path, description in files_to_check.items():
        if Path(file_path).exists():
            print_success(f"{file_path} - {description}")
        else:
            print_error(f"{file_path} - ОТСУТСТВУЕТ")
            all_exist = False
    
    return all_exist

def check_directories():
    """Проверка необходимых директорий"""
    print_info("\nПроверка директорий...")
    
    dirs_to_check = [
        'app/templates',
        'app/static',
        'app/routes',
        'app/utils',
        'instance',
        'scripts',
    ]
    
    all_exist = True
    for dir_path in dirs_to_check:
        if Path(dir_path).exists():
            print_success(f"{dir_path}/")
        else:
            print_error(f"{dir_path}/ - ОТСУТСТВУЕТ")
            all_exist = False
    
    # Создаём logs если нет
    if not Path('logs').exists():
        Path('logs').mkdir()
        print_warning("Создана директория logs/")
    else:
        print_success("logs/")
    
    # Создаём uploads если нет
    if not Path('uploads').exists():
        Path('uploads').mkdir()
        print_warning("Создана директория uploads/")
    else:
        print_success("uploads/")
    
    return all_exist

def check_env_variables():
    """Проверка переменных окружения"""
    print_info("\nПроверка переменных окружения (.env)...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        important_vars = {
            'SECRET_KEY': 'Секретный ключ Flask',
            'DATABASE_URL': 'URL базы данных',
        }
        
        for var, description in important_vars.items():
            value = os.getenv(var)
            if value:
                # Скрываем значение для безопасности
                masked = value[:10] + '...' if len(value) > 10 else '***'
                print_success(f"{var} = {masked} - {description}")
            else:
                print_warning(f"{var} - НЕ УСТАНОВЛЕНА (будет использовано значение по умолчанию)")
        
        return True
    except ImportError:
        print_error("python-dotenv не установлен")
        return False

def test_import_app():
    """Тест импорта приложения"""
    print_info("\nТест импорта приложения...")
    
    try:
        # Добавляем текущую директорию в путь
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        from app import create_app, db
        app = create_app()
        
        print_success("Приложение успешно импортировано")
        print_success(f"Flask app: {app.name}")
        print_success(f"Database URI: {app.config.get('SQLALCHEMY_DATABASE_URI', 'не настроен')[:50]}...")
        
        return True
    except Exception as e:
        print_error(f"Ошибка импорта: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_database_connection():
    """Тест подключения к базе данных"""
    print_info("\nТест подключения к базе данных...")
    
    try:
        from app import create_app, db
        app = create_app()
        
        with app.app_context():
            # Попытка подключения
            db.engine.connect()
            print_success("Подключение к базе данных успешно")
            
            # Проверка таблиц
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            if tables:
                print_success(f"Найдено {len(tables)} таблиц в базе данных")
            else:
                print_warning("База данных пуста. Запустите: python scripts/seed_data.py")
            
            return True
    except Exception as e:
        print_error(f"Ошибка подключения к БД: {str(e)}")
        print_warning("Возможно, база данных не создана. Запустите: python scripts/seed_data.py")
        return False

def main():
    """Основная функция проверки"""
    print("\n" + "="*60)
    print(f"{BLUE}ПРОВЕРКА ГОТОВНОСТИ ПРОЕКТА SIMPLE HR{RESET}")
    print("="*60 + "\n")
    
    results = []
    
    # Запускаем все проверки
    results.append(("Python версия", check_python_version()))
    results.append(("Пакеты Python", check_required_packages()))
    results.append(("Конфигурационные файлы", check_config_files()))
    results.append(("Директории", check_directories()))
    results.append(("Переменные окружения", check_env_variables()))
    results.append(("Импорт приложения", test_import_app()))
    results.append(("База данных", test_database_connection()))
    
    # Итоги
    print("\n" + "="*60)
    print(f"{BLUE}ИТОГИ ПРОВЕРКИ{RESET}")
    print("="*60 + "\n")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = f"{GREEN}✓ PASSED{RESET}" if result else f"{RED}✗ FAILED{RESET}"
        print(f"{name:30} {status}")
    
    print("\n" + "-"*60)
    print(f"Успешно: {passed}/{total}")
    
    if passed == total:
        print(f"\n{GREEN}✓ ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ!{RESET}")
        print(f"\n{BLUE}Следующие шаги:{RESET}")
        print("1. Заполните базу данных: python scripts/seed_data.py")
        print("2. Запустите приложение: python run.py")
        print("3. Откройте в браузере: http://localhost:5000")
        print("\nУчётные данные:")
        print("  Администратор: admin / admin123")
        print("  HR менеджер:   hr1 / hr1123")
    else:
        print(f"\n{YELLOW}⚠ НЕКОТОРЫЕ ПРОВЕРКИ НЕ ПРОЙДЕНЫ{RESET}")
        print("Исправьте ошибки перед запуском приложения.")
    
    print("\n")
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
