"""
Оптимизация статических файлов для Simple HR
Минификация CSS/JS и сжатие
"""

import os
import re
import gzip
import shutil
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class StaticOptimizer:
    """Оптимизатор статических файлов"""
    
    def __init__(self, static_folder: str):
        self.static_folder = Path(static_folder)
        self.compression_level = 9  # Максимальное сжатие
    
    def minify_css(self, css_content: str) -> str:
        """
        Минификация CSS
        Удаляет комментарии, лишние пробелы и переносы строк
        """
        # Удаление комментариев /* */
        css_content = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)
        
        # Удаление пробелов вокруг {, }, :, ;
        css_content = re.sub(r'\s*([{}:;,])\s*', r'\1', css_content)
        
        # Удаление переносов строк и множественных пробелов
        css_content = re.sub(r'\s+', ' ', css_content)
        
        # Удаление пробелов в начале и конце
        css_content = css_content.strip()
        
        return css_content
    
    def minify_js(self, js_content: str) -> str:
        """
        Базовая минификация JavaScript
        Удаляет комментарии и лишние пробелы
        """
        # Удаление однострочных комментариев //
        js_content = re.sub(r'//.*?\n', '\n', js_content)
        
        # Удаление многострочных комментариев /* */
        js_content = re.sub(r'/\*.*?\*/', '', js_content, flags=re.DOTALL)
        
        # Удаление множественных пробелов
        js_content = re.sub(r'\s+', ' ', js_content)
        
        # Удаление пробелов вокруг операторов
        js_content = re.sub(r'\s*([{};,()=])\s*', r'\1', js_content)
        
        return js_content.strip()
    
    def compress_file(self, file_path: Path) -> bool:
        """
        Создание gzip-сжатой версии файла
        """
        try:
            gz_path = file_path.with_suffix(file_path.suffix + '.gz')
            
            with open(file_path, 'rb') as f_in:
                with gzip.open(gz_path, 'wb', compresslevel=self.compression_level) as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            original_size = file_path.stat().st_size
            compressed_size = gz_path.stat().st_size
            ratio = (1 - compressed_size / original_size) * 100
            
            logger.info(
                f"Сжат {file_path.name}: "
                f"{original_size} -> {compressed_size} байт "
                f"({ratio:.1f}% сжатие)"
            )
            return True
            
        except Exception as e:
            logger.error(f"Ошибка сжатия {file_path}: {e}")
            return False
    
    def optimize_css_file(self, css_file: Path) -> bool:
        """Оптимизация CSS файла"""
        try:
            # Пропускаем уже минифицированные файлы
            if '.min.' in css_file.name:
                return False
            
            with open(css_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_size = len(content)
            minified = self.minify_css(content)
            minified_size = len(minified)
            
            # Создание .min.css версии
            min_file = css_file.with_name(
                css_file.stem + '.min.css'
            )
            
            with open(min_file, 'w', encoding='utf-8') as f:
                f.write(minified)
            
            # Сжатие минифицированной версии
            self.compress_file(min_file)
            
            ratio = (1 - minified_size / original_size) * 100
            logger.info(
                f"Минифицирован {css_file.name}: "
                f"{original_size} -> {minified_size} байт "
                f"({ratio:.1f}% уменьшение)"
            )
            return True
            
        except Exception as e:
            logger.error(f"Ошибка минификации {css_file}: {e}")
            return False
    
    def optimize_js_file(self, js_file: Path) -> bool:
        """Оптимизация JS файла"""
        try:
            # Пропускаем уже минифицированные файлы
            if '.min.' in js_file.name:
                return False
            
            with open(js_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_size = len(content)
            minified = self.minify_js(content)
            minified_size = len(minified)
            
            # Создание .min.js версии
            min_file = js_file.with_name(
                js_file.stem + '.min.js'
            )
            
            with open(min_file, 'w', encoding='utf-8') as f:
                f.write(minified)
            
            # Сжатие минифицированной версии
            self.compress_file(min_file)
            
            ratio = (1 - minified_size / original_size) * 100
            logger.info(
                f"Минифицирован {js_file.name}: "
                f"{original_size} -> {minified_size} байт "
                f"({ratio:.1f}% уменьшение)"
            )
            return True
            
        except Exception as e:
            logger.error(f"Ошибка минификации {js_file}: {e}")
            return False
    
    def optimize_all(self) -> dict:
        """
        Оптимизация всех статических файлов
        
        Returns:
            dict: Статистика оптимизации
        """
        stats = {
            'css_files': 0,
            'js_files': 0,
            'compressed_files': 0,
            'errors': []
        }
        
        # Поиск и оптимизация CSS файлов
        for css_file in self.static_folder.glob('*.css'):
            if '.min.' not in css_file.name:
                if self.optimize_css_file(css_file):
                    stats['css_files'] += 1
        
        # Поиск и оптимизация JS файлов
        for js_file in self.static_folder.glob('*.js'):
            if '.min.' not in js_file.name:
                if self.optimize_js_file(js_file):
                    stats['js_files'] += 1
        
        # Сжатие всех текстовых файлов
        for pattern in ['*.css', '*.js', '*.html', '*.svg']:
            for file in self.static_folder.glob(pattern):
                if not file.name.endswith('.gz'):
                    if self.compress_file(file):
                        stats['compressed_files'] += 1
        
        logger.info(
            f"Оптимизация завершена: "
            f"{stats['css_files']} CSS, "
            f"{stats['js_files']} JS, "
            f"{stats['compressed_files']} сжатых файлов"
        )
        
        return stats
    
    def clean_optimized(self):
        """Удаление оптимизированных файлов (.min и .gz)"""
        count = 0
        
        for pattern in ['*.min.css', '*.min.js', '*.gz']:
            for file in self.static_folder.glob(pattern):
                file.unlink()
                count += 1
        
        logger.info(f"Удалено {count} оптимизированных файлов")
        return count


def optimize_static_files(app):
    """
    Flask команда для оптимизации статических файлов
    Использование: flask optimize-static
    """
    static_folder = app.static_folder
    optimizer = StaticOptimizer(static_folder)
    
    print(f"🚀 Оптимизация статических файлов в {static_folder}...")
    stats = optimizer.optimize_all()
    
    print(f"✅ Готово!")
    print(f"   CSS файлов минифицировано: {stats['css_files']}")
    print(f"   JS файлов минифицировано: {stats['js_files']}")
    print(f"   Файлов сжато: {stats['compressed_files']}")
    
    return stats


if __name__ == '__main__':
    # Для тестирования
    import sys
    if len(sys.argv) > 1:
        static_folder = sys.argv[1]
        optimizer = StaticOptimizer(static_folder)
        optimizer.optimize_all()
    else:
        print("Использование: python static_optimizer.py <путь_к_static_папке>")
