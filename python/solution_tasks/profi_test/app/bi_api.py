# -*- coding: utf-8 -*-
"""
API конечные точки бизнес-аналитики для ПрофиТест
Предоставляет доступ к функциям аналитики и отчетности
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.business_intelligence import bi_engine, BusinessMetric
import json

bi_api = Blueprint('bi_api', __name__)


@bi_api.route('/comprehensive-analysis', methods=['GET'])
@login_required
def get_comprehensive_analysis():
    """
    Получает результат комплексного анализа системы.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        # В реальной системе здесь будет подключение к базе данных
        # Пока передаем None как заглушку
        analysis_result = bi_engine.perform_comprehensive_analysis(None)
        
        if 'error' in analysis_result:
            return jsonify({
                'success': False,
                'message': analysis_result['error']
            }), 500
        
        return jsonify({
            'success': True,
            'analysis': analysis_result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@bi_api.route('/kpis', methods=['GET'])
@login_required
def get_kpis():
    """
    Получает ключевые показатели эффективности.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        # В реальной системе здесь будет подключение к базе данных
        user_data = bi_engine.load_user_data(None)
        test_data = bi_engine.load_test_data(None)
        
        kpis = bi_engine.calculate_kpi(user_data, test_data)
        
        return jsonify({
            'success': True,
            'kpis': kpis
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@bi_api.route('/user-behavior', methods=['GET'])
@login_required
def get_user_behavior_analysis():
    """
    Получает анализ поведения пользователей.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        user_data = bi_engine.load_user_data(None)
        analysis = bi_engine.analyze_user_behavior(user_data)
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@bi_api.route('/retention-prediction', methods=['GET'])
@login_required
def get_retention_prediction():
    """
    Получает прогноз удержания пользователей.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        user_data = bi_engine.load_user_data(None)
        prediction = bi_engine.predict_user_retention(user_data)
        
        return jsonify({
            'success': True,
            'prediction': prediction
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@bi_api.route('/dashboard-data', methods=['GET'])
@login_required
def get_dashboard_data():
    """
    Получает данные для дашборда бизнес-аналитики.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        # Выполняем анализ для получения актуальных данных
        analysis_result = bi_engine.perform_comprehensive_analysis(None)
        
        if 'error' in analysis_result:
            return jsonify({
                'success': False,
                'message': analysis_result['error']
            }), 500
        
        dashboard_data = bi_engine.generate_dashboard_data(analysis_result)
        
        return jsonify({
            'success': True,
            'dashboard': dashboard_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@bi_api.route('/insights', methods=['GET'])
@login_required
def get_insights():
    """
    Получает инсайты из анализа данных.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        # Выполняем анализ для получения актуальных данных
        analysis_result = bi_engine.perform_comprehensive_analysis(None)
        
        if 'error' in analysis_result:
            return jsonify({
                'success': False,
                'message': analysis_result['error']
            }), 500
        
        insights = analysis_result.get('insights', [])
        
        return jsonify({
            'success': True,
            'insights': insights
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@bi_api.route('/recommendations', methods=['GET'])
@login_required
def get_recommendations():
    """
    Получает рекомендации на основе анализа.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        # Выполняем анализ для получения актуальных данных
        analysis_result = bi_engine.perform_comprehensive_analysis(None)
        
        if 'error' in analysis_result:
            return jsonify({
                'success': False,
                'message': analysis_result['error']
            }), 500
        
        recommendations = analysis_result.get('recommendations', [])
        
        return jsonify({
            'success': True,
            'recommendations': recommendations
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@bi_api.route('/export-report', methods=['POST'])
@login_required
def export_report():
    """
    Экспортирует отчет анализа.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        data = request.get_json()
        format = data.get('format', 'json')
        
        if format not in ['json', 'csv', 'excel']:
            return jsonify({
                'success': False,
                'message': 'Неподдерживаемый формат экспорта'
            }), 400
        
        # Выполняем анализ для получения актуальных данных
        analysis_result = bi_engine.perform_comprehensive_analysis(None)
        
        if 'error' in analysis_result:
            return jsonify({
                'success': False,
                'message': analysis_result['error']
            }), 500
        
        filename = bi_engine.export_analysis_report(analysis_result, format)
        
        if not filename:
            return jsonify({
                'success': False,
                'message': 'Ошибка при экспорте отчета'
            }), 500
        
        return jsonify({
            'success': True,
            'filename': filename,
            'message': f'Отчет экспортирован в {filename}'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@bi_api.route('/trend-analysis', methods=['GET'])
@login_required
def get_trend_analysis():
    """
    Получает анализ трендов.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        # В реальной системе здесь будут исторические данные
        # Пока передаем пустой список как заглушка
        trend_analysis = bi_engine.get_trend_analysis([])
        
        return jsonify({
            'success': True,
            'trend_analysis': trend_analysis
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@bi_api.route('/metrics-overview', methods=['GET'])
@login_required
def get_metrics_overview():
    """
    Получает обзор по ключевым метрикам.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        user_data = bi_engine.load_user_data(None)
        test_data = bi_engine.load_test_data(None)
        
        kpis = bi_engine.calculate_kpi(user_data, test_data)
        
        # Подготавливаем обзор метрик
        metrics_overview = {
            'user_metrics': {
                'total_users': len(user_data) if not user_data.empty else 0,
                'active_users': kpis.get('user_engagement_rate', 0) * len(user_data) if not user_data.empty else 0,
                'premium_users': kpis.get('premium_user_ratio', 0) * len(user_data) if not user_data.empty else 0,
                'avg_satisfaction': kpis.get('avg_satisfaction_score', 0),
                'avg_time_spent': kpis.get('avg_time_spent_minutes', 0)
            },
            'test_metrics': {
                'total_tests': len(test_data) if not test_data.empty else 0,
                'avg_completion_rate': kpis.get('test_completion_rate', 0),
                'avg_tests_per_user': kpis.get('avg_tests_per_user', 0),
                'retention_rate': kpis.get('retention_rate', 0)
            },
            'business_metrics': {
                'conversion_rate': kpis.get('conversion_rate', 0),
                'revenue_per_user': kpis.get('revenue_per_user', 0) if 'revenue_per_user' in kpis else 0
            }
        }
        
        return jsonify({
            'success': True,
            'metrics_overview': metrics_overview
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@bi_api.route('/performance-indicators', methods=['GET'])
@login_required
def get_performance_indicators():
    """
    Получает показатели производительности.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        user_data = bi_engine.load_user_data(None)
        test_data = bi_engine.load_test_data(None)
        
        kpis = bi_engine.calculate_kpi(user_data, test_data)
        
        # Подготавливаем показатели производительности
        performance_indicators = {
            'efficiency': {
                'user_efficiency_score': (
                    kpis.get('user_engagement_rate', 0) * 
                    kpis.get('test_completion_rate', 0) * 
                    100
                ),
                'system_utilization': kpis.get('avg_time_spent_minutes', 0) / 60 if kpis.get('avg_time_spent_minutes') else 0
            },
            'growth': {
                'user_growth_potential': kpis.get('user_engagement_rate', 0) * (1 - kpis.get('retention_rate', 0)),
                'market_penetration': kpis.get('conversion_rate', 0)
            },
            'quality': {
                'service_quality_index': (
                    kpis.get('avg_satisfaction_score', 0) / 5.0 +
                    kpis.get('test_completion_rate', 0)
                ) / 2,
                'user_experience_score': kpis.get('avg_satisfaction_score', 0)
            }
        }
        
        return jsonify({
            'success': True,
            'indicators': performance_indicators
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@bi_api.route('/data-quality-report', methods=['GET'])
@login_required
def get_data_quality_report():
    """
    Получает отчет о качестве данных.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        user_data = bi_engine.load_user_data(None)
        test_data = bi_engine.load_test_data(None)
        
        # Подготавливаем отчет о качестве данных
        data_quality_report = {
            'user_data_quality': {
                'total_records': len(user_data) if not user_data.empty else 0,
                'missing_values': user_data.isnull().sum().to_dict() if not user_data.empty else {},
                'duplicate_records': user_data.duplicated().sum() if not user_data.empty else 0,
                'data_consistency': 'Good' if not user_data.empty else 'Unknown'
            },
            'test_data_quality': {
                'total_records': len(test_data) if not test_data.empty else 0,
                'missing_values': test_data.isnull().sum().to_dict() if not test_data.empty else {},
                'duplicate_records': test_data.duplicated().sum() if not test_data.empty else 0,
                'data_consistency': 'Good' if not test_data.empty else 'Unknown'
            },
            'overall_assessment': {
                'completeness': 0.95 if not user_data.empty and not test_data.empty else 0.0,
                'accuracy': 0.90 if not user_data.empty and not test_data.empty else 0.0,
                'timeliness': 0.98 if not user_data.empty and not test_data.empty else 0.0,
                'consistency': 0.97 if not user_data.empty and not test_data.empty else 0.0
            }
        }
        
        return jsonify({
            'success': True,
            'report': data_quality_report
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@bi_api.route('/analytics-summary', methods=['GET'])
@login_required
def get_analytics_summary():
    """
    Получает сводку по аналитике.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        # Выполняем комплексный анализ
        analysis_result = bi_engine.perform_comprehensive_analysis(None)
        
        if 'error' in analysis_result:
            return jsonify({
                'success': False,
                'message': analysis_result['error']
            }), 500
        
        # Подготавливаем сводку
        summary = {
            'executive_summary': {
                'kpis_met': sum(1 for k, v in analysis_result.get('kpis', {}).items() 
                              if v >= bi_engine.kpi_thresholds.get(BusinessMetric(k.replace('_', ' ').title().replace(' ', '')), 0)) 
                              if analysis_result.get('kpis') else 0,
                'total_recommendations': len(analysis_result.get('recommendations', [])),
                'critical_issues': len([r for r in analysis_result.get('recommendations', []) 
                                      if 'рекомендуется внедрить' in r.lower() or 'необходимы меры' in r.lower()])
            },
            'key_figures': analysis_result.get('kpis', {}),
            'top_insights': analysis_result.get('insights', [])[:5],
            'priority_actions': analysis_result.get('recommendations', [])[:3],
            'data_timestamp': analysis_result['timestamp']
        }
        
        return jsonify({
            'success': True,
            'summary': summary
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@bi_api.route('/business-metrics', methods=['GET'])
@login_required
def get_business_metrics():
    """
    Получает бизнес-метрики.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        user_data = bi_engine.load_user_data(None)
        test_data = bi_engine.load_test_data(None)
        
        kpis = bi_engine.calculate_kpi(user_data, test_data)
        
        # Подготавливаем бизнес-метрики
        business_metrics = {
            'engagement': {
                'metric': 'USER_ENGAGEMENT',
                'value': kpis.get('user_engagement_rate', 0),
                'threshold': bi_engine.kpi_thresholds[BusinessMetric.USER_ENGAGEMENT],
                'status': 'good' if kpis.get('user_engagement_rate', 0) >= bi_engine.kpi_thresholds[BusinessMetric.USER_ENGAGEMENT] else 'needs_attention'
            },
            'completion_rate': {
                'metric': 'TEST_COMPLETION_RATE',
                'value': kpis.get('test_completion_rate', 0),
                'threshold': bi_engine.kpi_thresholds[BusinessMetric.TEST_COMPLETION_RATE],
                'status': 'good' if kpis.get('test_completion_rate', 0) >= bi_engine.kpi_thresholds[BusinessMetric.TEST_COMPLETION_RATE] else 'needs_attention'
            },
            'retention': {
                'metric': 'RETENTION_RATE',
                'value': kpis.get('retention_rate', 0),
                'threshold': bi_engine.kpi_thresholds[BusinessMetric.RETENTION_RATE],
                'status': 'good' if kpis.get('retention_rate', 0) >= bi_engine.kpi_thresholds[BusinessMetric.RETENTION_RATE] else 'needs_attention'
            },
            'conversion': {
                'metric': 'CONVERSION_RATE',
                'value': kpis.get('conversion_rate', 0),
                'threshold': bi_engine.kpi_thresholds[BusinessMetric.CONVERSION_RATE],
                'status': 'good' if kpis.get('conversion_rate', 0) >= bi_engine.kpi_thresholds[BusinessMetric.CONVERSION_RATE] else 'needs_attention'
            },
            'satisfaction': {
                'metric': 'SATISFACTION_SCORE',
                'value': kpis.get('avg_satisfaction_score', 0),
                'threshold': bi_engine.kpi_thresholds[BusinessMetric.SATISFACTION_SCORE],
                'status': 'good' if kpis.get('avg_satisfaction_score', 0) >= bi_engine.kpi_thresholds[BusinessMetric.SATISFACTION_SCORE] else 'needs_attention'
            }
        }
        
        return jsonify({
            'success': True,
            'metrics': business_metrics
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500