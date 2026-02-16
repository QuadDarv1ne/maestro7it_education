"""
Система real-time обновлений через WebSocket
Мгновенные уведомления и обновления для пользователей
"""

from flask_socketio import emit, join_room, leave_room, rooms
from typing import Dict, List, Any, Optional
from datetime import datetime
import json


class RealtimeUpdateManager:
    """Менеджер real-time обновлений"""
    
    def __init__(self, socketio=None):
        self.socketio = socketio
        self.active_connections = {}
        self.room_subscriptions = {}
        
    def init_app(self, socketio):
        """Инициализация с SocketIO"""
        self.socketio = socketio
        self._register_handlers()
    
    def _register_handlers(self):
        """Регистрация обработчиков событий"""
        
        @self.socketio.on('connect')
        def handle_connect():
            """Обработка подключения клиента"""
            from flask import request
            
            user_id = request.args.get('user_id')
            if user_id:
                self.active_connections[request.sid] = {
                    'user_id': user_id,
                    'connected_at': datetime.utcnow(),
                    'rooms': []
                }
                
                # Автоматическая подписка на персональную комнату
                join_room(f'user_{user_id}')
                
                emit('connected', {
                    'status': 'success',
                    'message': 'Connected to real-time updates',
                    'timestamp': datetime.utcnow().isoformat()
                })
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            """Обработка отключения клиента"""
            from flask import request
            
            if request.sid in self.active_connections:
                del self.active_connections[request.sid]
        
        @self.socketio.on('subscribe')
        def handle_subscribe(data):
            """Подписка на комнату/канал"""
            room = data.get('room')
            if room:
                join_room(room)
                emit('subscribed', {
                    'room': room,
                    'timestamp': datetime.utcnow().isoformat()
                })
        
        @self.socketio.on('unsubscribe')
        def handle_unsubscribe(data):
            """Отписка от комнаты/канала"""
            room = data.get('room')
            if room:
                leave_room(room)
                emit('unsubscribed', {
                    'room': room,
                    'timestamp': datetime.utcnow().isoformat()
                })
    
    def broadcast_tournament_update(
        self,
        tournament_id: int,
        update_type: str,
        data: Dict[str, Any]
    ):
        """
        Отправка обновления о турнире всем подписчикам
        
        Args:
            tournament_id: ID турнира
            update_type: Тип обновления (created, updated, deleted, status_changed)
            data: Данные обновления
        """
        if not self.socketio:
            return
        
        message = {
            'type': 'tournament_update',
            'update_type': update_type,
            'tournament_id': tournament_id,
            'data': data,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # Отправка в комнату турнира
        self.socketio.emit(
            'tournament_update',
            message,
            room=f'tournament_{tournament_id}'
        )
        
        # Отправка в общую комнату турниров
        self.socketio.emit(
            'tournament_update',
            message,
            room='tournaments'
        )
    
    def notify_user(
        self,
        user_id: int,
        notification_type: str,
        title: str,
        message: str,
        data: Optional[Dict[str, Any]] = None
    ):
        """
        Отправка уведомления конкретному пользователю
        
        Args:
            user_id: ID пользователя
            notification_type: Тип уведомления
            title: Заголовок
            message: Сообщение
            data: Дополнительные данные
        """
        if not self.socketio:
            return
        
        notification = {
            'type': notification_type,
            'title': title,
            'message': message,
            'data': data or {},
            'timestamp': datetime.utcnow().isoformat()
        }
        
        self.socketio.emit(
            'notification',
            notification,
            room=f'user_{user_id}'
        )
    
    def broadcast_system_message(
        self,
        message: str,
        severity: str = 'info',
        action_required: bool = False
    ):
        """
        Отправка системного сообщения всем подключенным пользователям
        
        Args:
            message: Текст сообщения
            severity: Уровень важности (info, warning, error)
            action_required: Требуется ли действие от пользователя
        """
        if not self.socketio:
            return
        
        system_message = {
            'type': 'system_message',
            'message': message,
            'severity': severity,
            'action_required': action_required,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        self.socketio.emit('system_message', system_message, broadcast=True)
    
    def send_live_stats_update(self, stats: Dict[str, Any]):
        """
        Отправка обновления live статистики
        
        Args:
            stats: Статистические данные
        """
        if not self.socketio:
            return
        
        self.socketio.emit(
            'stats_update',
            {
                'stats': stats,
                'timestamp': datetime.utcnow().isoformat()
            },
            room='stats'
        )
    
    def broadcast_user_activity(
        self,
        user_id: int,
        activity_type: str,
        details: Dict[str, Any]
    ):
        """
        Отправка информации о активности пользователя
        
        Args:
            user_id: ID пользователя
            activity_type: Тип активности
            details: Детали активности
        """
        if not self.socketio:
            return
        
        activity = {
            'user_id': user_id,
            'activity_type': activity_type,
            'details': details,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # Отправка в комнату активности
        self.socketio.emit(
            'user_activity',
            activity,
            room='activity_feed'
        )
    
    def send_typing_indicator(
        self,
        room: str,
        user_id: int,
        is_typing: bool
    ):
        """
        Отправка индикатора набора текста (для чатов/форума)
        
        Args:
            room: Комната/канал
            user_id: ID пользователя
            is_typing: Печатает ли пользователь
        """
        if not self.socketio:
            return
        
        self.socketio.emit(
            'typing',
            {
                'user_id': user_id,
                'is_typing': is_typing,
                'timestamp': datetime.utcnow().isoformat()
            },
            room=room
        )
    
    def get_active_users_count(self) -> int:
        """Получить количество активных подключений"""
        return len(self.active_connections)
    
    def get_room_users(self, room: str) -> List[int]:
        """Получить список пользователей в комнате"""
        users = []
        for sid, conn_data in self.active_connections.items():
            if room in conn_data.get('rooms', []):
                users.append(conn_data['user_id'])
        return users
    
    def disconnect_user(self, user_id: int, reason: str = 'Server initiated'):
        """
        Принудительное отключение пользователя
        
        Args:
            user_id: ID пользователя
            reason: Причина отключения
        """
        if not self.socketio:
            return
        
        for sid, conn_data in list(self.active_connections.items()):
            if conn_data['user_id'] == user_id:
                self.socketio.emit(
                    'force_disconnect',
                    {'reason': reason},
                    room=sid
                )
                # SocketIO автоматически обработает отключение


class LiveDashboard:
    """Live дашборд для администраторов"""
    
    def __init__(self, realtime_manager: RealtimeUpdateManager):
        self.realtime_manager = realtime_manager
        self.update_interval = 5  # секунды
    
    def start_live_updates(self):
        """Запуск live обновлений дашборда"""
        import threading
        import time
        
        def update_loop():
            while True:
                try:
                    stats = self._collect_stats()
                    self.realtime_manager.send_live_stats_update(stats)
                    time.sleep(self.update_interval)
                except Exception as e:
                    import logging
                    logging.error(f"Error in live dashboard update: {e}")
                    time.sleep(self.update_interval)
        
        thread = threading.Thread(target=update_loop, daemon=True)
        thread.start()
    
    def _collect_stats(self) -> Dict[str, Any]:
        """Сбор статистики для дашборда"""
        from app.models.tournament import Tournament
        from app.models.user import User
        from app.utils.advanced_monitoring import performance_monitor
        from app.utils.health_checker import health_checker
        
        # Статистика турниров
        total_tournaments = Tournament.query.count()
        active_tournaments = Tournament.query.filter(
            Tournament.status == 'Ongoing'
        ).count()
        
        # Статистика пользователей
        total_users = User.query.count()
        active_connections = self.realtime_manager.get_active_users_count()
        
        # Производительность
        perf_summary = performance_monitor.get_summary()
        
        # Здоровье системы
        health_summary = health_checker.get_summary()
        
        return {
            'tournaments': {
                'total': total_tournaments,
                'active': active_tournaments
            },
            'users': {
                'total': total_users,
                'online': active_connections
            },
            'performance': {
                'avg_response_time': perf_summary.get('avg_response_time', 0),
                'error_rate': perf_summary.get('error_rate', 0)
            },
            'health': {
                'status': health_summary.get('status', 'unknown'),
                'healthy_checks': health_summary.get('healthy_checks', 0),
                'total_checks': health_summary.get('total_checks', 0)
            },
            'timestamp': datetime.utcnow().isoformat()
        }


# Глобальный экземпляр
realtime_manager = RealtimeUpdateManager()
