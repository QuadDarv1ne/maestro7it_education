import os
import json
import csv
from datetime import datetime
from app.models import Employee, Department, Position, Vacation, Order, User
from app import db

def backup_database(backup_dir='backups'):
    """Создание резервной копии базы данных"""
    # Создаем директорию для бэкапов, если она не существует
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    # Генерируем имя файла с временной меткой
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f'hr_backup_{timestamp}'
    
    # Экспортируем данные в JSON
    json_path = os.path.join(backup_dir, f'{backup_filename}.json')
    export_to_json(json_path)
    
    # Экспортируем данные в CSV
    csv_dir = os.path.join(backup_dir, f'{backup_filename}_csv')
    if not os.path.exists(csv_dir):
        os.makedirs(csv_dir)
    export_to_csv(csv_dir)
    
    return {
        'json_file': json_path,
        'csv_directory': csv_dir,
        'timestamp': timestamp
    }

def export_to_json(filepath):
    """Экспорт всех данных в JSON файл"""
    backup_data = {
        'metadata': {
            'created_at': datetime.now().isoformat(),
            'version': '1.0'
        },
        'employees': [],
        'departments': [],
        'positions': [],
        'vacations': [],
        'orders': [],
        'users': []
    }
    
    # Экспорт сотрудников
    employees = Employee.query.all()
    for emp in employees:
        backup_data['employees'].append({
            'id': emp.id,
            'full_name': emp.full_name,
            'email': emp.email,
            'employee_id': emp.employee_id,
            'hire_date': emp.hire_date.isoformat() if emp.hire_date else None,
            'department_id': emp.department_id,
            'position_id': emp.position_id,
            'status': emp.status
        })
    
    # Экспорт подразделений
    departments = Department.query.all()
    for dept in departments:
        backup_data['departments'].append({
            'id': dept.id,
            'name': dept.name
        })
    
    # Экспорт должностей
    positions = Position.query.all()
    for pos in positions:
        backup_data['positions'].append({
            'id': pos.id,
            'title': pos.title
        })
    
    # Экспорт отпусков
    vacations = Vacation.query.all()
    for vac in vacations:
        backup_data['vacations'].append({
            'id': vac.id,
            'employee_id': vac.employee_id,
            'start_date': vac.start_date.isoformat() if vac.start_date else None,
            'end_date': vac.end_date.isoformat() if vac.end_date else None,
            'type': vac.type
        })
    
    # Экспорт приказов
    orders = Order.query.all()
    for order in orders:
        backup_data['orders'].append({
            'id': order.id,
            'employee_id': order.employee_id,
            'type': order.type,
            'date_issued': order.date_issued.isoformat() if order.date_issued else None,
            'new_department_id': order.new_department_id,
            'new_position_id': order.new_position_id
        })
    
    # Экспорт пользователей (без паролей)
    users = User.query.all()
    for user in users:
        backup_data['users'].append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'is_active': user.is_active
        })
    
    # Записываем данные в файл
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(backup_data, f, ensure_ascii=False, indent=2)

def export_to_csv(backup_dir):
    """Экспорт всех данных в CSV файлы"""
    # Экспорт сотрудников
    employees = Employee.query.all()
    with open(os.path.join(backup_dir, 'employees.csv'), 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'full_name', 'email', 'employee_id', 'hire_date', 'department_id', 'position_id', 'status'])
        for emp in employees:
            writer.writerow([
                emp.id,
                emp.full_name,
                emp.email,
                emp.employee_id,
                emp.hire_date,
                emp.department_id,
                emp.position_id,
                emp.status
            ])
    
    # Экспорт подразделений
    departments = Department.query.all()
    with open(os.path.join(backup_dir, 'departments.csv'), 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'name'])
        for dept in departments:
            writer.writerow([dept.id, dept.name])
    
    # Экспорт должностей
    positions = Position.query.all()
    with open(os.path.join(backup_dir, 'positions.csv'), 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'title'])
        for pos in positions:
            writer.writerow([pos.id, pos.title])
    
    # Экспорт отпусков
    vacations = Vacation.query.all()
    with open(os.path.join(backup_dir, 'vacations.csv'), 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'employee_id', 'start_date', 'end_date', 'type'])
        for vac in vacations:
            writer.writerow([
                vac.id,
                vac.employee_id,
                vac.start_date,
                vac.end_date,
                vac.type
            ])
    
    # Экспорт приказов
    orders = Order.query.all()
    with open(os.path.join(backup_dir, 'orders.csv'), 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'employee_id', 'order_type', 'date_issued', 'details'])
        for order in orders:
            writer.writerow([
                order.id,
                order.employee_id,
                order.order_type,
                order.date_issued,
                order.details
            ])
    
    # Экспорт пользователей
    users = User.query.all()
    with open(os.path.join(backup_dir, 'users.csv'), 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'username', 'email', 'role', 'is_active'])
        for user in users:
            writer.writerow([
                user.id,
                user.username,
                user.email,
                user.role,
                user.is_active
            ])

def restore_from_json(filepath):
    """Восстановление данных из JSON файла (только для администраторов)"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            backup_data = json.load(f)
        
        # Очищаем существующие данные (в обратном порядке из-за внешних ключей)
        Vacation.query.delete()
        Order.query.delete()
        Employee.query.delete()
        Position.query.delete()
        Department.query.delete()
        # User не удаляем, чтобы сохранить администратора
        
        db.session.commit()
        
        # Восстанавливаем подразделения
        for dept_data in backup_data.get('departments', []):
            dept = Department()
            dept.id = dept_data['id']
            dept.name = dept_data['name']
            db.session.add(dept)
        
        # Восстанавливаем должности
        for pos_data in backup_data.get('positions', []):
            pos = Position()
            pos.id = pos_data['id']
            pos.title = pos_data['title']
            db.session.add(pos)
        
        # Восстанавливаем сотрудников
        for emp_data in backup_data.get('employees', []):
            emp = Employee()
            emp.id = emp_data['id']
            emp.full_name = emp_data['full_name']
            emp.email = emp_data['email']
            emp.employee_id = emp_data['employee_id']
            emp.hire_date = datetime.fromisoformat(emp_data['hire_date']).date() if emp_data['hire_date'] else None
            emp.department_id = emp_data['department_id']
            emp.position_id = emp_data['position_id']
            emp.status = emp_data['status']
            db.session.add(emp)
        
        # Восстанавливаем отпуска
        for vac_data in backup_data.get('vacations', []):
            vac = Vacation()
            vac.id = vac_data['id']
            vac.employee_id = vac_data['employee_id']
            vac.start_date = datetime.fromisoformat(vac_data['start_date']).date() if vac_data['start_date'] else None
            vac.end_date = datetime.fromisoformat(vac_data['end_date']).date() if vac_data['end_date'] else None
            vac.type = vac_data['type']
            db.session.add(vac)
        
        # Восстанавливаем приказы
        for order_data in backup_data.get('orders', []):
            order = Order()
            order.id = order_data['id']
            order.employee_id = order_data['employee_id']
            order.type = order_data['type']
            order.date_issued = datetime.fromisoformat(order_data['date_issued']).date() if order_data['date_issued'] else None
            order.new_department_id = order_data['new_department_id']
            order.new_position_id = order_data['new_position_id']
            db.session.add(order)
        
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Ошибка при восстановлении данных: {e}")
        return False

def list_backups(backup_dir='backups'):
    """Получение списка доступных резервных копий"""
    if not os.path.exists(backup_dir):
        return []
    
    backups = []
    for item in os.listdir(backup_dir):
        item_path = os.path.join(backup_dir, item)
        if os.path.isfile(item_path) and item.endswith('.json'):
            stat = os.stat(item_path)
            backups.append({
                'name': item,
                'path': item_path,
                'size': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime)
            })
    
    # Сортируем по дате модификации (новые первыми)
    backups.sort(key=lambda x: x['modified'], reverse=True)
    return backups

def cleanup_old_backups(backup_dir='backups', days_to_keep=30):
    """Удаление старых резервных копий"""
    from datetime import timedelta
    import shutil
    
    if not os.path.exists(backup_dir):
        return 0
    
    cutoff_date = datetime.now() - timedelta(days=days_to_keep)
    deleted_count = 0
    
    for item in os.listdir(backup_dir):
        item_path = os.path.join(backup_dir, item)
        if os.path.isfile(item_path) and item.endswith('.json'):
            stat = os.stat(item_path)
            modified_date = datetime.fromtimestamp(stat.st_mtime)
            if modified_date < cutoff_date:
                # Удаляем JSON файл
                os.remove(item_path)
                deleted_count += 1
                
                # Удаляем соответствующую директорию CSV, если она существует
                csv_dir = item_path.replace('.json', '_csv')
                if os.path.exists(csv_dir) and os.path.isdir(csv_dir):
                    shutil.rmtree(csv_dir)
    
    return deleted_count