from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import Position
from app import db

bp = Blueprint('positions', __name__)

@bp.route('/')
@login_required
def list_positions():
    positions = Position.query.all()
    return render_template('positions/list.html', positions=positions)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_position():
    if request.method == 'POST':
        title = request.form['title']
        
        # Check if position already exists
        existing_pos = Position.query.filter_by(title=title).first()
        if existing_pos:
            flash('Должность с таким названием уже существует')
            return redirect(url_for('positions.create_position'))
        
        # Create new position
        position = Position(title=title)
        
        try:
            db.session.add(position)
            db.session.commit()
            flash('Должность успешно добавлена')
            return redirect(url_for('positions.list_positions'))
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при добавлении должности')
            return redirect(url_for('positions.create_position'))
    
    return render_template('positions/form.html')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_position(id):
    position = Position.query.get_or_404(id)
    
    if request.method == 'POST':
        title = request.form['title']
        
        # Check if another position with the same title exists
        existing_pos = Position.query.filter_by(title=title).first()
        if existing_pos and existing_pos.id != id:
            flash('Должность с таким названием уже существует')
            return redirect(url_for('positions.edit_position', id=id))
        
        position.title = title
        
        try:
            db.session.commit()
            flash('Должность успешно обновлена')
            return redirect(url_for('positions.list_positions'))
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при обновлении должности')
            return redirect(url_for('positions.edit_position', id=id))
    
    return render_template('positions/form.html', position=position)

@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_position(id):
    position = Position.query.get_or_404(id)
    
    # Check if position has employees
    if position.employees:
        flash('Невозможно удалить должность, так как на ней есть сотрудники')
        return redirect(url_for('positions.list_positions'))
    
    try:
        db.session.delete(position)
        db.session.commit()
        flash('Должность успешно удалена')
    except Exception as e:
        db.session.rollback()
        flash('Ошибка при удалении должности')
    
    return redirect(url_for('positions.list_positions'))