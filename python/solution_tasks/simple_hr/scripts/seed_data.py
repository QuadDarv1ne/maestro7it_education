"""
Скрипт для заполнения базы данных тестовыми данными.
Создает пользователей, подразделения, должности, сотрудников, приказы и отпуска.
"""

import sys
import os
from pathlib import Path

# Добавляем корневую директорию проекта в путь для импорта
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app import create_app, db
from app.models import User, Department, Position, Employee, Order, Vacation, Notification, AuditLog
from datetime import date, datetime, timedelta
import random

try:
    from faker import Faker
    FAKER_AVAILABLE = True
except ImportError:
    FAKER_AVAILABLE = False
    print("⚠️  Библиотека Faker не установлена. Используются упрощенные данные.")
    print("   Установите: pip install faker")

# Константы
DEPARTMENTS_DATA = [
    'IT Department', 
    'HR Department', 
    'Finance Department', 
    'Marketing Department', 
    'Support Department',
    'Sales Department',
    'Operations Department',
    'R&D Department'
]

POSITIONS_DATA = [
    'Software Developer',
    'Senior Developer',
    'Team Lead',
    'HR Manager',
    'HR Specialist',
    'Accountant',
    'Senior Accountant',
    'Financial Analyst',
    'Marketing Manager',
    'Marketing Specialist',
    'Support Specialist',
    'Sales Manager',
    'Sales Representative',
    'Operations Manager',
    'Research Engineer',
    'QA Engineer',
    'DevOps Engineer',
    'Product Manager',
    'Business Analyst',
    'Project Manager'
]

ORDER_TYPES = ['hire', 'transfer', 'dismissal']
VACATION_TYPES = ['paid', 'unpaid', 'sick']

def create_users(fake=None):
    """Создание пользователей системы"""
    print("📝 Создание пользователей...")
    users = []
    
    # Администратор
    admin = User()
    admin.username = 'admin'
    admin.email = 'admin@company.com'
    admin.role = 'admin'
    admin.active = True
    admin.set_password('admin123')
    admin.created_at = datetime.utcnow() - timedelta(days=365)
    admin.totp_enabled = False
    admin.totp_secret = None
    users.append(admin)
    
    # HR менеджеры
    for i in range(1, 4):
        hr = User()
        hr.username = f'hr{i}'
        hr.email = f'hr{i}@company.com' if not fake else fake.company_email()
        hr.role = 'hr'
        hr.active = True
        hr.set_password(f'hr{i}123')
        hr.created_at = datetime.utcnow() - timedelta(days=random.randint(100, 300))
        hr.totp_enabled = False
        hr.totp_secret = None
        users.append(hr)
    
    db.session.add_all(users)
    db.session.commit()
    print(f"✅ Создано {len(users)} пользователей")
    return users

def create_departments():
    """Создание подразделений"""
    print("🏢 Создание подразделений...")
    departments = []
    
    for name in DEPARTMENTS_DATA:
        dept = Department()
        dept.name = name
        departments.append(dept)
    
    db.session.add_all(departments)
    db.session.commit()
    print(f"✅ Создано {len(departments)} подразделений")
    return departments

def create_positions():
    """Создание должностей"""
    print("💼 Создание должностей...")
    positions = []
    
    for title in POSITIONS_DATA:
        pos = Position()
        pos.title = title
        positions.append(pos)
    
    db.session.add_all(positions)
    db.session.commit()
    print(f"✅ Создано {len(positions)} должностей")
    return positions

def create_employees(departments, positions, count=50, fake=None):
    """Создание сотрудников"""
    print(f"👥 Создание {count} сотрудников...")
    employees = []
    
    # Даты приема на работу
    start_date = date(2020, 1, 1)
    end_date = date(2025, 10, 1)
    days_range = (end_date - start_date).days
    
    for i in range(1, count + 1):
        emp = Employee()
        
        if fake:
            emp.full_name = fake.name()
            emp.email = fake.company_email()
        else:
            emp.full_name = f'Сотрудник {i}'
            emp.email = f'employee{i}@company.com'
        
        emp.employee_id = f'EMP{i:05d}'
        
        # Случайная дата приема на работу
        random_days = random.randint(0, days_range)
        emp.hire_date = start_date + timedelta(days=random_days)
        
        # 90% активных, 10% уволенных
        emp.status = 'active' if random.random() < 0.9 else 'dismissed'
        
        emp.department_id = departments[random.randint(0, len(departments) - 1)].id
        emp.position_id = positions[random.randint(0, len(positions) - 1)].id
        
        employees.append(emp)
        
        # Коммитим батчами для лучшей производительности
        if i % 100 == 0:
            db.session.add_all(employees)
            db.session.commit()
            employees = []
            print(f"   Создано {i}/{count} сотрудников...")
    
    if employees:
        db.session.add_all(employees)
        db.session.commit()
    
    print(f"✅ Создано {count} сотрудников")
    return Employee.query.all()

def create_orders(employees, departments, positions):
    """Создание приказов"""
    print(f"📋 Создание приказов...")
    orders = []
    
    active_employees = [e for e in employees if e.status == 'active']
    dismissed_employees = [e for e in employees if e.status == 'dismissed']
    
    # Приказы о приеме на работу для всех активных сотрудников
    for emp in active_employees[:min(20, len(active_employees))]:
        order = Order()
        order.employee_id = emp.id
        order.type = 'hire'
        order.date_issued = emp.hire_date
        orders.append(order)
    
    # Приказы о переводе для части активных сотрудников
    transfer_count = min(10, len(active_employees) // 5)
    for emp in random.sample(active_employees, min(transfer_count, len(active_employees))):
        order = Order()
        order.employee_id = emp.id
        order.type = 'transfer'
        # Дата перевода - через некоторое время после приема
        days_after_hire = random.randint(180, 1000)
        order.date_issued = emp.hire_date + timedelta(days=days_after_hire)
        
        # Устанавливаем новое подразделение и/или должность
        if random.random() < 0.7:
            order.new_department_id = random.choice(departments).id
        if random.random() < 0.7:
            order.new_position_id = random.choice(positions).id
        orders.append(order)
    
    # Приказы об увольнении для уволенных сотрудников
    for emp in dismissed_employees:
        order = Order()
        order.employee_id = emp.id
        order.type = 'dismissal'
        # Дата увольнения - через некоторое время после приема
        days_after_hire = random.randint(365, 1500)
        order.date_issued = emp.hire_date + timedelta(days=days_after_hire)
        orders.append(order)
    
    db.session.add_all(orders)
    db.session.commit()
    print(f"✅ Создано {len(orders)} приказов")
    return orders

def create_vacations(employees, count=40):
    """Создание отпусков"""
    print(f"🏖️  Создание {count} отпусков...")
    vacations = []
    
    # Отпуска только для активных сотрудников
    active_employees = [e for e in employees if e.status == 'active']
    
    if not active_employees:
        print("⚠️  Нет активных сотрудников для создания отпусков")
        return vacations
    
    current_year = date.today().year
    
    for i in range(count):
        vacation = Vacation()
        emp = random.choice(active_employees)
        vacation.employee_id = emp.id
        vacation.type = random.choice(VACATION_TYPES)
        
        # Генерация дат отпуска (не раньше даты приема на работу)
        year = random.choice([current_year - 1, current_year, current_year + 1])
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        
        vacation.start_date = date(year, month, day)
        
        # Проверка что отпуск не раньше даты приема
        if vacation.start_date < emp.hire_date:
            vacation.start_date = emp.hire_date + timedelta(days=random.randint(30, 365))
        
        # Длительность отпуска от 7 до 28 дней
        if vacation.type == 'paid':
            duration = random.randint(7, 28)
        elif vacation.type == 'sick':
            duration = random.randint(3, 14)
        else:  # unpaid
            duration = random.randint(5, 20)
        
        vacation.end_date = vacation.start_date + timedelta(days=duration)
        
        # Установка статуса отпуска
        vacation.status = random.choice(['pending', 'approved', 'rejected'])
        
        # Добавление заметок для отклоненных отпусков
        if vacation.status == 'rejected':
            vacation.notes = random.choice([
                'Недостаточно дней для отпуска',
                'Конфликт с рабочим графиком',
                'Необходимо согласование с руководителем'
            ])
        else:
            vacation.notes = None
        
        # Даты создания и обновления
        days_created_ago = random.randint(0, 60)
        vacation.created_at = datetime.utcnow() - timedelta(days=days_created_ago)
        vacation.updated_at = vacation.created_at
        
        vacations.append(vacation)
    
    db.session.add_all(vacations)
    db.session.commit()
    print(f"✅ Создано {count} отпусков")
    return vacations

def create_notifications(users, count=20):
    """Создание уведомлений"""
    print(f"🔔 Создание {count} уведомлений...")
    notifications = []
    
    notification_templates = [
        ("Новый сотрудник", "В компанию принят новый сотрудник."),
        ("Отпуск одобрен", "Ваш отпуск был одобрен."),
        ("Приказ создан", "Создан новый приказ по сотруднику."),
        ("Напоминание", "Не забудьте проверить заявки на отпуск."),
        ("Обновление данных", "Обновлены данные сотрудника."),
        ("Системное уведомление", "Запланировано обновление системы."),
    ]
    
    for i in range(count):
        notification = Notification()
        notification.user_id = random.choice(users).id
        
        title, message = random.choice(notification_templates)
        notification.title = title
        notification.message = message
        notification.is_read = random.choice([True, False])
        
        # Дата за последние 30 дней
        days_ago = random.randint(0, 30)
        notification.created_at = datetime.utcnow() - timedelta(days=days_ago, hours=random.randint(0, 23))
        
        notifications.append(notification)
    
    db.session.add_all(notifications)
    db.session.commit()
    print(f"✅ Создано {count} уведомлений")
    return notifications

def create_audit_logs(users, count=50):
    """Создание логов аудита"""
    print(f"📊 Создание {count} записей аудита...")
    audit_logs = []
    
    actions = ['create', 'update', 'delete', 'login', 'logout', 'view', 'export']
    entity_types = ['employee', 'department', 'position', 'order', 'vacation', 'user']
    
    for i in range(count):
        log = AuditLog()
        log.user_id = random.choice(users).id
        log.action = random.choice(actions)
        log.entity_type = random.choice(entity_types)
        log.entity_id = random.randint(1, 100)
        log.description = f"Действие '{log.action}' над '{log.entity_type}' с ID {log.entity_id}"
        log.ip_address = f"192.168.{random.randint(1, 254)}.{random.randint(1, 254)}"
        log.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        
        # Дата за последние 60 дней
        days_ago = random.randint(0, 60)
        log.created_at = datetime.utcnow() - timedelta(days=days_ago, hours=random.randint(0, 23))
        
        audit_logs.append(log)
    
    db.session.add_all(audit_logs)
    db.session.commit()
    print(f"✅ Создано {count} записей аудита")
    return audit_logs

def main():
    """Основная функция запуска"""
    print("\n" + "="*60)
    print("🚀 ЗАПУСК ЗАПОЛНЕНИЯ БАЗЫ ДАННЫХ ТЕСТОВЫМИ ДАННЫМИ")
    print("="*60 + "\n")
    
    # Установка seed для воспроизводимости результатов
    random.seed(42)
    
    # Создание приложения и контекста
    app = create_app()
    app.app_context().push()
    
    # Инициализация Faker если доступен
    if FAKER_AVAILABLE:
        fake = Faker('ru_RU')
        Faker.seed(42)
    else:
        fake = None
    
    try:
        # Очистка и создание таблиц
        print("🗑️  Очистка базы данных...")
        db.drop_all()
        print("🔨 Создание таблиц...")
        db.create_all()
        print("✅ База данных готова\n")
        
        # Создание данных
        users = create_users(fake)
        departments = create_departments()
        positions = create_positions()
        employees = create_employees(departments, positions, count=50, fake=fake)
        orders = create_orders(employees, departments, positions)
        vacations = create_vacations(employees, count=40)
        notifications = create_notifications(users, count=20)
        audit_logs = create_audit_logs(users, count=50)
        
        # Статистика
        print("\n" + "="*60)
        print("📈 СТАТИСТИКА СОЗДАННЫХ ДАННЫХ")
        print("="*60)
        print(f"Пользователей:        {len(users)}")
        print(f"  - Администраторов:  {len([u for u in users if u.role == 'admin'])}")
        print(f"  - HR менеджеров:    {len([u for u in users if u.role == 'hr'])}")
        print(f"Подразделений:        {len(departments)}")
        print(f"Должностей:           {len(positions)}")
        print(f"Сотрудников:          {len(employees)}")
        print(f"  - Активных:         {len([e for e in employees if e.status == 'active'])}")
        print(f"  - Уволенных:        {len([e for e in employees if e.status == 'dismissed'])}")
        print(f"Приказов:             {len(orders)}")
        print(f"  - О приёме:         {len([o for o in orders if o.type == 'hire'])}")
        print(f"  - О переводе:       {len([o for o in orders if o.type == 'transfer'])}")
        print(f"  - Об увольнении:    {len([o for o in orders if o.type == 'dismissal'])}")
        print(f"Отпусков:             {len(vacations)}")
        print(f"  - Оплачиваемых:     {len([v for v in vacations if v.type == 'paid'])}")
        print(f"  - Неоплачиваемых:   {len([v for v in vacations if v.type == 'unpaid'])}")
        print(f"  - Больничных:       {len([v for v in vacations if v.type == 'sick'])}")
        print(f"  - Одобренных:       {len([v for v in vacations if v.status == 'approved'])}")
        print(f"  - Ожидающих:        {len([v for v in vacations if v.status == 'pending'])}")
        print(f"  - Отклонённых:      {len([v for v in vacations if v.status == 'rejected'])}")
        print(f"Уведомлений:          {len(notifications)}")
        print(f"  - Прочитанных:      {len([n for n in notifications if n.is_read])}")
        print(f"  - Непрочитанных:    {len([n for n in notifications if not n.is_read])}")
        print(f"Записей аудита:       {len(audit_logs)}")
        print("="*60)
        
        print("\n✨ Тестовые данные успешно загружены!")
        print("\n📌 Учетные данные для входа:")
        print("   Администратор: admin / admin123")
        print("   HR менеджер:   hr1 / hr1123")
        print("   HR менеджер:   hr2 / hr2123")
        print("   HR менеджер:   hr3 / hr3123")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ Ошибка при заполнении базы данных: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()