# -*- coding: utf-8 -*-
"""
Модуль расширенного управления конфигурацией для ПрофиТест
Предоставляет продвинутые возможности управления настройками приложения
"""
import os
import json
import yaml
from datetime import datetime
from typing import Any, Dict, Optional, Union
import logging
from functools import wraps


class ConfigSource:
    """Класс для определения источников конфигурации"""
    ENVIRONMENT = 'environment'
    FILE = 'file'
    DATABASE = 'database'
    DEFAULT = 'default'


class ConfigValidationError(Exception):
    """Исключение для ошибок валидации конфигурации"""
    def __init__(self, message: str, field: str = None):
        self.message = message
        self.field = field
        super().__init__(self.message)


class AdvancedConfigManager:
    """
    Расширенный менеджер конфигурации для системы ПрофиТест.
    Обеспечивает гибкое управление настройками из различных источников.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.config_data = {}
        self.config_sources = {}
        self.validators = {}
        self.defaults = {}
        self.required_fields = set()
        
    def load_from_environment(self, prefix: str = 'PROFI_'):
        """
        Загружает конфигурацию из переменных окружения.
        
        Args:
            prefix: Префикс для переменных окружения
        """
        try:
            env_config = {}
            for key, value in os.environ.items():
                if key.startswith(prefix):
                    config_key = key[len(prefix):].lower()
                    env_config[config_key] = self._parse_value(value)
            
            self.config_data.update(env_config)
            self.config_sources.update({k: ConfigSource.ENVIRONMENT for k in env_config.keys()})
            
            self.logger.info(f"Загружено {len(env_config)} параметров из переменных окружения")
            
        except Exception as e:
            self.logger.error(f"Ошибка при загрузке конфигурации из окружения: {str(e)}")
    
    def load_from_file(self, file_path: str, file_format: str = 'auto'):
        """
        Загружает конфигурацию из файла.
        
        Args:
            file_path: Путь к файлу конфигурации
            file_format: Формат файла (json, yaml, auto)
        """
        try:
            if not os.path.exists(file_path):
                self.logger.warning(f"Файл конфигурации не найден: {file_path}")
                return
            
            # Определение формата файла
            if file_format == 'auto':
                if file_path.endswith('.json'):
                    file_format = 'json'
                elif file_path.endswith(('.yaml', '.yml')):
                    file_format = 'yaml'
                else:
                    raise ValueError(f"Неизвестный формат файла: {file_path}")
            
            # Загрузка данных
            with open(file_path, 'r', encoding='utf-8') as f:
                if file_format == 'json':
                    file_config = json.load(f)
                elif file_format == 'yaml':
                    file_config = yaml.safe_load(f)
                else:
                    raise ValueError(f"Неподдерживаемый формат: {file_format}")
            
            self.config_data.update(file_config)
            self.config_sources.update({k: ConfigSource.FILE for k in file_config.keys()})
            
            self.logger.info(f"Загружено {len(file_config)} параметров из файла {file_path}")
            
        except Exception as e:
            self.logger.error(f"Ошибка при загрузке конфигурации из файла {file_path}: {str(e)}")
    
    def load_from_database(self, db_session):
        """
        Загружает конфигурацию из базы данных.
        
        Args:
            db_session: Сессия базы данных
        """
        try:
            # В реальной реализации здесь будет запрос к таблице конфигурации
            # Пока используем заглушку
            db_config = {
                'db_pool_size': 20,
                'db_max_overflow': 30,
                'cache_ttl': 3600
            }
            
            self.config_data.update(db_config)
            self.config_sources.update({k: ConfigSource.DATABASE for k in db_config.keys()})
            
            self.logger.info(f"Загружено {len(db_config)} параметров из базы данных")
            
        except Exception as e:
            self.logger.error(f"Ошибка при загрузке конфигурации из базы данных: {str(e)}")
    
    def set_default(self, key: str, value: Any, description: str = ""):
        """
        Устанавливает значение по умолчанию для параметра.
        
        Args:
            key: Ключ параметра
            value: Значение по умолчанию
            description: Описание параметра
        """
        self.defaults[key] = {
            'value': value,
            'description': description,
            'source': ConfigSource.DEFAULT
        }
        
        # Устанавливаем значение по умолчанию если параметр не задан
        if key not in self.config_data:
            self.config_data[key] = value
            self.config_sources[key] = ConfigSource.DEFAULT
    
    def set_required(self, *keys: str):
        """
        Устанавливает обязательные параметры конфигурации.
        
        Args:
            *keys: Ключи обязательных параметров
        """
        self.required_fields.update(keys)
    
    def register_validator(self, key: str, validator_func):
        """
        Регистрирует функцию валидации для параметра.
        
        Args:
            key: Ключ параметра
            validator_func: Функция валидации
        """
        self.validators[key] = validator_func
    
    def validate_config(self):
        """
        Проверяет конфигурацию на соответствие требованиям.
        
        Raises:
            ConfigValidationError: Если конфигурация не прошла валидацию
        """
        try:
            # Проверка обязательных полей
            missing_fields = self.required_fields - set(self.config_data.keys())
            if missing_fields:
                raise ConfigValidationError(
                    f"Отсутствуют обязательные параметры: {', '.join(missing_fields)}",
                    field=','.join(missing_fields)
                )
            
            # Проверка валидаторов
            for key, validator in self.validators.items():
                if key in self.config_data:
                    try:
                        validator(self.config_data[key])
                    except Exception as e:
                        raise ConfigValidationError(
                            f"Ошибка валидации параметра {key}: {str(e)}",
                            field=key
                        )
            
            self.logger.info("Конфигурация успешно прошла валидацию")
            
        except ConfigValidationError:
            raise
        except Exception as e:
            raise ConfigValidationError(f"Ошибка валидации конфигурации: {str(e)}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Получает значение параметра конфигурации.
        
        Args:
            key: Ключ параметра
            default: Значение по умолчанию
            
        Returns:
            Значение параметра
        """
        return self.config_data.get(key, default)
    
    def get_with_metadata(self, key: str, default: Any = None) -> Dict[str, Any]:
        """
        Получает значение параметра с метаданными.
        
        Args:
            key: Ключ параметра
            default: Значение по умолчанию
            
        Returns:
            dict: Значение и метаданные параметра
        """
        value = self.config_data.get(key, default)
        source = self.config_sources.get(key, ConfigSource.DEFAULT)
        default_info = self.defaults.get(key, {})
        
        return {
            'value': value,
            'source': source,
            'description': default_info.get('description', ''),
            'is_default': source == ConfigSource.DEFAULT,
            'required': key in self.required_fields
        }
    
    def set(self, key: str, value: Any, source: str = ConfigSource.DEFAULT):
        """
        Устанавливает значение параметра конфигурации.
        
        Args:
            key: Ключ параметра
            value: Значение параметра
            source: Источник значения
        """
        self.config_data[key] = value
        self.config_sources[key] = source
    
    def get_all(self) -> Dict[str, Any]:
        """
        Получает все параметры конфигурации.
        
        Returns:
            dict: Все параметры конфигурации
        """
        return self.config_data.copy()
    
    def get_by_source(self, source: str) -> Dict[str, Any]:
        """
        Получает параметры из определенного источника.
        
        Args:
            source: Источник конфигурации
            
        Returns:
            dict: Параметры из указанного источника
        """
        return {
            key: self.config_data[key] 
            for key, src in self.config_sources.items() 
            if src == source
        }
    
    def reload(self):
        """Перезагружает конфигурацию из всех источников"""
        try:
            # Сохраняем текущие значения по умолчанию
            old_defaults = self.defaults.copy()
            old_required = self.required_fields.copy()
            old_validators = self.validators.copy()
            
            # Очистка текущей конфигурации
            self.config_data.clear()
            self.config_sources.clear()
            
            # Восстановление структуры
            self.defaults = old_defaults
            self.required_fields = old_required
            self.validators = old_validators
            
            # Перезагрузка из источников
            # Здесь можно добавить логику перезагрузки из файлов/БД
            
            self.logger.info("Конфигурация успешно перезагружена")
            
        except Exception as e:
            self.logger.error(f"Ошибка при перезагрузке конфигурации: {str(e)}")
    
    def export_config(self, file_path: str, format: str = 'json'):
        """
        Экспортирует конфигурацию в файл.
        
        Args:
            file_path: Путь к файлу для экспорта
            format: Формат экспорта (json, yaml)
        """
        try:
            config_with_metadata = {}
            for key in self.config_data:
                config_with_metadata[key] = self.get_with_metadata(key)
            
            if format == 'json':
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(config_with_metadata, f, indent=2, ensure_ascii=False)
            elif format == 'yaml':
                with open(file_path, 'w', encoding='utf-8') as f:
                    yaml.dump(config_with_metadata, f, default_flow_style=False, allow_unicode=True)
            else:
                raise ValueError(f"Неподдерживаемый формат экспорта: {format}")
            
            self.logger.info(f"Конфигурация экспортирована в {file_path}")
            
        except Exception as e:
            self.logger.error(f"Ошибка при экспорте конфигурации: {str(e)}")
            raise
    
    def _parse_value(self, value: str) -> Union[str, int, float, bool, list, dict]:
        """
        Парсит строковое значение в соответствующий тип данных.
        
        Args:
            value: Строковое значение
            
        Returns:
            Распарсенное значение
        """
        # Попытка преобразования в boolean
        if value.lower() in ('true', 'false', '1', '0'):
            return value.lower() in ('true', '1')
        
        # Попытка преобразования в число
        try:
            if '.' in value:
                return float(value)
            else:
                return int(value)
        except ValueError:
            pass
        
        # Попытка преобразования в JSON
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            pass
        
        # Возвращаем строку если все остальные попытки неудачны
        return value
    
    def create_config_decorator(self, config_key: str):
        """
        Создает декоратор для конфигурируемых функций.
        
        Args:
            config_key: Ключ конфигурации
            
        Returns:
            function: Декоратор
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Получаем значение конфигурации
                config_value = self.get(config_key)
                if config_value:
                    # Передаем конфигурацию в функцию
                    kwargs[config_key] = config_value
                return func(*args, **kwargs)
            return wrapper
        return decorator
    
    def get_config_summary(self) -> Dict[str, Any]:
        """
        Получает сводку по конфигурации.
        
        Returns:
            dict: Сводка конфигурации
        """
        source_counts = {}
        for source in self.config_sources.values():
            source_counts[source] = source_counts.get(source, 0) + 1
        
        return {
            'total_parameters': len(self.config_data),
            'required_parameters': len(self.required_fields),
            'configured_parameters': len([k for k in self.config_data.keys() if k in self.required_fields]),
            'source_distribution': source_counts,
            'validation_status': 'passed' if self._is_valid() else 'failed',
            'last_updated': datetime.utcnow().isoformat()
        }
    
    def _is_valid(self) -> bool:
        """Проверяет валидность текущей конфигурации"""
        try:
            self.validate_config()
            return True
        except ConfigValidationError:
            return False


# Глобальный экземпляр менеджера конфигурации
config_manager = AdvancedConfigManager()