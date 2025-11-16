"""
Утилиты для экспорта данных в различные форматы
"""
import csv
import io
from datetime import datetime
from flask import Response


def export_employees_to_csv(employees):
    """Экспорт списка сотрудников в CSV"""
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Заголовки
    writer.writerow([
        'ID',
        'ФИО',
        'Email',
        'Табельный номер',
        'Дата найма',
        'Статус',
        'Отдел',
        'Должность'
    ])
    
    # Данные
    for emp in employees:
        writer.writerow([
            emp.id,
            emp.full_name,
            emp.email,
            emp.employee_id,
            emp.hire_date.strftime('%Y-%m-%d') if emp.hire_date else '',
            emp.status,
            emp.department.name if emp.department else '',
            emp.position.title if emp.position else ''
        ])
    
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={
            'Content-Disposition': f'attachment; filename=employees_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        }
    )


def export_vacations_to_csv(vacations):
    """Экспорт отпусков в CSV"""
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Заголовки
    writer.writerow([
        'ID',
        'Сотрудник',
        'Дата начала',
        'Дата окончания',
        'Тип',
        'Длительность (дней)'
    ])
    
    # Данные
    for vac in vacations:
        duration = (vac.end_date - vac.start_date).days + 1
        writer.writerow([
            vac.id,
            vac.employee.full_name if vac.employee else '',
            vac.start_date.strftime('%Y-%m-%d') if vac.start_date else '',
            vac.end_date.strftime('%Y-%m-%d') if vac.end_date else '',
            vac.type,
            duration
        ])
    
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={
            'Content-Disposition': f'attachment; filename=vacations_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        }
    )


def export_orders_to_csv(orders):
    """Экспорт приказов в CSV"""
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Заголовки
    writer.writerow([
        'ID',
        'Сотрудник',
        'Тип',
        'Дата',
        'Новый отдел',
        'Новая должность'
    ])
    
    # Данные
    for order in orders:
        writer.writerow([
            order.id,
            order.employee.full_name if order.employee else '',
            order.type,
            order.date_issued.strftime('%Y-%m-%d') if order.date_issued else '',
            order.new_department.name if order.new_department else '',
            order.new_position.title if order.new_position else ''
        ])
    
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={
            'Content-Disposition': f'attachment; filename=orders_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        }
    )


def export_departments_to_csv(departments):
    """Экспорт отделов в CSV"""
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Заголовки
    writer.writerow([
        'ID',
        'Название',
        'Количество сотрудников'
    ])
    
    # Данные
    for dept in departments:
        writer.writerow([
            dept.id,
            dept.name,
            len(dept.employees) if dept.employees else 0
        ])
    
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={
            'Content-Disposition': f'attachment; filename=departments_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        }
    )
