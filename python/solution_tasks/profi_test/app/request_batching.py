# -*- coding: utf-8 -*-
"""
Пакетная обработка запросов и массовые операции для улучшения производительности
"""
import logging
from flask import request, jsonify
from typing import Dict, Any, List, Callable, Optional
import time
import threading
from collections import defaultdict, deque
from functools import wraps
import json

logger = logging.getLogger(__name__)

class RequestBatcher:
    """Группирует похожие запросы вместе для лучшей производительности"""
    
    def __init__(self, app=None):
        self.app = app
        self.batch_queues = defaultdict(deque)
        self.batch_callbacks = {}
        self.batch_config = {
            'default_batch_size': 10,
            'max_batch_size': 100,
            'batch_timeout': 0.1,  # seconds
            'max_queue_size': 1000
        }
        self.stats = defaultdict(int)
        self.batch_threads = {}
        self.batch_lock = threading.Lock()
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Инициализирует группировщик запросов с Flask приложением"""
        self.app = app
        app.request_batcher = self
    
    def register_batch_endpoint(self, endpoint_name: str, batch_processor: Callable, 
                              batch_size: int = None, timeout: float = None):
        """
        Регистрирует конечную точку пакетной обработки
        
        Args:
            endpoint_name: Название конечной точки
            batch_processor: Функция для обработки пакетных запросов
            batch_size: Максимальный размер пакета
            timeout: Максимальное время ожидания формирования пакета
        """
        self.batch_callbacks[endpoint_name] = {
            'processor': batch_processor,
            'batch_size': batch_size or self.batch_config['default_batch_size'],
            'timeout': timeout or self.batch_config['batch_timeout']
        }
        
        logger.info(f"Registered batch endpoint: {endpoint_name}")
    
    def add_to_batch(self, endpoint_name: str, request_data: Dict[str, Any], 
                    callback: Callable = None) -> Any:
        """
        Добавляет запрос в очередь пакетной обработки
        
        Args:
            endpoint_name: Название конечной точки пакетной обработки
            request_data: Данные запроса для обработки
            callback: Необязательный обратный вызов для результата
        
        Returns:
            Результат пакетной обработки
        """
        if endpoint_name not in self.batch_callbacks:
            raise ValueError(f"Batch endpoint '{endpoint_name}' not registered")
        
        # Create batch item
        batch_item = {
            'data': request_data,
            'callback': callback,
            'timestamp': time.time(),
            'result': None,
            'completed': False
        }
        
        # Add to queue
        with self.batch_lock:
            queue = self.batch_queues[endpoint_name]
            queue.append(batch_item)
            
            # Start batch processing thread if not already running
            if endpoint_name not in self.batch_threads or not self.batch_threads[endpoint_name].is_alive():
                self._start_batch_processor(endpoint_name)
            
            # Check queue size limits
            if len(queue) > self.batch_config['max_queue_size']:
                logger.warning(f"Batch queue for {endpoint_name} exceeded max size")
                # Remove oldest items
                while len(queue) > self.batch_config['max_queue_size'] // 2:
                    queue.popleft()
        
        self.stats['requests_added'] += 1
        
        # Wait for result (blocking)
        while not batch_item['completed']:
            time.sleep(0.001)  # 1ms sleep to prevent busy waiting
        
        return batch_item['result']
    
    def _start_batch_processor(self, endpoint_name: str):
        """Запускает фоновый поток для пакетной обработки"""
        def process_batch():
            try:
                self._process_batch_queue(endpoint_name)
            except Exception as e:
                logger.error(f"Error in batch processor for {endpoint_name}: {e}")
        
        thread = threading.Thread(target=process_batch, daemon=True)
        thread.start()
        self.batch_threads[endpoint_name] = thread
    
    def _process_batch_queue(self, endpoint_name: str):
        """Обрабатывает запросы в очереди пакетной обработки"""
        config = self.batch_callbacks[endpoint_name]
        processor = config['processor']
        max_batch_size = config['batch_size']
        timeout = config['timeout']
        
        while True:
            batch_items = []
            
            # Collect batch items
            with self.batch_lock:
                queue = self.batch_queues[endpoint_name]
                
                # Collect items for current batch
                while queue and len(batch_items) < max_batch_size:
                    item = queue[0]
                    
                    # Check if item has timed out
                    if time.time() - item['timestamp'] > timeout:
                        batch_items.append(queue.popleft())
                    elif len(batch_items) >= max_batch_size:
                        break
                    else:
                        # Wait for more items or timeout
                        break
            
            # Process batch if we have items
            if batch_items:
                try:
                    self._execute_batch(endpoint_name, batch_items, processor)
                except Exception as e:
                    logger.error(f"Error processing batch for {endpoint_name}: {e}")
                    # Mark all items as failed
                    for item in batch_items:
                        item['result'] = {'error': str(e)}
                        item['completed'] = True
            
            # Sleep briefly to prevent busy waiting
            time.sleep(0.001)
            
            # Exit if queue is empty
            with self.batch_lock:
                if not self.batch_queues[endpoint_name]:
                    break
    
    def _execute_batch(self, endpoint_name: str, batch_items: List[Dict], processor: Callable):
        """Выполняет пакетную обработку"""
        start_time = time.time()
        
        try:
            # Extract request data
            batch_data = [item['data'] for item in batch_items]
            
            # Process batch
            batch_results = processor(batch_data)
            
            # Distribute results
            for i, item in enumerate(batch_items):
                if i < len(batch_results):
                    item['result'] = batch_results[i]
                else:
                    item['result'] = {'error': 'No result for this item'}
                item['completed'] = True
            
            # Update statistics
            execution_time = time.time() - start_time
            self.stats[f'{endpoint_name}_batches_processed'] += 1
            self.stats[f'{endpoint_name}_items_processed'] += len(batch_items)
            self.stats[f'{endpoint_name}_avg_batch_time'] = (
                self.stats.get(f'{endpoint_name}_avg_batch_time', 0) * 0.9 +
                execution_time * 0.1
            )
            
            logger.debug(f"Processed batch of {len(batch_items)} items for {endpoint_name} in {execution_time:.4f}s")
            
        except Exception as e:
            logger.error(f"Batch execution failed for {endpoint_name}: {e}")
            raise

class BulkOperationManager:
    """Управляет массовыми операциями базы данных для лучшей производительности"""
    
    def __init__(self, app=None):
        self.app = app
        self.bulk_operations = {}
        self.stats = defaultdict(int)
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Инициализирует менеджер массовых операций с Flask приложением"""
        self.app = app
        app.bulk_operation_manager = self
    
    def register_bulk_operation(self, operation_name: str, bulk_processor: Callable):
        """Регистрирует процессор массовой операции"""
        self.bulk_operations[operation_name] = bulk_processor
        logger.info(f"Registered bulk operation: {operation_name}")
    
    def execute_bulk_operation(self, operation_name: str, data_list: List[Dict]) -> Dict[str, Any]:
        """Выполняет массовую операцию с оптимизацией производительности"""
        if operation_name not in self.bulk_operations:
            raise ValueError(f"Bulk operation '{operation_name}' not registered")
        
        start_time = time.time()
        processor = self.bulk_operations[operation_name]
        
        try:
            # Execute bulk operation
            result = processor(data_list)
            
            # Update statistics
            execution_time = time.time() - start_time
            self.stats[f'{operation_name}_operations'] += 1
            self.stats[f'{operation_name}_items_processed'] += len(data_list)
            self.stats[f'{operation_name}_total_time'] += execution_time
            
            logger.info(f"Bulk operation {operation_name}: {len(data_list)} items in {execution_time:.4f}s")
            
            return {
                'success': True,
                'items_processed': len(data_list),
                'execution_time': execution_time,
                'result': result
            }
            
        except Exception as e:
            logger.error(f"Bulk operation {operation_name} failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'items_processed': 0,
                'execution_time': time.time() - start_time
            }

def batch_request(batch_key: str = None, batch_size: int = 10):
    """
    Декоратор для создания конечных точек пакетных запросов
    
    Usage:
        @app.route('/api/batch/users', methods=['POST'])
        @batch_request('user_lookup', batch_size=20)
        def batch_user_lookup(batch_data):
            # Process batch of user lookups
            results = []
            for data in batch_data:
                user = User.query.get(data['user_id'])
                results.append({'user_id': user.id, 'username': user.username})
            return results
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Check if this is a batch request
            if request.is_json:
                try:
                    batch_data = request.get_json()
                    
                    if isinstance(batch_data, list):
                        # This is a batch request
                        batcher = request_batcher
                        if not batcher:
                            # Fallback to direct execution
                            return jsonify(func(batch_data))
                        
                        # Process each item in batch
                        results = []
                        for item in batch_data:
                            if batch_key:
                                result = batcher.add_to_batch(batch_key, item)
                            else:
                                result = func([item])[0] if func([item]) else None
                            results.append(result)
                        
                        return jsonify(results)
                    else:
                        # Single request - treat as batch of one
                        result = func([batch_data])
                        return jsonify(result[0] if result else None)
                        
                except Exception as e:
                    logger.error(f"Error processing batch request: {e}")
                    return jsonify({'error': str(e)}), 400
            else:
                # Not JSON request
                return jsonify({'error': 'Request must be JSON'}), 400
        
        # Register batch endpoint
        if batch_key:
            def batch_processor(data_list):
                return func(data_list)
            
            # Register with request batcher
            from flask import current_app
            if hasattr(current_app, 'request_batcher'):
                current_app.request_batcher.register_batch_endpoint(
                    batch_key, batch_processor, batch_size=batch_size
                )
        
        return wrapper
    return decorator

class DatabaseBatchInserter:
    """Оптимизирует массовую вставку в базу данных"""
    
    def __init__(self, model_class, batch_size: int = 100):
        self.model_class = model_class
        self.batch_size = batch_size
        self.batch_buffer = []
        self.lock = threading.Lock()
        
    def add(self, **kwargs):
        """Добавить элемент в пакет"""
        with self.lock:
            self.batch_buffer.append(kwargs)
            
            if len(self.batch_buffer) >= self.batch_size:
                self._flush_batch()
    
    def add_many(self, items: List[Dict]):
        """Добавить несколько элементов в пакет"""
        with self.lock:
            self.batch_buffer.extend(items)
            
            while len(self.batch_buffer) >= self.batch_size:
                self._flush_batch()
    
    def flush(self):
        """Очистить оставшиеся элементы в буфере"""
        with self.lock:
            if self.batch_buffer:
                self._flush_batch()
    
    def _flush_batch(self):
        """Очистить текущий пакет в базу данных"""
        if not self.batch_buffer:
            return
        
        try:
            from app import db
            
            # Create model instances
            instances = [self.model_class(**data) for data in self.batch_buffer[:self.batch_size]]
            
            # Bulk insert
            db.session.bulk_save_objects(instances)
            db.session.commit()
            
            # Remove processed items
            self.batch_buffer = self.batch_buffer[self.batch_size:]
            
            logger.debug(f"Flushed batch of {len(instances)} {self.model_class.__name__} objects")
            
        except Exception as e:
            logger.error(f"Error in batch insert: {e}")
            db.session.rollback()
            raise

# Global instances
request_batcher = RequestBatcher()
bulk_manager = BulkOperationManager()

# Flask CLI commands
def register_batching_commands(app):
    """Регистрирует CLI команды для пакетной обработки"""
    import click
    from flask.cli import with_appcontext
    
    @app.cli.command('batch-stats')
    @with_appcontext
    def show_batch_stats():
        """Показывает статистику пакетной обработки"""
        if hasattr(app, 'request_batcher'):
            stats = app.request_batcher.stats
            click.echo("Request Batching Statistics:")
            for key, value in stats.items():
                click.echo(f"  {key}: {value}")
        else:
            click.echo("Request batcher not initialized")
    
    @app.cli.command('bulk-stats')
    @with_appcontext
    def show_bulk_stats():
        """Показывает статистику массовых операций"""
        if hasattr(app, 'bulk_operation_manager'):
            stats = app.bulk_operation_manager.stats
            click.echo("Bulk Operation Statistics:")
            for key, value in stats.items():
                click.echo(f"  {key}: {value}")
        else:
            click.echo("Bulk operation manager not initialized")