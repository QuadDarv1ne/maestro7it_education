from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import Order, Employee, Department, Position
from app.forms import OrderForm
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
    form = OrderForm()
    if form.validate_on_submit():
        # Create new order
        order = Order(
            employee_id=form.employee_id.data,
            type=form.type.data,
            date_issued=form.date_issued.data,
            new_department_id=form.new_department_id.data if form.new_department_id.data else None,
            new_position_id=form.new_position_id.data if form.new_position_id.data else None
        )
        
        try:
            db.session.add(order)
            db.session.commit()
            flash('Приказ успешно создан')
            return redirect(url_for('orders.list_orders'))
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при создании приказа')
            return render_template('orders/form.html', form=form)
    
    return render_template('orders/form.html', form=form)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_order(id):
    order = Order.query.get_or_404(id)
    form = OrderForm(obj=order)
    
    if form.validate_on_submit():
        order.employee_id = form.employee_id.data
        order.type = form.type.data
        order.date_issued = form.date_issued.data
        order.new_department_id = form.new_department_id.data if form.new_department_id.data else None
        order.new_position_id = form.new_position_id.data if form.new_position_id.data else None
        
        try:
            db.session.commit()
            flash('Приказ успешно обновлен')
            return redirect(url_for('orders.list_orders'))
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при обновлении приказа')
            return render_template('orders/form.html', form=form, order=order)
    
    return render_template('orders/form.html', form=form, order=order)

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