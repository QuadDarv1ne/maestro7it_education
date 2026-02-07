# -*- coding: utf-8 -*-
"""
Модуль восстановления после ошибок для базы данных товаров Ozon

Этот модуль предоставляет инструменты для восстановления после ошибок 
и обеспечения отказоустойчивости системы базы данных.
"""

import os
import shutil
import traceback
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any
from config import DATABASE_NAME, LOGS_DIR
from utils import get_logger


logger = get_logger(__name__)


class ErrorRecoverySystem:
    """Класс для восстановления после ошибок и обеспечения отказоустойчивости."""
    
    def __init__(self, db_path: str = DATABASE_NAME, logs_dir: str = "logs", recovery_dir: str = "recovery_points"):
        """
        Инициализировать систему восстановления после ошибок.
        
        Args:
            db_path: Путь к основной базе данных
            logs_dir: Директория для логов
            recovery_dir: Директория для точек восстановления
        """
        self.db_path = db_path
        self.logs_dir = Path(logs_dir)
        self.recovery_dir = Path(recovery_dir)
        self.recovery_dir.mkdir(exist_ok=True)
        
        # Словарь для отслеживания точек восстановления
        self.recovery_points: Dict[str, Dict] = {}
        
        logger.info(f"Система восстановления после ошибок инициализирована: {db_path}")
    
    def create_recovery_point(self, name: str = None) -> str:
        """
        Создать точку восстановления базы данных.
        
        Args:
            name: Имя точки восстановления (опционально)
            
        Returns:
            Путь к созданной точке восстановления
        """
        if name is None:
            name = f"recovery_point_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        recovery_path = self.recovery_dir / f"{name}.duckdb"
        
        try:
            # Создать копию базы данных
            shutil.copy2(self.db_path, recovery_path)
            
            # Зарегистрировать точку восстановления
            self.recovery_points[name] = {
                'path': str(recovery_path),
                'timestamp': datetime.now(),
                'size': recovery_path.stat().st_size,
                'description': f'Точка восстановления создана: {datetime.now()}'
            }
            
            logger.info(f"Создана точка восстановления: {name} -> {recovery_path}")
            return str(recovery_path)
            
        except Exception as e:
            logger.error(f"Ошибка при создании точки восстановления: {e}")
            raise
    
    def recover_from_point(self, recovery_point_name: str) -> bool:
        """
        Восстановить базу данных из точки восстановления.
        
        Args:
            recovery_point_name: Имя точки восстановления
            
        Returns:
            Успешность восстановления
        """
        try:
            if recovery_point_name not in self.recovery_points:
                available_points = list(self.recovery_points.keys())
                logger.error(f"Точка восстановления '{recovery_point_name}' не найдена. Доступны: {available_points}")
                return False
            
            recovery_path = self.recovery_points[recovery_point_name]['path']
            
            if not os.path.exists(recovery_path):
                logger.error(f"Файл точки восстановления не существует: {recovery_path}")
                return False
            
            # Сделать резервную копию текущей базы данных
            backup_path = f"{self.db_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            if os.path.exists(self.db_path):
                shutil.copy2(self.db_path, backup_path)
                logger.info(f"Создана резервная копия текущей базы: {backup_path}")
            
            # Восстановить из точки восстановления
            shutil.copy2(recovery_path, self.db_path)
            
            logger.info(f"База данных восстановлена из точки: {recovery_point_name}")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка при восстановлении из точки восстановления: {e}")
            return False
    
    def list_recovery_points(self) -> List[Dict[str, Any]]:
        """
        Получить список всех точек восстановления.
        
        Returns:
            Список точек восстановления
        """
        recovery_list = []
        for name, info in self.recovery_points.items():
            recovery_list.append({
                'name': name,
                'path': info['path'],
                'timestamp': info['timestamp'],
                'size': info['size'],
                'description': info['description']
            })
        
        # Сортировать по времени создания (новые первыми)
        recovery_list.sort(key=lambda x: x['timestamp'], reverse=True)
        return recovery_list
    
    def cleanup_old_recovery_points(self, keep_count: int = 5):
        """
        Удалить старые точки восстановления, оставив только последние N.
        
        Args:
            keep_count: Количество точек восстановления для сохранения
        """
        recovery_points = self.list_recovery_points()
        if len(recovery_points) <= keep_count:
            logger.info(f"Нет необходимости очищать точки восстановления. Всего: {len(recovery_points)}, сохранить: {keep_count}")
            return
        
        recovery_points_to_delete = recovery_points[keep_count:]
        for recovery_point in recovery_points_to_delete:
            recovery_path = Path(recovery_point['path'])
            if recovery_path.exists():
                recovery_path.unlink()
                logger.info(f"Удалена старая точка восстановления: {recovery_point['name']}")
        
        # Обновить внутренний словарь
        self.recovery_points = {rp['name']: self.recovery_points[rp['name']] for rp in recovery_points[:keep_count]}
        
        logger.info(f"Очистка завершена. Удалено: {len(recovery_points_to_delete)} точек восстановления")
    
    def execute_with_recovery(self, operation: Callable, *args, **kwargs) -> Any:
        """
        Выполнить операцию с автоматическим восстановлением при ошибке.
        
        Args:
            operation: Функция для выполнения
            *args: Аргументы для функции
            **kwargs: Ключевые аргументы для функции
            
        Returns:
            Результат выполнения операции
        """
        # Создать точку восстановления перед выполнением операции
        recovery_point_name = f"auto_recovery_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        try:
            # Создать точку восстановления
            recovery_path = self.create_recovery_point(recovery_point_name)
            logger.info(f"Создана автоматическая точка восстановления перед выполнением операции: {recovery_point_name}")
            
            # Выполнить операцию
            result = operation(*args, **kwargs)
            
            # Удалить точку восстановления, если операция прошла успешно
            recovery_path_obj = Path(recovery_path)
            if recovery_path_obj.exists():
                recovery_path_obj.unlink()
                logger.info(f"Удалена автоматическая точка восстановления (операция успешна): {recovery_point_name}")
            
            return result
            
        except Exception as e:
            logger.error(f"Ошибка при выполнении операции: {e}")
            logger.info(f"Пытаюсь восстановить базу данных из точки: {recovery_point_name}")
            
            # Попытаться восстановить из точки восстановления
            success = self.recover_from_point(recovery_point_name)
            if success:
                logger.info("Восстановление успешно выполнено")
            else:
                logger.error("Не удалось выполнить восстановление")
            
            # Удалить использованную точку восстановления
            recovery_path_obj = Path(recovery_path)
            if recovery_path_obj.exists():
                recovery_path_obj.unlink()
            
            # Переподнять исключение
            raise
    
    def handle_exception(self, exception: Exception, context: str = "") -> Dict[str, Any]:
        """
        Обработать исключение и создать отчет о восстановлении.
        
        Args:
            exception: Исключение для обработки
            context: Контекст возникновения исключения
            
        Returns:
            Отчет о восстановлении
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        report = {
            'timestamp': timestamp,
            'exception_type': type(exception).__name__,
            'exception_message': str(exception),
            'traceback': traceback.format_exc(),
            'context': context,
            'recovery_attempts': 0,
            'recovery_success': False
        }
        
        logger.error(f"Обработка исключения в контексте '{context}': {exception}")
        
        # Сохранить отчет в файл
        report_path = self.logs_dir / f"error_report_{timestamp.replace(' ', '_').replace(':', '-')}.txt"
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(f"Отчет об ошибке - {timestamp}\n")
                f.write(f"Контекст: {context}\n")
                f.write(f"Тип исключения: {report['exception_type']}\n")
                f.write(f"Сообщение: {report['exception_message']}\n")
                f.write(f"Трассировка:\n{report['traceback']}\n")
            
            logger.info(f"Отчет об ошибке сохранен: {report_path}")
        except Exception as e:
            logger.error(f"Не удалось сохранить отчет об ошибке: {e}")
        
        return report
    
    def get_recovery_statistics(self) -> Dict[str, Any]:
        """
        Получить статистику по восстановлению.
        
        Returns:
            Статистика по восстановлению
        """
        recovery_points = self.list_recovery_points()
        
        stats = {
            'total_recovery_points': len(recovery_points),
            'total_size_bytes': sum(rp['size'] for rp in recovery_points),
            'latest_recovery_point': recovery_points[0]['timestamp'] if recovery_points else None,
            'oldest_recovery_point': recovery_points[-1]['timestamp'] if recovery_points else None
        }
        
        return stats


def main():
    """Основная функция для демонстрации возможностей системы восстановления после ошибок."""
    from config import LOG_LEVEL
    from utils import setup_logging
    
    # Настроить логирование
    setup_logging(LOG_LEVEL)
    
    logger.info("Запуск системы восстановления после ошибок")
    
    try:
        recovery_system = ErrorRecoverySystem()
        
        print("🔧 СИСТЕМА ВОССТАНОВЛЕНИЯ ПОСЛЕ ОШИБОК")
        print("="*60)
        
        # Создать точку восстановления
        print("1. Создание точки восстановления...")
        recovery_path = recovery_system.create_recovery_point("initial_state")
        print(f"   ✅ Точка восстановления создана: {os.path.basename(recovery_path)}")
        
        # Показать список точек восстановления
        print("\n2. Список точек восстановления:")
        recovery_points = recovery_system.list_recovery_points()
        for i, rp in enumerate(recovery_points, 1):
            print(f"   {i}. {rp['name']} - {rp['size']} байт - {rp['timestamp']}")
        
        # Показать статистику
        print("\n3. Статистика восстановления:")
        stats = recovery_system.get_recovery_statistics()
        print(f"   Всего точек восстановления: {stats['total_recovery_points']}")
        print(f"   Общий размер: {stats['total_size_bytes']} байт")
        print(f"   Последняя точка: {stats['latest_recovery_point']}")
        
        print(f"\n✨ Система восстановления после ошибок работает!")
        
    except Exception as e:
        logger.error(f"Ошибка в системе восстановления: {e}")
        print(f"❌ Ошибка: {e}")


if __name__ == "__main__":
    main()