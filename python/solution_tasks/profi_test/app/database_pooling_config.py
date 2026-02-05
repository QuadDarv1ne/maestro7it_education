"""
Конфигурация пула соединений с базой данных для повышения производительности
"""
import logging
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool, NullPool
from sqlalchemy.pool import StaticPool
import os

logger = logging.getLogger(__name__)

class DatabasePoolManager:
    """Управляет пулом соединений с базой данных с расширенной конфигурацией"""
    
    def __init__(self, app=None):
        self.app = app
        self.engine = None
        self.pool = None
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Инициализация пула соединений с Flask приложением"""
        self.app = app
        
        # Получение конфигурации базы данных
        database_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
        engine_options = app.config.get('SQLALCHEMY_ENGINE_OPTIONS', {})
        
        # Создание оптимизированного движка с пулом соединений
        self.engine = self._create_pooled_engine(database_uri, engine_options)
        
        # Сохранение движка в приложении для легкого доступа
        app.db_engine = self.engine
        
        logger.info("Пул соединений с базой данных инициализирован")
    
    def _create_pooled_engine(self, database_uri, engine_options):
        """Создание SQLAlchemy движка с оптимизированным пулом соединений"""
        
        # Конфигурация пула по умолчанию
        default_pool_config = {
            'poolclass': QueuePool,
            'pool_size': 20,           # Количество соединений для поддержания
            'max_overflow': 30,        # Дополнительные соединения сверх pool_size
            'pool_recycle': 3600,      # Пересоздание соединений через 1 час
            'pool_pre_ping': True,     # Проверка соединений перед использованием
            'pool_timeout': 30,        # Таймаут получения соединения из пула
            'echo': False              # Установить в True для отладки SQL
        }
        
        # Переопределение через переменные окружения при наличии
        pool_config = {
            'pool_size': int(os.environ.get('DB_POOL_SIZE', default_pool_config['pool_size'])),
            'max_overflow': int(os.environ.get('DB_MAX_OVERFLOW', default_pool_config['max_overflow'])),
            'pool_recycle': int(os.environ.get('DB_POOL_RECYCLE', default_pool_config['pool_recycle'])),
            'pool_pre_ping': os.environ.get('DB_POOL_PRE_PING', 'true').lower() == 'true',
            'pool_timeout': int(os.environ.get('DB_POOL_TIMEOUT', default_pool_config['pool_timeout'])),
            'poolclass': QueuePool,
            'echo': os.environ.get('DB_ECHO', 'false').lower() == 'true'
        }
        
        # Специальная обработка SQLite (без пула соединений)
        if database_uri.startswith('sqlite:'):
            if database_uri == 'sqlite:///:memory:':
                # База данных в памяти - используем StaticPool
                pool_config.update({
                    'poolclass': StaticPool,
                    'connect_args': {'check_same_thread': False}
                })
                # Удаление параметров пула, которые не применяются к StaticPool
                pool_config.pop('pool_size', None)
                pool_config.pop('max_overflow', None)
                pool_config.pop('pool_timeout', None)
            else:
                # Файловая SQLite - без пула для избежания блокировок
                pool_config.update({
                    'poolclass': NullPool
                })
                # Удаление параметров пула, которые не применяются к NullPool
                pool_config.pop('pool_size', None)
                pool_config.pop('max_overflow', None)
                pool_config.pop('pool_timeout', None)
        else:
            # Для PostgreSQL, MySQL и др. - используем пул соединений
            # Добавление специфических оптимизаций для разных баз данных
            if 'postgresql' in database_uri:
                pool_config['connect_args'] = {
                    'sslmode': 'prefer',
                    'application_name': 'profi_test'
                }
            elif 'mysql' in database_uri:
                pool_config['connect_args'] = {
                    'charset': 'utf8mb4',
                    'autocommit': True
                }
        
        # Объединение с существующими параметрами движка
        final_config = {**engine_options, **pool_config}
        
        # Создание движка
        engine = create_engine(database_uri, **final_config)
        
        # Подписка на события пула для мониторинга
        from sqlalchemy import event
        
        @event.listens_for(engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            if database_uri.startswith('sqlite:'):
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA journal_mode=WAL")
                cursor.execute("PRAGMA synchronous=NORMAL")
                cursor.execute("PRAGMA cache_size=10000")
                cursor.execute("PRAGMA temp_store=MEMORY")
                cursor.execute("PRAGMA mmap_size=268435456")  # 256MB
                cursor.close()
        
        return engine
    
    def get_pool_stats(self):
        """Получение статистики текущего пула"""
        if not self.engine or not hasattr(self.engine.pool, 'size'):
            return {'error': 'Пул недоступен'}
        
        try:
            pool = self.engine.pool
            stats = {
                'pool_size': pool.size(),
                'checked_in': pool.checkedin() if hasattr(pool, 'checkedin') else 'N/A',
                'checked_out': pool.checkedout() if hasattr(pool, 'checkedout') else 'N/A',
                'overflow': pool.overflow() if hasattr(pool, 'overflow') else 'N/A',
                'recycle': pool._recycle if hasattr(pool, '_recycle') else 'N/A'
            }
            
            # Add additional stats if available
            if hasattr(pool, '_timeout'):
                stats['timeout'] = pool._timeout
            if hasattr(pool, '_max_overflow'):
                stats['max_overflow_setting'] = pool._max_overflow
            
            return stats
        except Exception as e:
            logger.error(f"Ошибка получения статистики пула: {e}")
            return {'error': str(e)}
    
    def monitor_connection_health(self):
        """Мониторинг состояния соединений"""
        if not self.engine:
            return {'error': 'Движок недоступен'}
        
        try:
            # Проверка активности соединения
            with self.engine.connect() as conn:
                # Выполняем простой запрос для проверки работоспособности
                result = conn.execute("SELECT 1").fetchone()
                is_alive = result is not None
            
            stats = self.get_pool_stats()
            stats['connection_alive'] = is_alive
            
            # Проверка производительности соединения
            import time
            start_time = time.time()
            with self.engine.connect() as conn:
                conn.execute("SELECT COUNT(*) FROM sqlite_master").fetchone()
            query_time = time.time() - start_time
            
            stats['health_check_time'] = round(query_time * 1000, 2)  # milliseconds
            
            return stats
        except Exception as e:
            logger.error(f"Ошибка проверки состояния соединения: {e}")
            return {'error': str(e), 'connection_alive': False}
    
    def dispose_pool(self):
        """Освобождение всех соединений в пуле"""
        if self.engine:
            self.engine.dispose()
            logger.info("Пул соединений с базой данных освобожден")
    
    def recreate_pool(self):
        """Пересоздание пула соединений"""
        if self.app and self.app.config.get('SQLALCHEMY_DATABASE_URI'):
            self.engine = self._create_pooled_engine(
                self.app.config['SQLALCHEMY_DATABASE_URI'],
                self.app.config.get('SQLALCHEMY_ENGINE_OPTIONS', {})
            )
            self.app.db_engine = self.engine
            logger.info("Пул соединений с базой данных пересоздан")

# Глобальный экземпляр
db_pool_manager = DatabasePoolManager()

# Flask CLI команды для управления пулом
def register_pool_commands(app):
    """Регистрация CLI команд управления пулом базы данных"""
    import click
    from flask.cli import with_appcontext
    
    @app.cli.command('pool-stats')
    @with_appcontext
    def pool_statistics():
        """Показать статистику пула соединений с базой данных"""
        stats = db_pool_manager.get_pool_stats()
        click.echo("Статистика пула соединений с базой данных:")
        for key, value in stats.items():
            click.echo(f"  {key}: {value}")
    
    @app.cli.command('pool-dispose')
    @with_appcontext
    def dispose_pool():
        """Освободить все соединения с базой данных в пуле"""
        db_pool_manager.dispose_pool()
        click.echo("Пул соединений с базой данных освобожден")
    
    @app.cli.command('pool-recreate')
    @with_appcontext
    def recreate_pool():
        """Пересоздать пул соединений с базой данных"""
        db_pool_manager.recreate_pool()
        click.echo("Пул соединений с базой данных пересоздан")