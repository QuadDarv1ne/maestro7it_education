"""
Команды для управления приложением через CLI
"""
import click
from flask.cli import with_appcontext
from app import db
from app.models import User, Department, Position, Employee
from datetime import datetime


@click.group()
def cli():
    """Команды управления Simple HR"""
    pass


@cli.command()
@with_appcontext
def init_db():
    """Инициализация базы данных"""
    click.echo('Создание таблиц...')
    db.create_all()
    click.echo('✓ База данных инициализирована')


@cli.command()
@with_appcontext
def seed_db():
    """Заполнение базы данных тестовыми данными"""
    click.echo('Создание тестовых данных...')
    
    # Создание администратора
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@example.com',
            role='admin'
        )
        admin.set_password('admin')
        db.session.add(admin)
        click.echo('✓ Создан администратор (admin/admin)')
    
    # Создание HR пользователя
    hr_user = User.query.filter_by(username='hr').first()
    if not hr_user:
        hr_user = User(
            username='hr',
            email='hr@example.com',
            role='hr'
        )
        hr_user.set_password('hr')
        db.session.add(hr_user)
        click.echo('✓ Создан HR пользователь (hr/hr)')
    
    # Создание отделов
    departments = ['IT', 'HR', 'Финансы', 'Маркетинг', 'Продажи']
    for dept_name in departments:
        if not Department.query.filter_by(name=dept_name).first():
            dept = Department(name=dept_name)
            db.session.add(dept)
            click.echo(f'✓ Создан отдел: {dept_name}')
    
    # Создание должностей
    positions = ['Разработчик', 'Менеджер', 'Аналитик', 'Специалист', 'Директор']
    for pos_title in positions:
        if not Position.query.filter_by(title=pos_title).first():
            pos = Position(title=pos_title)
            db.session.add(pos)
            click.echo(f'✓ Создана должность: {pos_title}')
    
    db.session.commit()
    click.echo('✓ База данных заполнена тестовыми данными')


@cli.command()
@click.option('--username', prompt='Имя пользователя', help='Имя пользователя')
@click.option('--email', prompt='Email', help='Email пользователя')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='Пароль')
@click.option('--role', type=click.Choice(['admin', 'hr']), default='hr', help='Роль пользователя')
@with_appcontext
def create_user(username, email, password, role):
    """Создание нового пользователя"""
    if User.query.filter_by(username=username).first():
        click.echo(f'✗ Пользователь {username} уже существует', err=True)
        return
    
    if User.query.filter_by(email=email).first():
        click.echo(f'✗ Email {email} уже используется', err=True)
        return
    
    user = User(username=username, email=email, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    click.echo(f'✓ Пользователь {username} создан с ролью {role}')


@cli.command()
@click.option('--username', prompt='Имя пользователя', help='Имя пользователя')
@with_appcontext
def reset_password(username):
    """Сброс пароля пользователя"""
    user = User.query.filter_by(username=username).first()
    if not user:
        click.echo(f'✗ Пользователь {username} не найден', err=True)
        return
    
    password = click.prompt('Новый пароль', hide_input=True, confirmation_prompt=True)
    user.set_password(password)
    db.session.commit()
    
    click.echo(f'✓ Пароль для {username} успешно изменён')


@cli.command()
@with_appcontext
def list_users():
    """Список всех пользователей"""
    users = User.query.all()
    if not users:
        click.echo('Пользователи не найдены')
        return
    
    click.echo('\nСписок пользователей:')
    click.echo('-' * 60)
    click.echo(f'{"ID":<5} {"Имя":<20} {"Email":<25} {"Роль":<10}')
    click.echo('-' * 60)
    
    for user in users:
        click.echo(f'{user.id:<5} {user.username:<20} {user.email:<25} {user.role:<10}')
    
    click.echo('-' * 60)
    click.echo(f'Всего: {len(users)} пользователей\n')


@cli.command()
@with_appcontext
def stats():
    """Показать статистику базы данных"""
    employee_count = Employee.query.count()
    active_employees = Employee.query.filter_by(status='active').count()
    department_count = Department.query.count()
    position_count = Position.query.count()
    user_count = User.query.count()
    
    click.echo('\n📊 Статистика системы Simple HR')
    click.echo('=' * 50)
    click.echo(f'Сотрудников всего: {employee_count}')
    click.echo(f'Активных сотрудников: {active_employees}')
    click.echo(f'Отделов: {department_count}')
    click.echo(f'Должностей: {position_count}')
    click.echo(f'Пользователей: {user_count}')
    click.echo('=' * 50 + '\n')


@cli.command()
@click.confirmation_option(prompt='Вы уверены? Это удалит ВСЕ данные!')
@with_appcontext
def drop_db():
    """Удаление всех таблиц из базы данных"""
    click.echo('Удаление всех таблиц...')
    db.drop_all()
    click.echo('✓ Все таблицы удалены')


@cli.command()
@with_appcontext
def backup_db():
    """Создание резервной копии базы данных"""
    from app.utils.backup import backup_database
    
    try:
        result = backup_database()
        click.echo(f'✓ Резервная копия создана: {result["filename"]}')
        click.echo(f'  Размер: {result["size"]} bytes')
        click.echo(f'  Время: {result["timestamp"]}')
    except Exception as e:
        click.echo(f'✗ Ошибка при создании резервной копии: {str(e)}', err=True)


@cli.command()
@with_appcontext
def migrate_vacation_status():
    """Добавить поле status в таблицу vacation"""
    click.echo('Выполнение миграции vacation...')
    
    try:
        # Проверяем, есть ли уже колонка status
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        columns = [c['name'] for c in inspector.get_columns('vacation')]
        
        if 'status' in columns:
            click.echo('⚠ Колонка status уже существует')
            return
        
        # Выполняем миграцию через SQLAlchemy
        from sqlalchemy import text
        
        with db.engine.connect() as conn:
            # Для SQLite
            if 'sqlite' in str(db.engine.url):
                click.echo('Миграция для SQLite...')
                conn.execute(text("ALTER TABLE vacation ADD COLUMN status VARCHAR(20) NOT NULL DEFAULT 'approved'"))
                conn.execute(text("ALTER TABLE vacation ADD COLUMN notes TEXT"))
                conn.execute(text("ALTER TABLE vacation ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP"))
                conn.execute(text("ALTER TABLE vacation ADD COLUMN updated_at DATETIME DEFAULT CURRENT_TIMESTAMP"))
                conn.commit()
            # Для MySQL
            else:
                click.echo('Миграция для MySQL...')
                conn.execute(text("ALTER TABLE vacation ADD COLUMN status VARCHAR(20) NOT NULL DEFAULT 'approved'"))
                conn.execute(text("ALTER TABLE vacation ADD COLUMN notes TEXT"))
                conn.execute(text("ALTER TABLE vacation ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP"))
                conn.execute(text("ALTER TABLE vacation ADD COLUMN updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
                conn.execute(text("CREATE INDEX idx_vacation_status ON vacation(status)"))
                conn.commit()
        
        click.echo('✓ Миграция выполнена успешно')
        
        # Обновляем все существующие записи
        from app.models import Vacation
        vacations = Vacation.query.all()
        for v in vacations:
            if not hasattr(v, 'status') or v.status is None:
                v.status = 'approved'
        db.session.commit()
        
        click.echo(f'✓ Обновлено {len(vacations)} записей отпусков')
        
    except Exception as e:
        click.echo(f'✗ Ошибка миграции: {str(e)}', err=True)
        import traceback
        click.echo(traceback.format_exc(), err=True)


@cli.command()
@with_appcontext
def optimize_static():
    """Оптимизация статических файлов (минификация и сжатие)"""
    from app.utils.static_optimizer import optimize_static_files
    
    try:
        from flask import current_app
        stats = optimize_static_files(current_app)
        click.echo('✓ Оптимизация завершена успешно')
    except Exception as e:
        click.echo(f'✗ Ошибка оптимизации: {str(e)}', err=True)


@cli.command()
@with_appcontext
def clear_cache():
    """Очистка всего кэша приложения"""
    from app.utils.redis_cache import cache
    
    try:
        if cache.flush_all():
            click.echo('✓ Кэш успешно очищен')
        else:
            click.echo('⚠ Кэш не включен или не доступен')
    except Exception as e:
        click.echo(f'✗ Ошибка очистки кэша: {str(e)}', err=True)


@cli.command()
@with_appcontext
def cache_stats_cli():
    """Показать статистику кэша"""
    from app.utils.redis_cache import cache_stats
    
    try:
        stats = cache_stats()
        click.echo('\n📊 Статистика кэша')
        click.echo('=' * 50)
        
        if not stats.get('enabled'):
            click.echo('⚠ Кэш выключен')
            if 'error' in stats:
                click.echo(f'Ошибка: {stats["error"]}')
        else:
            click.echo(f'Тип кэша: {stats.get("type", "unknown")}')
            click.echo(f'Количество ключей: {stats.get("keys", 0)}')
            
            if stats.get('type') == 'redis':
                click.echo(f'Попаданий: {stats.get("hits", 0)}')
                click.echo(f'Промахов: {stats.get("misses", 0)}')
                click.echo(f'Использовано памяти: {stats.get("memory_used", "N/A")}')
                
                total = stats.get('hits', 0) + stats.get('misses', 0)
                if total > 0:
                    hit_rate = (stats.get('hits', 0) / total) * 100
                    click.echo(f'Hit Rate: {hit_rate:.1f}%')
        
        click.echo('=' * 50 + '\n')
    except Exception as e:
        click.echo(f'✗ Ошибка получения статистики: {str(e)}', err=True)


def register_commands(app):
    """Регистрация всех команд в приложении"""
    app.cli.add_command(cli)
