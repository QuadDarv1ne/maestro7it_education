"""
CDN Configuration для ChessCalendar-RU
"""
import os
from flask import Flask, send_from_directory, request, abort
from werkzeug.middleware.proxy_fix import ProxyFix
import os
from PIL import Image
import io
import hashlib
from urllib.parse import urlparse
import requests

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

def optimize_image(image_path, quality=85, max_width=None, max_height=None):
    """Оптимизация изображения"""
    try:
        with Image.open(image_path) as img:
            # Конвертировать в RGB если необходимо (для PNG с альфа-каналом)
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Изменить размер если указаны максимальные параметры
            if max_width or max_height:
                img.thumbnail((max_width or img.width, max_height or img.height), Image.Resampling.LANCZOS)
            
            # Сохранить оптимизированное изображение
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=quality, optimize=True)
            output.seek(0)
            
            return output
    except Exception as e:
        print(f"Error optimizing image {image_path}: {str(e)}")
        return None

def get_image_cache_path(image_filename, width=None, height=None, quality=None):
    """Получить путь к кешированному изображению"""
    cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cache', 'images')
    os.makedirs(cache_dir, exist_ok=True)
    
    # Создать уникальное имя файла на основе параметров
    name, ext = os.path.splitext(image_filename)
    params = f"_{width or 'orig'}x{height or 'orig'}_{quality or 85}" if width or height or quality else ""
    cache_filename = f"{name}{params}_{hashlib.md5((image_filename + str(width) + str(height) + str(quality)).encode()).hexdigest()[:8]}{ext}"
    
    return os.path.join(cache_dir, cache_filename)

# Flask приложение для обслуживания статических файлов
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

@app.before_request
def before_request():
    # Логирование запросов к CDN
    print(f"CDN request: {request.method} {request.path}")

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

@app.route('/cdn/images/optimized/<path:filename>')
def serve_optimized_image(filename):
    """Обслуживание оптимизированных изображений"""
    # Получить параметры из запроса
    width = request.args.get('width', type=int)
    height = request.args.get('height', type=int)
    quality = request.args.get('quality', default=85, type=int)
    
    # Ограничить максимальные значения параметров для безопасности
    width = min(width, 2000) if width else None
    height = min(height, 2000) if height else None
    quality = max(10, min(quality, 100)) if quality else 85
    
    static_folder = os.path.join(app.root_path, '..', 'static')
    original_path = os.path.join(static_folder, 'icons', filename)  # Предполагаем, что изображения в папке icons
    
    # Если файл не найден в icons, проверяем в других папках
    if not os.path.exists(original_path):
        original_path = os.path.join(static_folder, 'images', filename)
        if not os.path.exists(original_path):
            original_path = os.path.join(static_folder, 'screenshots', filename)
            if not os.path.exists(original_path):
                return "Image not found", 404
    
    # Проверить, есть ли уже оптимизированная версия в кэше
    cache_path = get_image_cache_path(filename, width, height, quality)
    
    if os.path.exists(cache_path):
        # Отдать закешированную версию
        response = send_from_directory(os.path.dirname(cache_path), os.path.basename(cache_path))
    else:
        # Оптимизировать изображение и сохранить в кэш
        optimized_img = optimize_image(original_path, quality, width, height)
        if optimized_img:
            # Сохранить оптимизированное изображение в кэш
            os.makedirs(os.path.dirname(cache_path), exist_ok=True)
            with open(cache_path, 'wb') as f:
                f.write(optimized_img.getvalue())
            
            # Отдать из кэша
            response = send_from_directory(os.path.dirname(cache_path), os.path.basename(cache_path))
        else:
            # Если оптимизация не удалась, вернуть оригинальный файл
            response = send_from_directory(os.path.dirname(original_path), os.path.basename(original_path))
    
    response.headers['Cache-Control'] = CDNConfig.CACHE_CONTROL.get('images', 'public, max-age=31536000')
    response.headers['CDN-Provider'] = CDNConfig.CURRENT_PROVIDER
    response.headers['Content-Type'] = 'image/jpeg'
    
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
    debug_mode = os.environ.get('DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=5004, debug=debug_mode)