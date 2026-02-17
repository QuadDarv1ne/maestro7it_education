"""
Image Optimization Service - Сервис для автоматической оптимизации изображений
"""
from flask import Flask, request, jsonify, send_file
from PIL import Image
import io
import os
import base64
from datetime import datetime

app = Flask(__name__)

class ImageOptimizer:
    def __init__(self):
        self.supported_formats = ['JPEG', 'PNG', 'WEBP', 'GIF']
        self.quality_settings = {
            'high': 95,
            'medium': 80,
            'low': 60
        }
    
    def optimize_image(self, image_data, target_format='WEBP', quality='medium', max_width=1920, max_height=1080):
        """Оптимизация изображения"""
        try:
            # Открытие изображения
            if isinstance(image_data, str):
                # Если данные в base64
                if image_data.startswith('data:image'):
                    image_data = image_data.split(',')[1]
                image_bytes = base64.b64decode(image_data)
                image = Image.open(io.BytesIO(image_bytes))
            else:
                image = Image.open(image_data)
            
            # Конвертация в RGB если нужно
            if image.mode in ('RGBA', 'LA', 'P'):
                if target_format != 'PNG':
                    # Создаем белый фон для прозрачных изображений
                    background = Image.new('RGB', image.size, (255, 255, 255))
                    if image.mode == 'P':
                        image = image.convert('RGBA')
                    background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                    image = background
                else:
                    image = image.convert('RGBA')
            else:
                image = image.convert('RGB')
            
            # Изменение размера если нужно
            if max_width and max_height:
                image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            
            # Оптимизация
            output = io.BytesIO()
            quality_value = self.quality_settings.get(quality, 80)
            
            if target_format.upper() == 'WEBP':
                image.save(output, format='WEBP', quality=quality_value, method=6, lossless=False)
            elif target_format.upper() == 'JPEG':
                image.save(output, format='JPEG', quality=quality_value, optimize=True, progressive=True)
            elif target_format.upper() == 'PNG':
                image.save(output, format='PNG', optimize=True)
            else:
                image.save(output, format=image.format or 'JPEG', quality=quality_value)
            
            output.seek(0)
            return output.getvalue(), image.size, image.mode
            
        except Exception as e:
            raise Exception(f"Image optimization failed: {str(e)}")
    
    def get_image_info(self, image_data):
        """Получить информацию об изображении"""
        try:
            if isinstance(image_data, str):
                if image_data.startswith('data:image'):
                    image_data = image_data.split(',')[1]
                image_bytes = base64.b64decode(image_data)
                image = Image.open(io.BytesIO(image_bytes))
            else:
                image = Image.open(image_data)
            
            return {
                'format': image.format,
                'mode': image.mode,
                'size': image.size,
                'width': image.width,
                'height': image.height
            }
        except Exception as e:
            raise Exception(f"Failed to get image info: {str(e)}")

optimizer = ImageOptimizer()

@app.route('/optimize', methods=['POST'])
def optimize_image_endpoint():
    """Оптимизация изображения через API"""
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({'error': 'No image data provided'}), 400
        
        image_data = data['image']
        target_format = data.get('format', 'WEBP')
        quality = data.get('quality', 'medium')
        max_width = data.get('max_width', 1920)
        max_height = data.get('max_height', 1080)
        
        # Оптимизация изображения
        optimized_bytes, size, mode = optimizer.optimize_image(
            image_data, target_format, quality, max_width, max_height
        )
        
        # Кодирование в base64 для ответа
        optimized_base64 = base64.b64encode(optimized_bytes).decode('utf-8')
        
        # Получение информации об оригинале
        original_info = optimizer.get_image_info(image_data)
        
        return jsonify({
            'optimized_image': f"data:image/{target_format.lower()};base64,{optimized_base64}",
            'original_info': original_info,
            'optimized_size': size,
            'optimized_mode': mode,
            'format': target_format,
            'quality': quality,
            'saved_bytes': len(base64.b64decode(image_data.split(',')[1] if isinstance(image_data, str) and ',' in image_data else image_data)) - len(optimized_bytes),
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/batch-optimize', methods=['POST'])
def batch_optimize():
    """Пакетная оптимизация изображений"""
    try:
        data = request.get_json()
        
        if not data or 'images' not in data:
            return jsonify({'error': 'No images provided'}), 400
        
        images = data['images']
        target_format = data.get('format', 'WEBP')
        quality = data.get('quality', 'medium')
        max_width = data.get('max_width', 1920)
        max_height = data.get('max_height', 1080)
        
        results = []
        total_saved = 0
        
        for i, image_data in enumerate(images):
            try:
                optimized_bytes, size, mode = optimizer.optimize_image(
                    image_data, target_format, quality, max_width, max_height
                )
                
                optimized_base64 = base64.b64encode(optimized_bytes).decode('utf-8')
                
                original_info = optimizer.get_image_info(image_data)
                saved_bytes = len(base64.b64decode(image_data.split(',')[1] if isinstance(image_data, str) and ',' in image_data else image_data)) - len(optimized_bytes)
                total_saved += saved_bytes
                
                results.append({
                    'index': i,
                    'optimized_image': f"data:image/{target_format.lower()};base64,{optimized_base64}",
                    'original_info': original_info,
                    'optimized_size': size,
                    'saved_bytes': saved_bytes,
                    'status': 'success'
                })
                
            except Exception as e:
                results.append({
                    'index': i,
                    'error': str(e),
                    'status': 'failed'
                })
        
        return jsonify({
            'results': results,
            'total_processed': len(images),
            'successful': len([r for r in results if r['status'] == 'success']),
            'failed': len([r for r in results if r['status'] == 'failed']),
            'total_saved_bytes': total_saved,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/info', methods=['POST'])
def get_image_info():
    """Получить информацию об изображении"""
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({'error': 'No image data provided'}), 400
        
        info = optimizer.get_image_info(data['image'])
        return jsonify({
            'info': info,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Проверка состояния сервиса"""
    return jsonify({
        'status': 'healthy',
        'service': 'image-optimization-service',
        'supported_formats': optimizer.supported_formats,
        'quality_settings': list(optimizer.quality_settings.keys()),
        'timestamp': datetime.utcnow().isoformat()
    })

if __name__ == '__main__':
    debug_mode = os.environ.get('DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=5005, debug=debug_mode)