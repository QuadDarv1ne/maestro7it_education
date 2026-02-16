"""
WebSocket handlers for real-time notifications
"""
from flask_socketio import SocketIO, emit, join_room, leave_room
from app.utils.notifications import broadcast_notification, send_realtime_notification
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Initialize SocketIO without app (will be init_app later)
socketio = SocketIO(cors_allowed_origins="*")

def init_websocket_handlers(app):
    """Initialize websocket handlers with the Flask app"""
    socketio.init_app(app, cors_allowed_origins="*")
    
    return socketio

# Event handlers
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    logger.info('Client connected to WebSocket')
    emit('status', {'msg': 'Connected to notification server'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    logger.info('Client disconnected from WebSocket')

@socketio.on('join')
def on_join(data):
    """Handle joining a room"""
    username = data.get('username', 'anonymous')
    room = data.get('room', 'general')
    join_room(room)
    emit('status', {'msg': f'{username} has entered the room {room}'})

@socketio.on('leave')
def on_leave(data):
    """Handle leaving a room"""
    username = data.get('username', 'anonymous')
    room = data.get('room', 'general')
    leave_room(room)
    emit('status', {'msg': f'{username} has left the room {room}'})

@socketio.on('subscribe_to_tournament')
def handle_subscribe_tournament(data):
    """Subscribe to tournament-specific notifications"""
    tournament_id = data.get('tournament_id')
    if tournament_id:
        room = f'tournament_{tournament_id}'
        join_room(room)
        emit('status', {'msg': f'Subscribed to tournament {tournament_id} notifications'})

@socketio.on('unsubscribe_from_tournament')
def handle_unsubscribe_tournament(data):
    """Unsubscribe from tournament-specific notifications"""
    tournament_id = data.get('tournament_id')
    if tournament_id:
        room = f'tournament_{tournament_id}'
        leave_room(room)
        emit('status', {'msg': f'Unsubscribed from tournament {tournament_id} notifications'})

@socketio.on('subscribe_to_user_notifications')
def handle_subscribe_user(data):
    """Subscribe to user-specific notifications"""
    user_id = data.get('user_id')
    if user_id:
        room = f'user_{user_id}'
        join_room(room)
        emit('status', {'msg': f'Subscribed to user {user_id} notifications'})