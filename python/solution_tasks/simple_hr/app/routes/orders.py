from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import Order, Employee, Department, Position
from app import db
from datetime import datetime

bp = Blueprint('orders', __name__)

@bp.route('/')
@login_required
def list_orders():
    orders = Order.query.all()
    return render_template('orders/list.html', orders=orders)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_order():
    if request.method == 'POST':
        employee_id = request.form['employee_id']
        order_type = request.form['type']
        date_issued = request.form['date_issued']
        new_department_id = request.form.get('new_department_id')
        new_position_id = request.form.get('new_position_id')
        
        # Create new order
        order = Order(
            employee_id=employee_id,
            type=order_type,
            date_issued=datetime.strptime(date_issued, '%Y-%m-%d').date(),
            new_department_id=new_department_id if new_department_id else None,
            new_position_id=new_position_id if new_position_id else None
        )
        
        try:
            db.session.add(order)
            db.session.commit()
            flash('Приказ успешно создан')
            return redirect(url_for('orders.list_orders'))
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при создании приказа')
            return redirect(url_for('orders.create_order'))
    
    employees = Employee.query.all()
    departments = Department.query.all()
    positions = Position.query.all()
    return render_template('orders/form.html', employees=employees, departments=departments, positions=positions)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_order(id):
    order = Order.query.get_or_404(id)
    
    if request.method == 'POST':
        order.employee_id = request.form['employee_id']
        order.type = request.form['type']
        order.date_issued = datetime.strptime(request.form['date_issued'], '%Y-%m-%d').date()
        order.new_department_id = request.form.get('new_department_id')
        order.new_position_id = request.form.get('new_position_id')
        
        try:
            db.session.commit()
            flash('Приказ успешно обновлен')
            return redirect(url_for('orders.list_orders'))
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при обновлении приказа')
            return redirect(url_for('orders.edit_order', id=id))
    
    employees = Employee.query.all()
    departments = Department.query.all()
    positions = Position.query.all()
    return render_template('orders/form.html', order=order, employees=employees, departments=departments, positions=positions)

@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_order(id):
    order = Order.query.get_or_404(id)
    
    try:
        db.session.delete(order)
        db.session.commit()
        flash('Приказ успешно удален')
    except Exception as e:
        db.session.rollback()
        flash('Ошибка при удалении приказа')
    
    return redirect(url_for('orders.list_orders'))