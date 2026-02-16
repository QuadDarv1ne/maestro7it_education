"""
CDN Configuration для ChessCalendar-RU
"""
import os
from flask import Flask, send_from_directory
from werkzeug.middleware.proxy_fix import ProxyFix

class CDNConfig:
    # Конфигурация CDN провайдеров
    CDN_PROVIDERS = {
        'cloudflare': {
            'base_url': 'https://your-subdomain.cloudflare.com',
            'api_key': os.environ.get('CLOUDFLARE_API_KEY'),
            'zone_id': os.environ.get('CLOUDFLARE_ZONE_ID')
        },
        'aws_cloudfront': {
            'base_url': 'https://your-distribution-id.cloudfront.net',
            'access_key': os.environ.get('AWS_ACCESS_KEY_ID'),
            'secret_key': os.environ.get('AWS_SECRET_ACCESS_KEY'),
            'distribution_id': os.environ.get('AWS_CLOUDFRONT_DISTRIBUTION_ID')
        },
        'google_cloud_cdn': {
            'base_url': 'https://storage.googleapis.com/your-bucket-name',
            'project_id': os.environ.get('GOOGLE_CLOUD_PROJECT_ID'),
            'bucket_name': os.environ.get('GOOGLE_CLOUD_BUCKET_NAME')
        }
    }
    
    # Текущий провайдер
    CURRENT_PROVIDER = os.environ.get('CDN_PROVIDER', 'cloudflare')
    
    # Типы файлов для CDN
    CDN_FILE_TYPES = {
        'images': ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'],
        'css': ['.css'],
        'js': ['.js'],
        'fonts': ['.woff', '.woff2', '.ttf', '.eot'],
        'videos': ['.mp4', '.webm', '.ogg']
    }
    
    # Настройки кэширования
    CACHE_CONTROL = {
        'images': 'public, max-age=31536000',  # 1 год
        'css': 'public, max-age=2592000',      # 30 дней
        'js': 'public, max-age=2592000',       # 30 дней
        'fonts': 'public, max-age=31536000',   # 1 год
        'videos': 'public, max-age=2592000'    # 30 дней
    }

def get_cdn_url(filename, file_type='images'):
    """Получить CDN URL для файла"""
    if CDNConfig.CURRENT_PROVIDER not in CDNConfig.CDN_PROVIDERS:
        return None
    
    provider = CDNConfig.CDN_PROVIDERS[CDNConfig.CURRENT_PROVIDER]
    base_url = provider['base_url']
    
    return f"{base_url}/{file_type}/{filename}"

def is_cdn_file(filename):
    """Проверить, должен ли файл загружаться через CDN"""
    _, ext = os.path.splitext(filename.lower())
    
    for file_type, extensions in CDNConfig.CDN_FILE_TYPES.items():
        if ext in extensions:
            return True, file_type
    
    return False, None

# Flask приложение для обслуживания статических файлов
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

@app.route('/cdn/<file_type>/<path:filename>')
def serve_cdn_file(file_type, filename):
    """Обслуживание файлов через CDN"""
    # Проверка типа файла
    if file_type not in CDNConfig.CDN_FILE_TYPES:
        return "Invalid file type", 400
    
    # Проверка расширения файла
    _, ext = os.path.splitext(filename.lower())
    if ext not in CDNConfig.CDN_FILE_TYPES[file_type]:
        return "Invalid file extension", 400
    
    # Проверка существования файла
    static_folder = os.path.join(app.root_path, '..', 'static')
    file_path = os.path.join(static_folder, file_type, filename)
    
    if not os.path.exists(file_path):
        return "File not found", 404
    
    # Установка заголовков кэширования
    cache_control = CDNConfig.CACHE_CONTROL.get(file_type, 'public, max-age=3600')
    
    response = send_from_directory(
        os.path.join(static_folder, file_type),
        filename
    )
    
    response.headers['Cache-Control'] = cache_control
    response.headers['CDN-Provider'] = CDNConfig.CURRENT_PROVIDER
    
    return response

@app.route('/cdn/upload', methods=['POST'])
def upload_to_cdn():
    """Загрузка файлов в CDN"""
    # В реальной реализации здесь будет логика загрузки в выбранный CDN провайдер
    return {"status": "not_implemented", "message": "CDN upload functionality needs to be implemented with specific provider APIs"}

@app.route('/cdn/status')
def cdn_status():
    """Проверка состояния CDN"""
    return {
        "provider": CDNConfig.CURRENT_PROVIDER,
        "configured": CDNConfig.CURRENT_PROVIDER in CDNConfig.CDN_PROVIDERS,
        "file_types": list(CDNConfig.CDN_FILE_TYPES.keys()),
        "cache_settings": CDNConfig.CACHE_CONTROL
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)