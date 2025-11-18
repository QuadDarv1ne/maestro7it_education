"""
WebSocket support for real-time notifications
"""
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_login import current_user
from functools import wraps

socketio = SocketIO(cors_allowed_origins="*", async_mode='threading')

def authenticated_only(f):
    """Decorator to ensure user is authenticated for SocketIO events"""
    @wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            emit('error', {'message': 'Authentication required'})
            return
        return f(*args, **kwargs)
    return wrapped

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    if current_user.is_authenticated:
        # Подключаем пользователя к его персональной комнате
        join_room(f'user_{current_user.id}')
        # Подключаем к общей комнате в зависимости от роли
        if current_user.is_admin():
            join_room('admin')
        elif current_user.is_hr():
            join_room('hr')
        
        emit('connected', {
            'message': 'Successfully connected to notification service',
            'user_id': current_user.id
        })

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    if current_user.is_authenticated:
        leave_room(f'user_{current_user.id}')
        if current_user.is_admin():
            leave_room('admin')
        elif current_user.is_hr():
            leave_room('hr')

@socketio.on('join_department')
@authenticated_only
def handle_join_department(data):
    """Allow user to join department-specific room"""
    department_id = data.get('department_id')
    if department_id:
        join_room(f'department_{department_id}')
        emit('joined', {'department_id': department_id})

@socketio.on('leave_department')
@authenticated_only
def handle_leave_department(data):
    """Allow user to leave department-specific room"""
    department_id = data.get('department_id')
    if department_id:
        leave_room(f'department_{department_id}')
        emit('left', {'department_id': department_id})

def send_notification(user_id, notification_type, message, data=None):
    """
    Send real-time notification to specific user
    
    Args:
        user_id: Target user ID
        notification_type: Type of notification (info, warning, error, success)
        message: Notification message
        data: Additional data (optional)
    """
    socketio.emit('notification', {
        'type': notification_type,
        'message': message,
        'data': data or {},
        'timestamp': __import__('datetime').datetime.utcnow().isoformat()
    }, room=f'user_{user_id}')

def broadcast_to_role(role, notification_type, message, data=None):
    """
    Broadcast notification to all users with specific role
    
    Args:
        role: Target role (admin, hr)
        notification_type: Type of notification
        message: Notification message
        data: Additional data (optional)
    """
    socketio.emit('notification', {
        'type': notification_type,
        'message': message,
        'data': data or {},
        'timestamp': __import__('datetime').datetime.utcnow().isoformat()
    }, room=role)

def broadcast_to_department(department_id, notification_type, message, data=None):
    """
    Broadcast notification to all users in specific department
    
    Args:
        department_id: Target department ID
        notification_type: Type of notification
        message: Notification message
        data: Additional data (optional)
    """
    socketio.emit('notification', {
        'type': notification_type,
        'message': message,
        'data': data or {},
        'timestamp': __import__('datetime').datetime.utcnow().isoformat()
    }, room=f'department_{department_id}')

def notify_vacation_request(employee_name, department_id):
    """Notify HR/admin about new vacation request"""
    broadcast_to_role('hr', 'info', 
                     f'Новая заявка на отпуск от {employee_name}',
                     {'type': 'vacation_request', 'employee': employee_name})
    broadcast_to_role('admin', 'info',
                     f'Новая заявка на отпуск от {employee_name}',
                     {'type': 'vacation_request', 'employee': employee_name})

def notify_vacation_approved(user_id, start_date, end_date):
    """Notify employee about approved vacation"""
    send_notification(user_id, 'success',
                     f'Ваш отпуск с {start_date} по {end_date} одобрен',
                     {'type': 'vacation_approved'})

def notify_vacation_rejected(user_id, reason):
    """Notify employee about rejected vacation"""
    send_notification(user_id, 'warning',
                     f'Ваша заявка на отпуск отклонена. Причина: {reason}',
                     {'type': 'vacation_rejected'})

def notify_new_employee(department_id, employee_name):
    """Notify department about new employee"""
    broadcast_to_department(department_id, 'info',
                          f'Новый сотрудник: {employee_name}',
                          {'type': 'new_employee', 'employee': employee_name})
