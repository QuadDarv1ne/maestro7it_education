#!/usr/bin/env python
"""
Скрипт для наполнения базы тестовыми данными
"""

import sys
import os
from datetime import date, timedelta

# Добавляем путь к приложению
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Employee, Department, Position, Vacation, Order

def create_test_data():
    """Создание тестовых данных"""
    app = create_app()
    
    with app.app_context():
        # Создаем таблицы, если их нет
        db.create_all()
        
        # Проверяем, есть ли уже данные
        if User.query.first():
            print("Тестовые данные уже существуют в базе")
            return
        
        # Создаем пользователей
        admin = User(username='admin', email='admin@example.com', role='admin')
        admin.set_password('admin123')
        
        hr_user = User(username='hr', email='hr@example.com', role='hr')
        hr_user.set_password('hr123')
        
        db.session.add(admin)
        db.session.add(hr_user)
        
        # Создаем подразделения (3-5)
        departments_data = [
            'IT',
            'HR',
            'Finance',
            'Marketing',
            'Operations'
        ]
        
        departments = []
        for dept_name in departments_data:
            dept = Department(name=dept_name)
            db.session.add(dept)
            departments.append(dept)
        
        # Создаем должности (5-7)
        positions_data = [
            'Developer',
            'HR Manager',
            'Accountant',
            'Marketing Specialist',
            'Operations Manager',
            'Team Lead',
            'Director'
        ]
        
        positions = []
        for pos_title in positions_data:
            pos = Position(title=pos_title)
            db.session.add(pos)
            positions.append(pos)
        
        # Создаем сотрудников (30+)
        employees_data = [
            # IT department
            {'full_name': 'Иванов Иван Иванович', 'email': 'ivanov@example.com', 'employee_id': 'ID0001', 'hire_date': date(2023, 1, 15), 'department': departments[0], 'position': positions[0]},
            {'full_name': 'Петров Петр Петрович', 'email': 'petrov@example.com', 'employee_id': 'ID0002', 'hire_date': date(2023, 2, 20), 'department': departments[0], 'position': positions[5]},
            {'full_name': 'Сидоров Сидор Сидорович', 'email': 'sidorov@example.com', 'employee_id': 'ID0003', 'hire_date': date(2023, 3, 10), 'department': departments[0], 'position': positions[0]},
            {'full_name': 'Козлов Алексей Владимирович', 'email': 'kozlov@example.com', 'employee_id': 'ID0004', 'hire_date': date(2023, 4, 5), 'department': departments[0], 'position': positions[5]},
            {'full_name': 'Морозова Анна Сергеевна', 'email': 'morozova@example.com', 'employee_id': 'ID0005', 'hire_date': date(2023, 5, 12), 'department': departments[0], 'position': positions[0]},
            {'full_name': 'Новиков Дмитрий Александрович', 'email': 'novikov@example.com', 'employee_id': 'ID0006', 'hire_date': date(2023, 6, 18), 'department': departments[0], 'position': positions[0]},
            
            # HR department
            {'full_name': 'Кузнецова Елена Петровна', 'email': 'kuznetsova@example.com', 'employee_id': 'ID0007', 'hire_date': date(2023, 7, 22), 'department': departments[1], 'position': positions[1]},
            {'full_name': 'Васильев Михаил Игоревич', 'email': 'vasiliev@example.com', 'employee_id': 'ID0008', 'hire_date': date(2023, 8, 30), 'department': departments[1], 'position': positions[1]},
            
            # Finance department
            {'full_name': 'Попова Ольга Дмитриевна', 'email': 'popova@example.com', 'employee_id': 'ID0009', 'hire_date': date(2023, 9, 15), 'department': departments[2], 'position': positions[2]},
            {'full_name': 'Лебедев Артем Викторович', 'email': 'lebedev@example.com', 'employee_id': 'ID0010', 'hire_date': date(2023, 10, 20), 'department': departments[2], 'position': positions[2]},
            {'full_name': 'Соколова Мария Андреевна', 'email': 'sokolova@example.com', 'employee_id': 'ID0011', 'hire_date': date(2023, 11, 5), 'department': departments[2], 'position': positions[2]},
            
            # Marketing department
            {'full_name': 'Михайлов Владимир Николаевич', 'email': 'mikhailov@example.com', 'employee_id': 'ID0012', 'hire_date': date(2023, 12, 10), 'department': departments[3], 'position': positions[3]},
            {'full_name': 'Новикова Екатерина Александровна', 'email': 'novikova@example.com', 'employee_id': 'ID0013', 'hire_date': date(2024, 1, 15), 'department': departments[3], 'position': positions[3]},
            {'full_name': 'Федоров Сергей Владимирович', 'email': 'fedorov@example.com', 'employee_id': 'ID0014', 'hire_date': date(2024, 2, 20), 'department': departments[3], 'position': positions[3]},
            {'full_name': 'Ковалева Анастасия Павловна', 'email': 'kotova@example.com', 'employee_id': 'ID0015', 'hire_date': date(2024, 3, 25), 'department': departments[3], 'position': positions[3]},
            
            # Operations department
            {'full_name': 'Волков Андрей Сергеевич', 'email': 'volkov@example.com', 'employee_id': 'ID0016', 'hire_date': date(2024, 4, 30), 'department': departments[4], 'position': positions[4]},
            {'full_name': 'Алексеева Татьяна Михайловна', 'email': 'alekseeva@example.com', 'employee_id': 'ID0017', 'hire_date': date(2024, 5, 5), 'department': departments[4], 'position': positions[4]},
            
            # Дополнительные сотрудники для достижения 30+
            {'full_name': 'Григорьев Дмитрий Викторович', 'email': 'grigoriev@example.com', 'employee_id': 'ID0018', 'hire_date': date(2024, 1, 10), 'department': departments[0], 'position': positions[0]},
            {'full_name': 'Крылова Оксана Сергеевна', 'email': 'krylova@example.com', 'employee_id': 'ID0019', 'hire_date': date(2024, 2, 15), 'department': departments[0], 'position': positions[0]},
            {'full_name': 'Белов Роман Андреевич', 'email': 'belov@example.com', 'employee_id': 'ID0020', 'hire_date': date(2024, 3, 20), 'department': departments[0], 'position': positions[0]},
            {'full_name': 'Жукова Ирина Валерьевна', 'email': 'zhukova@example.com', 'employee_id': 'ID0021', 'hire_date': date(2024, 4, 25), 'department': departments[0], 'position': positions[0]},
            {'full_name': 'Карпов Алексей Петрович', 'email': 'karpov@example.com', 'employee_id': 'ID0022', 'hire_date': date(2024, 5, 30), 'department': departments[0], 'position': positions[0]},
            {'full_name': 'Макарова Елена Дмитриевна', 'email': 'makarova@example.com', 'employee_id': 'ID0023', 'hire_date': date(2024, 6, 5), 'department': departments[1], 'position': positions[1]},
            {'full_name': 'Андреев Михаил Александрович', 'email': 'andreev@example.com', 'employee_id': 'ID0024', 'hire_date': date(2024, 7, 10), 'department': departments[2], 'position': positions[2]},
            {'full_name': 'Сорокина Анна Викторовна', 'email': 'sorokina@example.com', 'employee_id': 'ID0025', 'hire_date': date(2024, 8, 15), 'department': departments[2], 'position': positions[2]},
            {'full_name': 'Беляев Сергей Николаевич', 'email': 'belyaev@example.com', 'employee_id': 'ID0026', 'hire_date': date(2024, 9, 20), 'department': departments[3], 'position': positions[3]},
            {'full_name': 'Козлова Мария Андреевна', 'email': 'kozlova@example.com', 'employee_id': 'ID0027', 'hire_date': date(2024, 10, 25), 'department': departments[3], 'position': positions[3]},
            {'full_name': 'Лебедева Татьяна Сергеевна', 'email': 'lebedeva@example.com', 'employee_id': 'ID0028', 'hire_date': date(2024, 11, 30), 'department': departments[4], 'position': positions[4]},
            {'full_name': 'Смирнов Владимир Петрович', 'email': 'smirnov@example.com', 'employee_id': 'ID0029', 'hire_date': date(2024, 12, 5), 'department': departments[4], 'position': positions[4]},
            {'full_name': 'Иванова Ольга Александровна', 'email': 'ivanova@example.com', 'employee_id': 'ID0030', 'hire_date': date(2025, 1, 10), 'department': departments[0], 'position': positions[0]},
            {'full_name': 'Кузнецов Павел Михайлович', 'email': 'kuznetsov@example.com', 'employee_id': 'ID0031', 'hire_date': date(2025, 2, 15), 'department': departments[1], 'position': positions[1]},
            {'full_name': 'Попов Александр Сергеевич', 'email': 'popov@example.com', 'employee_id': 'ID0032', 'hire_date': date(2025, 3, 20), 'department': departments[2], 'position': positions[2]},
        ]
        
        employees = []
        for emp_data in employees_data:
            emp = Employee(
                full_name=emp_data['full_name'],
                email=emp_data['email'],
                employee_id=emp_data['employee_id'],
                hire_date=emp_data['hire_date'],
                department=emp_data['department'],
                position=emp_data['position'],
                status='active'
            )
            db.session.add(emp)
            employees.append(emp)
        
        # Создаем отпуска (10+)
        vacations_data = [
            {'employee': employees[0], 'start_date': date(2025, 6, 1), 'end_date': date(2025, 6, 14), 'type': 'paid'},
            {'employee': employees[1], 'start_date': date(2025, 7, 15), 'end_date': date(2025, 7, 28), 'type': 'paid'},
            {'employee': employees[2], 'start_date': date(2025, 8, 5), 'end_date': date(2025, 8, 18), 'type': 'paid'},
            {'employee': employees[3], 'start_date': date(2025, 9, 10), 'end_date': date(2025, 9, 23), 'type': 'paid'},
            {'employee': employees[4], 'start_date': date(2025, 10, 1), 'end_date': date(2025, 10, 14), 'type': 'paid'},
            {'employee': employees[5], 'start_date': date(2025, 11, 5), 'end_date': date(2025, 11, 18), 'type': 'paid'},
            {'employee': employees[6], 'start_date': date(2025, 12, 1), 'end_date': date(2025, 12, 14), 'type': 'paid'},
            {'employee': employees[7], 'start_date': date(2025, 6, 20), 'end_date': date(2025, 6, 25), 'type': 'sick'},
            {'employee': employees[8], 'start_date': date(2025, 7, 10), 'end_date': date(2025, 7, 15), 'type': 'unpaid'},
            {'employee': employees[9], 'start_date': date(2025, 8, 15), 'end_date': date(2025, 8, 20), 'type': 'sick'},
            {'employee': employees[10], 'start_date': date(2025, 9, 5), 'end_date': date(2025, 9, 10), 'type': 'paid'},
            {'employee': employees[11], 'start_date': date(2025, 10, 20), 'end_date': date(2025, 10, 25), 'type': 'paid'},
        ]
        
        for vac_data in vacations_data:
            vac = Vacation(
                employee=vac_data['employee'],
                start_date=vac_data['start_date'],
                end_date=vac_data['end_date'],
                type=vac_data['type']
            )
            db.session.add(vac)
        
        # Создаем приказы (10+)
        orders_data = [
            # Приказы о приеме
            {'employee': employees[0], 'type': 'hire', 'date_issued': date(2023, 1, 10)},
            {'employee': employees[1], 'type': 'hire', 'date_issued': date(2023, 2, 15)},
            {'employee': employees[2], 'type': 'hire', 'date_issued': date(2023, 3, 5)},
            {'employee': employees[3], 'type': 'hire', 'date_issued': date(2023, 4, 1)},
            {'employee': employees[4], 'type': 'hire', 'date_issued': date(2023, 5, 7)},
            {'employee': employees[5], 'type': 'hire', 'date_issued': date(2023, 6, 13)},
            {'employee': employees[6], 'type': 'hire', 'date_issued': date(2023, 7, 17)},
            {'employee': employees[7], 'type': 'hire', 'date_issued': date(2023, 8, 25)},
            
            # Приказы о переводе
            {'employee': employees[0], 'type': 'transfer', 'date_issued': date(2024, 1, 15), 'new_department': departments[0], 'new_position': positions[5]},
            {'employee': employees[1], 'type': 'transfer', 'date_issued': date(2024, 2, 20), 'new_department': departments[0], 'new_position': positions[5]},
            
            # Приказы об увольнении (для тестирования отчета по обороту)
            {'employee': employees[12], 'type': 'hire', 'date_issued': date(2023, 12, 5)},
            {'employee': employees[12], 'type': 'dismissal', 'date_issued': date(2025, 1, 15)},
            {'employee': employees[13], 'type': 'hire', 'date_issued': date(2024, 1, 10)},
            {'employee': employees[13], 'type': 'dismissal', 'date_issued': date(2025, 2, 20)},
        ]
        
        for order_data in orders_data:
            order = Order(
                employee=order_data['employee'],
                type=order_data['type'],
                date_issued=order_data['date_issued']
            )
            
            # Если это перевод, добавляем новое подразделение и должность
            if 'new_department' in order_data:
                order.new_department = order_data['new_department']
            if 'new_position' in order_data:
                order.new_position = order_data['new_position']
                
            db.session.add(order)
        
        # Сохраняем все изменения
        db.session.commit()
        print("Тестовые данные успешно созданы!")
        print(f"Создано пользователей: 2")
        print(f"Создано подразделений: {len(departments)}")
        print(f"Создано должностей: {len(positions)}")
        print(f"Создано сотрудников: {len(employees)}")
        print(f"Создано отпусков: {len(vacations_data)}")
        print(f"Создано приказов: {len(orders_data)}")

if __name__ == '__main__':
    create_test_data()