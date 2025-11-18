"""
Скрипт для инициализации базы данных
Создает все таблицы и заполняет начальными данными
"""
from app import create_app, db
from app.models import User, Department, Position, Employee, Order, Vacation, AuditLog, Notification
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import os

def init_database():
    """Инициализация базы данных"""
    app = create_app()
    
    with app.app_context():
        # Удаляем старую БД если существует
        db_path = os.path.join(app.instance_path, 'simple_hr_test.db')
        if os.path.exists(db_path):
            print(f"Удаление старой базы данных: {db_path}")
            os.remove(db_path)
        
        # Создаем все таблицы
        print("Создание таблиц базы данных...")
        db.create_all()
        print("✓ Таблицы созданы успешно")
        
        # Создаем пользователей
        print("\nСоздание пользователей...")
        admin = User(
            username='admin',
            email='admin@example.com',
            role='admin',
            active=True
        )
        admin.set_password('admin')
        
        hr = User(
            username='hr',
            email='hr@example.com',
            role='hr',
            active=True
        )
        hr.set_password('hr')
        
        db.session.add(admin)
        db.session.add(hr)
        print("✓ Создано 2 пользователя (admin, hr)")
        
        # Создаем отделы
        print("\nСоздание отделов...")
        departments = [
            Department(name='IT отдел'),
            Department(name='HR отдел'),
            Department(name='Бухгалтерия'),
            Department(name='Продажи'),
        ]
        for dept in departments:
            db.session.add(dept)
        print(f"✓ Создано {len(departments)} отделов")
        
        # Создаем должности
        print("\nСоздание должностей...")
        positions = [
            Position(title='Разработчик'),
            Position(title='HR менеджер'),
            Position(title='Бухгалтер'),
            Position(title='Менеджер по продажам'),
        ]
        for pos in positions:
            db.session.add(pos)
        print(f"✓ Создано {len(positions)} должностей")
        
        # Коммитим, чтобы получить ID отделов и должностей
        db.session.commit()
        
        # Создаем сотрудников
        print("\nСоздание сотрудников...")
        employees = [
            Employee(
                full_name='Иванов Иван Иванович',
                email='ivanov@example.com',
                employee_id='EMP001',
                hire_date=datetime(2023, 1, 15),
                birth_date=datetime(1990, 5, 20),
                phone='+7 (999) 123-45-67',
                address='Москва, ул. Ленина, 1',
                salary=100000,
                status='active',
                department_id=departments[0].id,
                position_id=positions[0].id
            ),
            Employee(
                full_name='Петрова Мария Сергеевна',
                email='petrova@example.com',
                employee_id='EMP002',
                hire_date=datetime(2023, 2, 10),
                birth_date=datetime(1992, 8, 15),
                phone='+7 (999) 234-56-78',
                address='Москва, ул. Пушкина, 2',
                salary=80000,
                status='active',
                department_id=departments[1].id,
                position_id=positions[1].id
            ),
            Employee(
                full_name='Сидоров Петр Александрович',
                email='sidorov@example.com',
                employee_id='EMP003',
                hire_date=datetime(2023, 3, 5),
                birth_date=datetime(1988, 11, 30),
                phone='+7 (999) 345-67-89',
                address='Москва, ул. Гоголя, 3',
                salary=90000,
                status='active',
                department_id=departments[2].id,
                position_id=positions[2].id
            ),
        ]
        
        for emp in employees:
            db.session.add(emp)
        print(f"✓ Создано {len(employees)} сотрудников")
        
        # Коммитим, чтобы получить ID сотрудников
        db.session.commit()
        
        # Создаем приказы
        print("\nСоздание приказов...")
        orders = [
            Order(
                employee_id=employees[0].id,
                type='hire',
                date_issued=datetime(2023, 1, 15).date(),
            ),
            Order(
                employee_id=employees[1].id,
                type='hire',
                date_issued=datetime(2023, 2, 10).date(),
            ),
        ]
        for order in orders:
            db.session.add(order)
        print(f"✓ Создано {len(orders)} приказов")
        
        # Создаем отпуска
        print("\nСоздание отпусков...")
        vacations = [
            Vacation(
                employee_id=employees[0].id,
                start_date=datetime(2024, 7, 1).date(),
                end_date=datetime(2024, 7, 14).date(),
                type='paid',
                status='approved',
                notes='Ежегодный оплачиваемый отпуск'
            ),
        ]
        for vac in vacations:
            db.session.add(vac)
        print(f"✓ Создано {len(vacations)} отпусков")
        
        # Финальный коммит
        db.session.commit()
        
        print("\n" + "="*50)
        print("✓ База данных успешно инициализирована!")
        print("="*50)
        print("\nДанные для входа:")
        print("  Администратор:")
        print("    Логин: admin")
        print("    Пароль: admin")
        print("\n  HR менеджер:")
        print("    Логин: hr")
        print("    Пароль: hr")
        print("="*50)
        
        return True

if __name__ == '__main__':
    init_database()
