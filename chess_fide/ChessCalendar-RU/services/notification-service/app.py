"""
Push Notification Service - Сервис для веб-уведомлений
"""
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
import json
import uuid
import redis

app = Flask(__name__)

# Redis для хранения подписок
redis_client = redis.Redis(host='redis', port=6379, db=0)

class PushNotificationService:
    def __init__(self):
        self.subscribers = {}  # Хранение подписчиков в памяти (в реальном приложении Redis)
    
    def subscribe_user(self, user_id, endpoint, keys, auth):
        """Подписка пользователя на уведомления"""
        subscription_id = str(uuid.uuid4())
        
        subscription_data = {
            'user_id': user_id,
            'endpoint': endpoint,
            'keys': keys,
            'auth': auth,
            'created_at': datetime.utcnow().isoformat(),
            'subscription_id': subscription_id
        }
        
        # Сохранение в Redis
        redis_client.hset('subscriptions', subscription_id, json.dumps(subscription_data))
        redis_client.sadd(f'user_subscriptions:{user_id}', subscription_id)
        
        return subscription_id
    
    def unsubscribe_user(self, subscription_id):
        """Отписка пользователя от уведомлений"""
        subscription_data = redis_client.hget('subscriptions', subscription_id)
        if subscription_data:
            data = json.loads(subscription_data)
            user_id = data['user_id']
            
            redis_client.hdel('subscriptions', subscription_id)
            redis_client.srem(f'user_subscriptions:{user_id}', subscription_id)
            return True
        return False
    
    def get_user_subscriptions(self, user_id):
        """Получить все подписки пользователя"""
        subscription_ids = redis_client.smembers(f'user_subscriptions:{user_id}')
        subscriptions = []
        
        for sub_id in subscription_ids:
            sub_id = sub_id.decode('utf-8')
            subscription_data = redis_client.hget('subscriptions', sub_id)
            if subscription_data:
                subscriptions.append(json.loads(subscription_data))
        
        return subscriptions
    
    def send_notification(self, subscription_id, title, body, icon='/static/icons/icon-192x192.png', url='/'):
        """Отправка уведомления конкретной подписке"""
        try:
            subscription_data = redis_client.hget('subscriptions', subscription_id)
            if not subscription_data:
                return False
            
            # В реальном приложении здесь будет отправка через Web Push API
            # Пока сохраняем в очередь для демонстрации
            notification_data = {
                'subscription_id': subscription_id,
                'title': title,
                'body': body,
                'icon': icon,
                'url': url,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            # Сохранение в очередь уведомлений
            queue_key = f'notification_queue:{subscription_id}'
            redis_client.lpush(queue_key, json.dumps(notification_data))
            redis_client.expire(queue_key, 3600)  # Хранить 1 час
            
            return True
        except Exception as e:
            print(f"Error sending notification: {e}")
            return False
    
    def send_bulk_notification(self, user_ids, title, body, icon='/static/icons/icon-192x192.png', url='/'):
        """Массовая отправка уведомлений группе пользователей"""
        sent_count = 0
        failed_count = 0
        
        for user_id in user_ids:
            subscriptions = self.get_user_subscriptions(user_id)
            for subscription in subscriptions:
                success = self.send_notification(
                    subscription['subscription_id'], title, body, icon, url
                )
                if success:
                    sent_count += 1
                else:
                    failed_count += 1
        
        return {
            'sent': sent_count,
            'failed': failed_count,
            'total_users': len(user_ids)
        }

notification_service = PushNotificationService()

# HTML шаблон для демонстрации
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Push Notifications Demo</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
    <h1>Web Push Notifications Demo</h1>
    
    <div id="status">Проверка поддержки...</div>
    <button id="subscribeBtn" disabled>Подписаться на уведомления</button>
    <button id="unsubscribeBtn" disabled>Отписаться</button>
    
    <div id="notifications">
        <h2>Последние уведомления:</h2>
        <ul id="notificationList"></ul>
    </div>
    
    <script>
        let subscription = null;
        const statusEl = document.getElementById('status');
        const subscribeBtn = document.getElementById('subscribeBtn');
        const unsubscribeBtn = document.getElementById('unsubscribeBtn');
        const notificationList = document.getElementById('notificationList');
        
        // Проверка поддержки
        if ('serviceWorker' in navigator && 'PushManager' in window) {
            statusEl.textContent = 'Push уведомления поддерживаются';
            subscribeBtn.disabled = false;
            
            // Регистрация Service Worker
            navigator.serviceWorker.register('/sw.js')
                .then(registration => {
                    console.log('Service Worker registered:', registration);
                })
                .catch(error => {
                    console.error('Service Worker registration failed:', error);
                    statusEl.textContent = 'Ошибка регистрации Service Worker';
                });
        } else {
            statusEl.textContent = 'Push уведомления не поддерживаются';
        }
        
        // Подписка на уведомления
        subscribeBtn.addEventListener('click', async () => {
            try {
                const permission = await Notification.requestPermission();
                if (permission !== 'granted') {
                    statusEl.textContent = 'Разрешение на уведомления не получено';
                    return;
                }
                
                const registration = await navigator.serviceWorker.ready;
                subscription = await registration.pushManager.subscribe({
                    userVisibleOnly: true,
                    applicationServerKey: urlBase64ToUint8Array('your-public-vapid-key')
                });
                
                // Отправка подписки на сервер
                const response = await fetch('/api/subscribe', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        subscription: subscription.toJSON(),
                        userId: 'demo-user-123'
                    })
                });
                
                if (response.ok) {
                    statusEl.textContent = 'Успешно подписаны на уведомления';
                    subscribeBtn.disabled = true;
                    unsubscribeBtn.disabled = false;
                }
            } catch (error) {
                console.error('Subscription failed:', error);
                statusEl.textContent = 'Ошибка подписки: ' + error.message;
            }
        });
        
        // Отписка
        unsubscribeBtn.addEventListener('click', async () => {
            if (subscription) {
                await subscription.unsubscribe();
                subscription = null;
                statusEl.textContent = 'Отписаны от уведомлений';
                subscribeBtn.disabled = false;
                unsubscribeBtn.disabled = true;
            }
        });
        
        // Функция для конвертации VAPID ключа
        function urlBase64ToUint8Array(base64String) {
            const padding = '='.repeat((4 - base64String.length % 4) % 4);
            const base64 = (base64String + padding)
                .replace(/\-/g, '+')
                .replace(/_/g, '/');
            
            const rawData = window.atob(base64);
            const outputArray = new Uint8Array(rawData.length);
            
            for (let i = 0; i < rawData.length; ++i) {
                outputArray[i] = rawData.charCodeAt(i);
            }
            return outputArray;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Главная страница с демо уведомлений"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    """API для подписки на уведомления"""
    try:
        data = request.get_json()
        subscription = data.get('subscription')
        user_id = data.get('userId', 'anonymous')
        
        if not subscription:
            return jsonify({'error': 'No subscription data provided'}), 400
        
        subscription_id = notification_service.subscribe_user(
            user_id,
            subscription.get('endpoint'),
            subscription.get('keys', {}),
            subscription.get('auth', '')
        )
        
        return jsonify({
            'status': 'success',
            'subscription_id': subscription_id,
            'message': 'Successfully subscribed to notifications'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/unsubscribe/<subscription_id>', methods=['DELETE'])
def unsubscribe(subscription_id):
    """API для отписки от уведомлений"""
    try:
        success = notification_service.unsubscribe_user(subscription_id)
        
        if success:
            return jsonify({
                'status': 'success',
                'message': 'Successfully unsubscribed from notifications'
            })
        else:
            return jsonify({'error': 'Subscription not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/notify', methods=['POST'])
def send_notification():
    """API для отправки уведомления"""
    try:
        data = request.get_json()
        subscription_id = data.get('subscription_id')
        title = data.get('title', 'Новое уведомление')
        body = data.get('body', 'У вас новое сообщение')
        icon = data.get('icon', '/static/icons/icon-192x192.png')
        url = data.get('url', '/')
        
        if not subscription_id:
            return jsonify({'error': 'No subscription_id provided'}), 400
        
        success = notification_service.send_notification(subscription_id, title, body, icon, url)
        
        if success:
            return jsonify({
                'status': 'success',
                'message': 'Notification sent successfully'
            })
        else:
            return jsonify({'error': 'Failed to send notification'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/notify/bulk', methods=['POST'])
def send_bulk_notification():
    """API для массовой отправки уведомлений"""
    try:
        data = request.get_json()
        user_ids = data.get('user_ids', [])
        title = data.get('title', 'Новое уведомление')
        body = data.get('body', 'У вас новое сообщение')
        icon = data.get('icon', '/static/icons/icon-192x192.png')
        url = data.get('url', '/')
        
        if not user_ids:
            return jsonify({'error': 'No user_ids provided'}), 400
        
        result = notification_service.send_bulk_notification(user_ids, title, body, icon, url)
        
        return jsonify({
            'status': 'success',
            'result': result,
            'message': 'Bulk notifications sent'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/subscriptions/<user_id>', methods=['GET'])
def get_subscriptions(user_id):
    """Получить подписки пользователя"""
    try:
        subscriptions = notification_service.get_user_subscriptions(user_id)
        return jsonify({
            'subscriptions': subscriptions,
            'count': len(subscriptions)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/sw.js')
def service_worker():
    """Service Worker для push уведомлений"""
    sw_content = """
self.addEventListener('push', function(event) {
    const data = event.data.json();
    
    const options = {
        body: data.body,
        icon: data.icon,
        badge: '/static/icons/icon-72x72.png',
        vibrate: [100, 50, 100],
        data: {
            url: data.url
        }
    };
    
    event.waitUntil(
        self.registration.showNotification(data.title, options)
    );
});

self.addEventListener('notificationclick', function(event) {
    event.notification.close();
    
    event.waitUntil(
        clients.openWindow(event.notification.data.url)
    );
});
"""
    return sw_content, 200, {'Content-Type': 'application/javascript'}

@app.route('/health', methods=['GET'])
def health_check():
    """Проверка состояния сервиса"""
    return jsonify({
        'status': 'healthy',
        'service': 'push-notification-service',
        'timestamp': datetime.utcnow().isoformat()
    })

if __name__ == '__main__':
    debug_mode = os.environ.get('DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=5007, debug=debug_mode)