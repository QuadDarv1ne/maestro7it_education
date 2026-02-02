from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from app import db
from app.models import User, TestResult, CareerGoal, LearningPath, CalendarEvent
from datetime import datetime, timedelta
import json

calendar_bp = Blueprint('calendar', __name__)


@calendar_bp.route('/calendar')
@login_required
def calendar_page():
    # Страница календаря для планирования карьерного развития
    return render_template('calendar/index.html')


@calendar_bp.route('/api/calendar/events')
@login_required
def get_calendar_events():
    # Получение событий календаря для пользователя
    start = request.args.get('start')
    end = request.args.get('end')
    
    events = CalendarEvent.query.filter_by(user_id=current_user.id)
    
    if start:
        start_date = datetime.fromisoformat(start)
        events = events.filter(CalendarEvent.start_datetime >= start_date)
    
    if end:
        end_date = datetime.fromisoformat(end)
        events = events.filter(CalendarEvent.start_datetime <= end_date)
    
    events_list = []
    for event in events.all():
        events_list.append({
            'id': event.id,
            'title': event.title,
            'description': event.description,
            'start': event.start_datetime.isoformat(),
            'end': event.end_datetime.isoformat() if event.end_datetime else None,
            'eventType': event.event_type,
            'location': event.location,
            'isRecurring': event.is_recurring,
            'reminderMinutes': event.reminder_minutes
        })
    
    return jsonify(events_list)


@calendar_bp.route('/api/calendar/events', methods=['POST'])
@login_required
def create_calendar_event():
    # Создание нового события календаря
    data = request.get_json()
    
    title = data.get('title', '')
    description = data.get('description', '')
    event_type = data.get('eventType', 'event')
    start_datetime_str = data.get('start')
    end_datetime_str = data.get('end')
    location = data.get('location', '')
    is_recurring = data.get('isRecurring', False)
    recurrence_pattern = data.get('recurrencePattern')
    reminder_minutes = data.get('reminderMinutes', 15)
    
    if not title or not start_datetime_str:
        return jsonify({'error': 'Title and start datetime are required'}), 400
    
    try:
        start_datetime = datetime.fromisoformat(start_datetime_str)
        end_datetime = datetime.fromisoformat(end_datetime_str) if end_datetime_str else None
    except ValueError:
        return jsonify({'error': 'Invalid datetime format'}), 400
    
    event = CalendarEvent(
        user_id=current_user.id,
        title=title,
        description=description,
        event_type=event_type,
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        location=location,
        is_recurring=is_recurring,
        recurrence_pattern=recurrence_pattern,
        reminder_minutes=reminder_minutes
    )
    
    db.session.add(event)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Событие успешно создано',
        'eventId': event.id
    })


@calendar_bp.route('/api/calendar/events/<int:event_id>', methods=['PUT', 'DELETE'])
@login_required
def manage_calendar_event(event_id):
    # Редактирование или удаление события календаря
    event = CalendarEvent.query.filter_by(id=event_id, user_id=current_user.id).first_or_404()
    
    if request.method == 'PUT':
        data = request.get_json()
        
        event.title = data.get('title', event.title)
        event.description = data.get('description', event.description)
        event.event_type = data.get('eventType', event.event_type)
        
        if data.get('start'):
            try:
                event.start_datetime = datetime.fromisoformat(data.get('start'))
            except ValueError:
                return jsonify({'error': 'Invalid start datetime format'}), 400
        
        if data.get('end'):
            try:
                event.end_datetime = datetime.fromisoformat(data.get('end'))
            except ValueError:
                return jsonify({'error': 'Invalid end datetime format'}), 400
        elif data.get('end') is None:
            event.end_datetime = None
        
        event.location = data.get('location', event.location)
        event.is_recurring = data.get('isRecurring', event.is_recurring)
        event.recurrence_pattern = data.get('recurrencePattern', event.recurrence_pattern)
        event.reminder_minutes = data.get('reminderMinutes', event.reminder_minutes)
        
        event.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Событие успешно обновлено'
        })
    
    elif request.method == 'DELETE':
        db.session.delete(event)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Событие успешно удалено'
        })


@calendar_bp.route('/api/career-goals')
@login_required
def get_career_goals():
    # Получение карьерных целей пользователя
    goals = CareerGoal.query.filter_by(user_id=current_user.id).order_by(
        CareerGoal.priority.desc(), 
        CareerGoal.created_at.desc()
    ).all()
    
    goals_list = []
    for goal in goals:
        goals_list.append({
            'id': goal.id,
            'title': goal.title,
            'description': goal.description,
            'targetDate': goal.target_date.isoformat() if goal.target_date else None,
            'currentStatus': goal.current_status,
            'priority': goal.priority,
            'createdAt': goal.created_at.isoformat()
        })
    
    return jsonify(goals_list)


@calendar_bp.route('/api/career-goals', methods=['POST'])
@login_required
def create_career_goal():
    # Создание новой карьерной цели
    data = request.get_json()
    
    title = data.get('title', '')
    description = data.get('description', '')
    target_date_str = data.get('targetDate')
    priority = data.get('priority', 3)
    
    if not title:
        return jsonify({'error': 'Title is required'}), 400
    
    target_date = None
    if target_date_str:
        try:
            target_date = datetime.fromisoformat(target_date_str).date()
        except ValueError:
            return jsonify({'error': 'Invalid date format'}), 400
    
    # Validate priority
    if priority < 1 or priority > 5:
        return jsonify({'error': 'Priority must be between 1 and 5'}), 400
    
    goal = CareerGoal(
        user_id=current_user.id,
        title=title,
        description=description,
        target_date=target_date,
        priority=priority
    )
    
    db.session.add(goal)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Цель успешно создана',
        'goalId': goal.id
    })


@calendar_bp.route('/api/career-goals/<int:goal_id>', methods=['PUT', 'DELETE'])
@login_required
def manage_career_goal(goal_id):
    # Редактирование или удаление карьерной цели
    goal = CareerGoal.query.filter_by(id=goal_id, user_id=current_user.id).first_or_404()
    
    if request.method == 'PUT':
        data = request.get_json()
        
        goal.title = data.get('title', goal.title)
        goal.description = data.get('description', goal.description)
        
        if data.get('targetDate'):
            try:
                goal.target_date = datetime.fromisoformat(data.get('targetDate')).date()
            except ValueError:
                return jsonify({'error': 'Invalid date format'}), 400
        elif data.get('targetDate') is None:
            goal.target_date = None
        
        if 'currentStatus' in data:
            goal.current_status = data['currentStatus']
        
        if 'priority' in data:
            priority = data['priority']
            if priority < 1 or priority > 5:
                return jsonify({'error': 'Priority must be between 1 and 5'}), 400
            goal.priority = priority
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Цель успешно обновлена'
        })
    
    elif request.method == 'DELETE':
        db.session.delete(goal)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Цель успешно удалена'
        })


@calendar_bp.route('/api/learning-paths')
@login_required
def get_learning_paths():
    # Получение образовательных траекторий пользователя
    goal_id = request.args.get('goalId')
    
    paths = LearningPath.query.filter_by(user_id=current_user.id)
    if goal_id:
        paths = paths.filter_by(goal_id=goal_id)
    
    paths_list = []
    for path in paths.all():
        paths_list.append({
            'id': path.id,
            'title': path.title,
            'description': path.description,
            'durationWeeks': path.duration_weeks,
            'difficultyLevel': path.difficulty_level,
            'status': path.status,
            'createdAt': path.created_at.isoformat(),
            'completedAt': path.completed_at.isoformat() if path.completed_at else None,
            'goalId': path.goal_id
        })
    
    return jsonify(paths_list)


@calendar_bp.route('/api/learning-paths', methods=['POST'])
@login_required
def create_learning_path():
    # Создание новой образовательной траектории
    data = request.get_json()
    
    title = data.get('title', '')
    description = data.get('description', '')
    goal_id = data.get('goalId')
    duration_weeks = data.get('durationWeeks', 4)
    difficulty_level = data.get('difficultyLevel', 'beginner')
    
    if not title:
        return jsonify({'error': 'Title is required'}), 400
    
    # Validate difficulty level
    valid_levels = ['beginner', 'intermediate', 'advanced']
    if difficulty_level not in valid_levels:
        return jsonify({'error': f'Difficulty level must be one of: {", ".join(valid_levels)}'}), 400
    
    # Validate goal exists if provided
    if goal_id:
        goal = CareerGoal.query.filter_by(id=goal_id, user_id=current_user.id).first()
        if not goal:
            return jsonify({'error': 'Invalid goal ID'}), 400
    
    path = LearningPath(
        user_id=current_user.id,
        title=title,
        description=description,
        goal_id=goal_id,
        duration_weeks=duration_weeks,
        difficulty_level=difficulty_level
    )
    
    db.session.add(path)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Образовательная траектория успешно создана',
        'pathId': path.id
    })


@calendar_bp.route('/api/learning-paths/<int:path_id>', methods=['PUT', 'DELETE'])
@login_required
def manage_learning_path(path_id):
    # Редактирование или удаление образовательной траектории
    path = LearningPath.query.filter_by(id=path_id, user_id=current_user.id).first_or_404()
    
    if request.method == 'PUT':
        data = request.get_json()
        
        path.title = data.get('title', path.title)
        path.description = data.get('description', path.description)
        path.duration_weeks = data.get('durationWeeks', path.duration_weeks)
        
        if 'difficultyLevel' in data:
            valid_levels = ['beginner', 'intermediate', 'advanced']
            difficulty_level = data['difficultyLevel']
            if difficulty_level not in valid_levels:
                return jsonify({'error': f'Difficulty level must be one of: {", ".join(valid_levels)}'}), 400
            path.difficulty_level = difficulty_level
        
        if 'status' in data:
            valid_statuses = ['not_started', 'in_progress', 'completed']
            status = data['status']
            if status not in valid_statuses:
                return jsonify({'error': f'Status must be one of: {", ".join(valid_statuses)}'}), 400
            path.status = status
            
            # Update completed_at if status changes to completed
            if status == 'completed' and not path.completed_at:
                path.completed_at = datetime.utcnow()
            elif status != 'completed':
                path.completed_at = None
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Образовательная траектория успешно обновлена'
        })
    
    elif request.method == 'DELETE':
        db.session.delete(path)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Образовательная траектория успешно удалена'
        })


@calendar_bp.route('/api/calendar/schedule-learning')
@login_required
def schedule_learning_sessions():
    # Автоматическое планирование сессий обучения на основе образовательных траекторий
    # Находит все активные образовательные траектории и создает события в календаре
    
    learning_paths = LearningPath.query.filter_by(
        user_id=current_user.id,
        status='in_progress'
    ).all()
    
    scheduled_events = []
    
    for path in learning_paths:
        # Для упрощения, создаем одно событие на начало траектории
        # В реальном приложении это будет более сложный алгоритм
        start_date = datetime.utcnow() + timedelta(days=1)  # Начать завтра
        
        event = CalendarEvent(
            user_id=current_user.id,
            title=f"Обучение: {path.title}",
            description=f"Начало образовательной траектории: {path.description}",
            event_type='learning_session',
            start_datetime=start_date,
            end_datetime=start_date + timedelta(hours=2),  # 2-часовая сессия
            location='Онлайн',
            reminder_minutes=30
        )
        
        db.session.add(event)
        scheduled_events.append({
            'pathId': path.id,
            'eventId': event.id,
            'title': event.title,
            'date': event.start_datetime.isoformat()
        })
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'scheduledEvents': scheduled_events,
        'count': len(scheduled_events)
    })