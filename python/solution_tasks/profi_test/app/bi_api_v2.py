# -*- coding: utf-8 -*-
"""
API конечные точки расширенной системы бизнес-интеллекта для ПрофиТест
Предоставляет доступ к продвинутым аналитическим функциям и прогнозированию
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.business_intelligence_v2 import bi_engine_v2, AnalysisType, TimePeriod
import json
from datetime import datetime

bi_api_v2 = Blueprint('bi_api_v2', __name__)


@bi_api_v2.route('/analytics/user-behavior', methods=['GET'])
@login_required
def analyze_user_behavior():
    """
    Анализирует поведение пользователей.
    """
    try:
        # Получаем параметры запроса
        period_str = request.args.get('period', 'monthly')
        try:
            period = TimePeriod(period_str)
        except ValueError:
            period = TimePeriod.MONTHLY
        
        # Выполняем анализ
        report = bi_engine_v2.analyze_user_behavior(period=period)
        
        return jsonify({
            'success': True,
            'report': {
                'id': report.id,
                'title': report.title,
                'analysis_type': report.analysis_type.value,
                'period': report.period.value,
                'data': report.data,
                'insights': report.insights,
                'recommendations': report.recommendations,
                'created_at': report.created_at.isoformat(),
                'metadata': report.metadata
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@bi_api_v2.route('/analytics/content-performance', methods=['GET'])
@login_required
def analyze_content_performance():
    """
    Анализирует эффективность контента.
    """
    try:
        content_type = request.args.get('content_type')
        
        # Выполняем анализ
        report = bi_engine_v2.analyze_content_performance(content_type=content_type)
        
        return jsonify({
            'success': True,
            'report': {
                'id': report.id,
                'title': report.title,
                'analysis_type': report.analysis_type.value,
                'period': report.period.value,
                'data': report.data,
                'insights': report.insights,
                'recommendations': report.recommendations,
                'created_at': report.created_at.isoformat(),
                'metadata': report.metadata
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@bi_api_v2.route('/analytics/forecast/user-activity', methods=['GET'])
@login_required
def forecast_user_activity():
    """
    Прогнозирует активность пользователей.
    """
    try:
        days_ahead = int(request.args.get('days', 30))
        
        # Выполняем прогноз
        forecast = bi_engine_v2.forecast_user_activity(days_ahead=days_ahead)
        
        return jsonify({
            'success': True,
            'forecast': forecast,
            'days_ahead': days_ahead
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@bi_api_v2.route('/analytics/anomalies', methods=['GET'])
@login_required
def detect_anomalies():
    """
    Обнаруживает аномалии в данных.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        data_type = request.args.get('data_type', 'user_activity')
        
        # Обнаруживаем аномалии
        anomalies = bi_engine_v2.detect_anomalies(data_type=data_type)
        
        return jsonify({
            'success': True,
            'anomalies': anomalies,
            'count': len(anomalies),
            'data_type': data_type
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@bi_api_v2.route('/analytics/segments', methods=['GET'])
@login_required
def get_user_segments():
    """
    Получает сегменты пользователей.
    """
    try:
        n_segments = int(request.args.get('segments', 5))
        
        # Сегментируем пользователей
        segments = bi_engine_v2.segment_users(n_segments=n_segments)
        
        segments_data = []
        for segment in segments:
            segments_data.append({
                'id': segment.id,
                'name': segment.name,
                'description': segment.description,
                'size': segment.size,
                'characteristics': segment.characteristics,
                'created_at': segment.created_at.isoformat()
            })
        
        return jsonify({
            'success': True,
            'segments': segments_data,
            'total_segments': len(segments)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@bi_api_v2.route('/analytics/reports', methods=['GET'])
@login_required
def get_analytics_reports():
    """
    Получает список всех аналитических отчетов.
    """
    try:
        reports = bi_engine_v2.get_all_reports()
        
        reports_data = []
        for report in reports:
            reports_data.append({
                'id': report.id,
                'title': report.title,
                'analysis_type': report.analysis_type.value,
                'period': report.period.value,
                'created_at': report.created_at.isoformat(),
                'insights_count': len(report.insights),
                'recommendations_count': len(report.recommendations)
            })
        
        return jsonify({
            'success': True,
            'reports': reports_data,
            'total_reports': len(reports)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@bi_api_v2.route('/analytics/reports/<report_id>', methods=['GET'])
@login_required
def get_analytics_report(report_id):
    """
    Получает конкретный аналитический отчет.
    """
    try:
        report = bi_engine_v2.get_analytics_report(report_id)
        
        if not report:
            return jsonify({
                'success': False,
                'message': 'Отчет не найден'
            }), 404
        
        return jsonify({
            'success': True,
            'report': {
                'id': report.id,
                'title': report.title,
                'analysis_type': report.analysis_type.value,
                'period': report.period.value,
                'data': report.data,
                'insights': report.insights,
                'recommendations': report.recommendations,
                'created_at': report.created_at.isoformat(),
                'metadata': report.metadata
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@bi_api_v2.route('/analytics/statistics', methods=['GET'])
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
        
        stats = bi_engine_v2.get_statistics()
        
        return jsonify({
            'success': True,
            'statistics': stats
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@bi_api_v2.route('/analytics/types', methods=['GET'])
@login_required
def get_analysis_types():
    """
    Получает список типов анализа.
    """
    try:
        types_data = []
        for analysis_type in AnalysisType:
            type_data = {
                'name': analysis_type.name,
                'value': analysis_type.value,
                'description': self._get_analysis_type_description(analysis_type)
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
    
    def _get_analysis_type_description(self, analysis_type):
        """Получает описание типа анализа."""
        descriptions = {
            AnalysisType.USER_BEHAVIOR: 'Анализ поведения пользователей',
            AnalysisType.CONTENT_PERFORMANCE: 'Анализ эффективности контента',
            AnalysisType.MARKET_TRENDS: 'Анализ рыночных трендов',
            AnalysisType.PREDICTIVE_ANALYTICS: 'Предиктивная аналитика',
            AnalysisType.ANOMALY_DETECTION: 'Обнаружение аномалий',
            AnalysisType.SEGMENTATION: 'Сегментация пользователей'
        }
        return descriptions.get(analysis_type, 'Неизвестный тип анализа')


@bi_api_v2.route('/analytics/periods', methods=['GET'])
@login_required
def get_time_periods():
    """
    Получает список периодов времени для анализа.
    """
    try:
        periods_data = []
        for period in TimePeriod:
            period_data = {
                'name': period.name,
                'value': period.value,
                'description': self._get_period_description(period)
            }
            periods_data.append(period_data)
        
        return jsonify({
            'success': True,
            'periods': periods_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
    
    def _get_period_description(self, period):
        """Получает описание периода."""
        descriptions = {
            TimePeriod.DAILY: 'Ежедневный анализ',
            TimePeriod.WEEKLY: 'Еженедельный анализ',
            TimePeriod.MONTHLY: 'Ежемесячный анализ',
            TimePeriod.QUARTERLY: 'Ежеквартальный анализ',
            TimePeriod.YEARLY: 'Ежегодный анализ'
        }
        return descriptions.get(period, 'Неизвестный период')


@bi_api_v2.route('/analytics/batch', methods=['POST'])
@login_required
def batch_analytics():
    """
    Выполняет пакетный анализ по нескольким параметрам.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        data = request.get_json()
        analyses = data.get('analyses', [])
        
        if not analyses:
            return jsonify({
                'success': False,
                'message': 'Список анализов не может быть пустым'
            }), 400
        
        batch_results = {}
        
        for i, analysis_request in enumerate(analyses):
            try:
                analysis_type = analysis_request.get('type')
                params = analysis_request.get('params', {})
                
                if analysis_type == 'user_behavior':
                    period = TimePeriod(params.get('period', 'monthly'))
                    report = bi_engine_v2.analyze_user_behavior(period=period)
                    batch_results[f'analysis_{i}'] = {
                        'type': 'user_behavior',
                        'report_id': report.id,
                        'title': report.title
                    }
                
                elif analysis_type == 'content_performance':
                    content_type = params.get('content_type')
                    report = bi_engine_v2.analyze_content_performance(content_type=content_type)
                    batch_results[f'analysis_{i}'] = {
                        'type': 'content_performance',
                        'report_id': report.id,
                        'title': report.title
                    }
                
                elif analysis_type == 'forecast':
                    days = params.get('days', 30)
                    forecast = bi_engine_v2.forecast_user_activity(days_ahead=days)
                    batch_results[f'analysis_{i}'] = {
                        'type': 'forecast',
                        'days_ahead': days,
                        'total_predicted_users': forecast['total_predicted_users']
                    }
                
                else:
                    batch_results[f'analysis_{i}'] = {'error': 'Неизвестный тип анализа'}
                    
            except Exception as e:
                batch_results[f'analysis_{i}'] = {'error': str(e)}
        
        return jsonify({
            'success': True,
            'batch_results': batch_results,
            'total_analyses': len(analyses)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@bi_api_v2.route('/analytics/export/<report_id>', methods=['GET'])
@login_required
def export_analytics_report(report_id):
    """
    Экспортирует аналитический отчет.
    """
    try:
        report = bi_engine_v2.get_analytics_report(report_id)
        
        if not report:
            return jsonify({
                'success': False,
                'message': 'Отчет не найден'
            }), 404
        
        # Формат экспорта
        export_format = request.args.get('format', 'json')
        
        if export_format == 'json':
            export_data = {
                'report': {
                    'id': report.id,
                    'title': report.title,
                    'analysis_type': report.analysis_type.value,
                    'period': report.period.value,
                    'data': report.data,
                    'insights': report.insights,
                    'recommendations': report.recommendations,
                    'created_at': report.created_at.isoformat(),
                    'metadata': report.metadata
                },
                'exported_at': datetime.now().isoformat(),
                'exported_by': current_user.username if hasattr(current_user, 'username') else 'unknown'
            }
            
            return jsonify(export_data)
        
        elif export_format == 'csv':
            # В реальной системе здесь будет генерация CSV
            return jsonify({
                'success': False,
                'message': 'Экспорт в CSV временно недоступен'
            }), 501
        
        else:
            return jsonify({
                'success': False,
                'message': 'Неподдерживаемый формат экспорта'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@bi_api_v2.route('/analytics/test', methods=['POST'])
@login_required
def test_bi_system():
    """
    Тестовая функция для проверки системы бизнес-интеллекта.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        # Выполняем тестовые анализы
        user_behavior_report = bi_engine_v2.analyze_user_behavior()
        content_report = bi_engine_v2.analyze_content_performance()
        forecast = bi_engine_v2.forecast_user_activity(days_ahead=7)
        anomalies = bi_engine_v2.detect_anomalies()
        segments = bi_engine_v2.segment_users(n_segments=3)
        
        # Получаем статистику
        stats = bi_engine_v2.get_statistics()
        
        return jsonify({
            'success': True,
            'message': 'Тестовая система бизнес-интеллекта выполнена успешно',
            'test_results': {
                'user_behavior_analysis': {
                    'report_id': user_behavior_report.id,
                    'insights_count': len(user_behavior_report.insights)
                },
                'content_analysis': {
                    'report_id': content_report.id,
                    'metrics_calculated': len(content_report.data.get('metrics', {}))
                },
                'forecast_generated': {
                    'days_ahead': 7,
                    'total_predicted_users': forecast['total_predicted_users']
                },
                'anomalies_detected': len(anomalies),
                'user_segments_created': len(segments)
            },
            'system_statistics': stats
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500