#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для автоматического перевода документации на русский язык
Автоматически переводит все файлы README и документацию в проекте
"""

import os
import re
from pathlib import Path

class DocumentationTranslator:
    def __init__(self):
        self.translations = {
            # Заголовки секций
            '## Quick Start': '## Быстрый старт',
            '## Components': '## Компоненты',
            '## Useful Commands': '## Полезные команды',
            '## Data Persistence': '## Персистентность данных',
            '## Environment Setup': '## Настройка окружения',
            '## Troubleshooting': '## Решение проблем',
            '## Feature Expansion': '## Расширение функционала',
            '## Requirements': '## Требования',
            '## Installation and Setup': '## Установка и запуск',
            '## Application Architecture': '## Архитектура приложения',
            '## Functional Features': '## Функциональные возможности',
            '## Integration with Main Project': '## Интеграция с основным проектом',
            '## Development Plans': '## Планы развития',
            '## Contributing': '## Вклад в развитие',
            '## License': '## Лицензия',
            '## Contacts': '## Контакты',
            
            # Подзаголовки
            '### Main container': '### Основной контейнер',
            '### SQLite Web Interface': '### Веб-интерфейс SQLite',
            '### Container Management': '### Управление контейнерами',
            '### Working with the main container': '### Работа с основным контейнером',
            '### Working with databases': '### Работа с базами данных',
            '### Environment Variables': '### Переменные окружения',
            '### Ports': '### Порты',
            '### If ports are busy': '### Если порты заняты',
            '### If containers fail to start': '### Если контейнеры не запускаются',
            '### Data updates': '### Обновление данных',
            '### Adding new databases': '### Добавление новых баз данных',
            '### Installing additional Python libraries': '### Установка дополнительных Python-библиотек',
            '### Core Functionality': '### Основной функционал',
            '### Learning Capabilities': '### Обучающие возможности',
            '### Technical Features': '### Технические особенности',
            '### Quick Start': '### Быстрый старт',
            '### Build for Publication': '### Сборка для публикации',
            '### Main Components': '### Основные компоненты',
            '### Practice Mode': '### Режим практики',
            '### Learning Mode': '### Обучающий режим',
            '### Competition Mode': '### Режим соревнований',
            '### Data Synchronization': '### Синхронизация данных',
            '### API Integration': '### API интеграция',
            '### Near-term Updates': '### Ближайшие обновления',
            '### Long-term Goals': '### Долгосрочные цели',
            '### How to Help the Project': '### Как помочь проекту',
            '### Contribution Guide': '### Руководство по вкладу',
            
            # Описания и термины
            'SQL Learning Platform': 'SQL Обучающая Платформа',
            'React Native': 'React Native',
            'Mobile application': 'Мобильное приложение',
            'Development Guidelines': 'Руководство по разработке',
            'CI/CD Pipeline': 'CI/CD Pipeline',
            'Quality Standards': 'Стандарты качества',
            'Security Standards': 'Стандарты безопасности',
            'Performance Requirements': 'Требования к производительности',
            'Database Management': 'Управление базами данных',
            'Query Execution': 'Выполнение запросов',
            'Learning Analytics': 'Аналитика обучения',
            'Exercise Management': 'Управление упражнениями',
            'Error Handling': 'Обработка ошибок',
            'SDK Examples': 'Примеры SDK',
            'Webhooks': 'Вебхуки',
            'Support and Documentation': 'Поддержка и документация',
            'API Documentation': 'Документация API',
            'Code Quality Standards': 'Стандарты качества кода',
            'Testing Requirements': 'Требования к тестированию',
            'Documentation Standards': 'Стандарты документации',
            'Branching Strategy': 'Стратегия ветвления',
            'Version Control': 'Контроль версий',
            'Monitoring and Maintenance': 'Мониторинг и обслуживание',
            'Contribution Guidelines': 'Руководство по внесению вклада',
        }
    
    def translate_file(self, file_path):
        """Переводит файл документации"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Применяем переводы
            original_content = content
            for english, russian in self.translations.items():
                content = content.replace(english, russian)
            
            # Если были изменения, сохраняем файл
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ Переведен: {file_path}")
                return True
            else:
                print(f"ℹ️  Нет изменений: {file_path}")
                return False
                
        except Exception as e:
            print(f"❌ Ошибка перевода {file_path}: {e}")
            return False
    
    def translate_project(self, project_root):
        """Переводит всю документацию в проекте"""
        project_path = Path(project_root)
        translated_files = []
        
        # Ищем файлы для перевода
        patterns = [
            '**/README.md',
            '**/*.md',
            '**/Dockerfile',
            '**/docker-compose.yml'
        ]
        
        for pattern in patterns:
            for file_path in project_path.glob(pattern):
                # Пропускаем уже переведенные файлы
                if 'docs' in str(file_path) or 'README' in str(file_path):
                    if self.translate_file(file_path):
                        translated_files.append(str(file_path))
        
        print(f"\n🏁 Перевод завершен!")
        print(f"📄 Переведено файлов: {len(translated_files)}")
        if translated_files:
            print("Список переведенных файлов:")
            for file in translated_files:
                print(f"  • {file}")

def main():
    print("🇷🇺 Автоматический перевод документации на русский язык")
    print("=" * 60)
    
    translator = DocumentationTranslator()
    current_dir = os.getcwd()
    
    print(f"📂 Рабочая директория: {current_dir}")
    print("🔍 Начинаем перевод документации...\n")
    
    translator.translate_project(current_dir)
    
    print("\n✅ Все файлы документации переведены на русский язык")

if __name__ == "__main__":
    main()