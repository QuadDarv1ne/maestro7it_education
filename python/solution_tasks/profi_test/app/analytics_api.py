# -*- coding: utf-8 -*-
"""
API конечные точки расширенной аналитики и отчетов для ПрофиТест
Предоставляет доступ к функциям аналитики и генерации отчетов
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.advanced_analytics import analytics_engine, ReportType, ReportFrequency, AnalyticsDimension
import json
from datetime import datetime, timedelta

analytics_api = Blueprint('analytics_api', __name__)


@analytics_api.route('/reports', methods=['POST'])
@login_required
def generate_report():
    """
    Генерирует новый отчет.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        data = request.get_json()
        
        # Валидация обязательных полей
        required_fields = ['report_type', 'title', 'description', 'start_date', 'end_date']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Поле {field} обязательно'
                }), 400
        
        # Парсинг дат
        try:
            start_date = datetime.fromisoformat(data['start_date'].replace('Z', '+00:00'))
            end_date = datetime.fromisoformat(data['end_date'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({
                'success': False,
                'message': 'Некорректный формат дат'
            }), 400
        
        # Создаем отчет
        report_id = analytics_engine.generate_report(
            report_type=ReportType(data['report_type']),
            title=data['title'],
            description=data['description'],
            date_range=(start_date, end_date),
            data_source=data.get('data_source', 'database')
        )
        
        if report_id:
            return jsonify({
                'success': True,
                'message': 'Отчет успешно сгенерирован',
                'report_id': report_id
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Не удалось сгенерировать отчет'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@analytics_api.route('/reports', methods=['GET'])
@login_required
def get_reports_list():
    """
    Получает список отчетов.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        # Параметры фильтрации
        report_type = request.args.get('type')
        is_scheduled = request.args.get('scheduled')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        # Получаем отчеты
        if report_type:
            try:
                report_type_enum = ReportType(report_type)
                all_reports = analytics_engine.get_reports_by_type(report_type_enum)
            except ValueError:
                return jsonify({
                    'success': False,
                    'message': 'Некорректный тип отчета'
                }), 400
        else:
            all_reports = list(analytics_engine.reports.values())
        
        # Применяем дополнительные фильтры
        if is_scheduled is not None:
            scheduled_flag = is_scheduled.lower() == 'true'
            all_reports = [r for r in all_reports if r.is_scheduled == scheduled_flag]
        
        # Сортировка по дате генерации
        all_reports.sort(key=lambda x: x.generated_at, reverse=True)
        
        # Пагинация
        total_reports = len(all_reports)
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_reports = all_reports[start_idx:end_idx]
        
        # Подготавливаем данные для ответа
        reports_data = []
        for report in paginated_reports:
            report_data = {
                'id': report.id,
                'report_type': report.report_type.value,
                'title': report.title,
                'description': report.description,
                'generated_at': report.generated_at.isoformat(),
                'period_start': report.period_start.isoformat(),
                'period_end': report.period_end.isoformat(),
                'is_scheduled': report.is_scheduled,
                'frequency': report.frequency.value if report.frequency else None,
                'data_size': len(str(report.data))
            }
            reports_data.append(report_data)
        
        return jsonify({
            'success': True,
            'reports': reports_data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total_reports,
                'pages': (total_reports + per_page - 1) // per_page
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@analytics_api.route('/reports/<report_id>', methods=['GET'])
@login_required
def get_report(report_id):
    """
    Получает информацию о конкретном отчете.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        report = analytics_engine.get_report(report_id)
        if not report:
            return jsonify({
                'success': False,
                'message': 'Отчет не найден'
            }), 404
        
        report_data = {
            'id': report.id,
            'report_type': report.report_type.value,
            'title': report.title,
            'description': report.description,
            'generated_at': report.generated_at.isoformat(),
            'period_start': report.period_start.isoformat(),
            'period_end': report.period_end.isoformat(),
            'data': report.data,
            'metadata': report.metadata,
            'is_scheduled': report.is_scheduled,
            'frequency': report.frequency.value if report.frequency else None
        }
        
        return jsonify({
            'success': True,
            'report': report_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@analytics_api.route('/reports/<report_id>', methods=['DELETE'])
@login_required
def delete_report(report_id):
    """
    Удаляет отчет.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        if report_id in analytics_engine.reports:
            del analytics_engine.reports[report_id]
            return jsonify({
                'success': True,
                'message': 'Отчет успешно удален'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Отчет не найден'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@analytics_api.route('/reports/schedule', methods=['POST'])
@login_required
def schedule_report():
    """
    Планирует регулярную генерацию отчета.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        data = request.get_json()
        
        # Валидация обязательных полей
        required_fields = ['report_type', 'title', 'description', 'frequency', 'start_date']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Поле {field} обязательно'
                }), 400
        
        # Парсинг дат
        try:
            start_date = datetime.fromisoformat(data['start_date'].replace('Z', '+00:00'))
            end_date = datetime.fromisoformat(data['end_date'].replace('Z', '+00:00')) if data.get('end_date') else None
        except ValueError:
            return jsonify({
                'success': False,
                'message': 'Некорректный формат дат'
            }), 400
        
        # Создаем запланированный отчет
        schedule_id = analytics_engine.schedule_report(
            report_type=ReportType(data['report_type']),
            title=data['title'],
            description=data['description'],
            frequency=ReportFrequency(data['frequency']),
            start_date=start_date,
            end_date=end_date
        )
        
        if schedule_id:
            return jsonify({
                'success': True,
                'message': 'Отчет успешно запланирован',
                'schedule_id': schedule_id
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Не удалось запланировать отчет'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@analytics_api.route('/analytics/query', methods=['POST'])
@login_required
def execute_analytics_query():
    """
    Выполняет аналитический запрос.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        data = request.get_json()
        
        # Валидация обязательных полей
        required_fields = ['dimensions', 'metrics', 'start_date', 'end_date']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Поле {field} обязательно'
                }), 400
        
        # Парсинг измерений
        try:
            dimensions = [AnalyticsDimension(d) for d in data['dimensions']]
        except ValueError:
            return jsonify({
                'success': False,
                'message': 'Некорректные измерения'
            }), 400
        
        # Парсинг дат
        try:
            start_date = datetime.fromisoformat(data['start_date'].replace('Z', '+00:00'))
            end_date = datetime.fromisoformat(data['end_date'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({
                'success': False,
                'message': 'Некорректный формат дат'
            }), 400
        
        # Выполняем запрос
        query_id = analytics_engine.execute_analytics_query(
            dimensions=dimensions,
            metrics=data['metrics'],
            filters=data.get('filters', {}),
            date_range=(start_date, end_date)
        )
        
        if query_id:
            return jsonify({
                'success': True,
                'message': 'Аналитический запрос выполнен',
                'query_id': query_id
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Не удалось выполнить аналитический запрос'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@analytics_api.route('/analytics/query/<query_id>', methods=['GET'])
@login_required
def get_query_results(query_id):
    """
    Получает результаты аналитического запроса.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        results = analytics_engine.get_query_results(query_id)
        if not results:
            return jsonify({
                'success': False,
                'message': 'Результаты не найдены'
            }), 404
        
        return jsonify({
            'success': True,
            'results': results
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@analytics_api.route('/reports/types', methods=['GET'])
@login_required
def get_report_types():
    """
    Получает список типов отчетов.
    """
    try:
        types_data = []
        for report_type in ReportType:
            type_data = {
                'name': report_type.name,
                'value': report_type.value,
                'description': self._get_report_type_description(report_type)
            }
            types_data.append(type_data)
        
        return jsonify({
            'success': True,
            'types': types_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
    
    def _get_report_type_description(self, report_type):
        """Получает описание типа отчета."""
        descriptions = {
            ReportType.USER_ACTIVITY: 'Активность пользователей',
            ReportType.TEST_PERFORMANCE: 'Производительность тестов',
            ReportType.CONTENT_ANALYTICS: 'Аналитика контента',
            ReportType.SYSTEM_PERFORMANCE: 'Производительность системы',
            ReportType.BUSINESS_METRICS: 'Бизнес-метрики',
            ReportType.USER_ENGAGEMENT: 'Вовлеченность пользователей',
            ReportType.RETENTION_ANALYSIS: 'Анализ удержания',
            ReportType.REVENUE_ANALYSIS: 'Анализ доходов'
        }
        return descriptions.get(report_type, 'Неизвестный тип')


@analytics_api.route('/reports/frequencies', methods=['GET'])
@login_required
def get_report_frequencies():
    """
    Получает список частот генерации отчетов.
    """
    try:
        frequencies_data = []
        for frequency in ReportFrequency:
            frequency_data = {
                'name': frequency.name,
                'value': frequency.value,
                'description': self._get_frequency_description(frequency)
            }
            frequencies_data.append(frequency_data)
        
        return jsonify({
            'success': True,
            'frequencies': frequencies_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
    
    def _get_frequency_description(self, frequency):
        """Получает описание частоты."""
        descriptions = {
            ReportFrequency.DAILY: 'Ежедневно',
            ReportFrequency.WEEKLY: 'Еженедельно',
            ReportFrequency.MONTHLY: 'Ежемесячно',
            ReportFrequency.QUARTERLY: 'Ежеквартально',
            ReportFrequency.YEARLY: 'Ежегодно',
            ReportFrequency.CUSTOM: 'Пользовательская частота'
        }
        return descriptions.get(frequency, 'Неизвестная частота')


@analytics_api.route('/analytics/dimensions', methods=['GET'])
@login_required
def get_analytics_dimensions():
    """
    Получает список измерений аналитики.
    """
    try:
        dimensions_data = []
        for dimension in AnalyticsDimension:
            dimension_data = {
                'name': dimension.name,
                'value': dimension.value,
                'description': self._get_dimension_description(dimension)
            }
            dimensions_data.append(dimension_data)
        
        return jsonify({
            'success': True,
            'dimensions': dimensions_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
    
    def _get_dimension_description(self, dimension):
        """Получает описание измерения."""
        descriptions = {
            AnalyticsDimension.TIME: 'Временные измерения',
            AnalyticsDimension.USER: 'Пользовательские измерения',
            AnalyticsDimension.CONTENT: 'Измерения контента',
            AnalyticsDimension.GEOGRAPHY: 'Географические измерения',
            AnalyticsDimension.DEVICE: 'Измерения устройств',
            AnalyticsDimension.CHANNEL: 'Измерения каналов'
        }
        return descriptions.get(dimension, 'Неизвестное измерение')


@analytics_api.route('/statistics', methods=['GET'])
@login_required
def get_analytics_statistics():
    """
    Получает статистику по аналитике.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        stats = analytics_engine.get_statistics()
        return jsonify({
            'success': True,
            'statistics': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@analytics_api.route('/reports/recent', methods=['GET'])
@login_required
def get_recent_reports():
    """
    Получает последние отчеты.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        limit = int(request.args.get('limit', 5))
        recent_reports = analytics_engine.get_recent_reports(limit)
        
        reports_data = []
        for report in recent_reports:
            report_data = {
                'id': report.id,
                'report_type': report.report_type.value,
                'title': report.title,
                'generated_at': report.generated_at.isoformat(),
                'is_scheduled': report.is_scheduled
            }
            reports_data.append(report_data)
        
        return jsonify({
            'success': True,
            'reports': reports_data,
            'count': len(reports_data)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@analytics_api.route('/test-analytics', methods=['POST'])
@login_required
def test_analytics_system():
    """
    Тестовая функция для проверки системы аналитики.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        # Генерируем тестовый отчет
        test_report_id = analytics_engine.generate_report(
            report_type=ReportType.USER_ACTIVITY,
            title='Тестовый отчет активности',
            description='Тестовый отчет для проверки системы',
            date_range=(datetime.now() - timedelta(days=7), datetime.now())
        )
        
        if test_report_id:
            # Получаем информацию о тестовом отчете
            test_report = analytics_engine.get_report(test_report_id)
            
            return jsonify({
                'success': True,
                'message': 'Тестовая аналитика выполнена успешно',
                'test_report_id': test_report_id,
                'report_info': {
                    'title': test_report.title,
                    'type': test_report.report_type.value,
                    'generated_at': test_report.generated_at.isoformat()
                }
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Не удалось выполнить тестовую аналитику'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500