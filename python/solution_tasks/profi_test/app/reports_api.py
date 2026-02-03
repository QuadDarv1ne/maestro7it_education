# -*- coding: utf-8 -*-
"""
API конечные точки отчетов для ПрофиТест
Предоставляет доступ к расширенным функциям отчетности и визуализации
"""
from flask import Blueprint, request, jsonify, send_file
from flask_login import login_required, current_user
from app.enhanced_reports import enhanced_reports
from app.visualizations import visualizer
from app import db
from app.models import User, TestResult, CareerGoal, LearningPath
import json
import io
import csv
from datetime import datetime

reports_api = Blueprint('reports_api', __name__)


@reports_api.route('/user/<int:user_id>/comprehensive', methods=['GET'])
@login_required
def get_user_comprehensive_report(user_id):
    """Получает комплексный отчет для пользователя"""
    try:
        if not current_user.is_admin and current_user.id != user_id:
            return jsonify({
                'success': False,
                'message': 'Access denied'
            }), 403
        
        report = enhanced_reports.generate_user_comprehensive_report(user_id)
        if report:
            return jsonify({
                'success': True,
                'report': report
            })
        else:
            return jsonify({
                'success': False,
                'message': 'User not found or report could not be generated'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@reports_api.route('/user/<int:user_id>/progress', methods=['GET'])
@login_required
def get_user_progress_report(user_id):
    """Get progress report for a user"""
    try:
        if not current_user.is_admin and current_user.id != user_id:
            return jsonify({
                'success': False,
                'message': 'Access denied'
            }), 403
        
        report = enhanced_reports.generate_user_progress_report(user_id)
        if report:
            return jsonify({
                'success': True,
                'report': report
            })
        else:
            return jsonify({
                'success': False,
                'message': 'User not found or report could not be generated'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@reports_api.route('/system/wide', methods=['GET'])
@login_required
def get_system_wide_report():
    """Получает системный отчет с агрегированной статистикой"""
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Admin access required'
            }), 403
        
        report = enhanced_reports.generate_system_wide_report()
        return jsonify({
            'success': True,
            'report': report
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@reports_api.route('/user/<int:user_id>/visualization/progress-timeline', methods=['GET'])
@login_required
def get_user_progress_timeline(user_id):
    """Получает визуализацию временной шкалы прогресса пользователя"""
    try:
        if not current_user.is_admin and current_user.id != user_id:
            return jsonify({
                'success': False,
                'message': 'Access denied'
            }), 403
        
        chart_html = visualizer.create_user_progress_timeline(user_id)
        if chart_html:
            return jsonify({
                'success': True,
                'chart': chart_html
            })
        else:
            return jsonify({
                'success': False,
                'message': 'No data available for visualization'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@reports_api.route('/user/<int:user_id>/visualization/test-comparison', methods=['GET'])
@login_required
def get_user_test_comparison(user_id):
    """Get user test results comparison visualization"""
    try:
        if not current_user.is_admin and current_user.id != user_id:
            return jsonify({
                'success': False,
                'message': 'Access denied'
            }), 403
        
        chart_html = visualizer.create_test_results_comparison(user_id)
        if chart_html:
            return jsonify({
                'success': True,
                'chart': chart_html
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Insufficient data for comparison'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@reports_api.route('/user/<int:user_id>/visualization/goals-progress', methods=['GET'])
@login_required
def get_user_goals_progress(user_id):
    """Get user career goals progress visualization"""
    try:
        if not current_user.is_admin and current_user.id != user_id:
            return jsonify({
                'success': False,
                'message': 'Access denied'
            }), 403
        
        chart_html = visualizer.create_career_goals_progress(user_id)
        if chart_html:
            return jsonify({
                'success': True,
                'chart': chart_html
            })
        else:
            return jsonify({
                'success': False,
                'message': 'No goals data available'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@reports_api.route('/user/<int:user_id>/visualization/learning-paths', methods=['GET'])
@login_required
def get_user_learning_paths_visualization(user_id):
    """Get user learning paths visualization"""
    try:
        if not current_user.is_admin and current_user.id != user_id:
            return jsonify({
                'success': False,
                'message': 'Access denied'
            }), 403
        
        chart_html = visualizer.create_learning_paths_progress(user_id)
        if chart_html:
            return jsonify({
                'success': True,
                'chart': chart_html
            })
        else:
            return jsonify({
                'success': False,
                'message': 'No learning paths data available'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@reports_api.route('/system/visualization/engagement-heatmap', methods=['GET'])
@login_required
def get_engagement_heatmap():
    """Get system-wide user engagement heatmap"""
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Admin access required'
            }), 403
        
        chart_html = visualizer.create_user_engagement_heatmap()
        if chart_html:
            return jsonify({
                'success': True,
                'chart': chart_html
            })
        else:
            return jsonify({
                'success': False,
                'message': 'No engagement data available'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@reports_api.route('/system/visualization/methodology-comparison', methods=['GET'])
@login_required
def get_methodology_comparison():
    """Get system-wide methodology comparison"""
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Admin access required'
            }), 403
        
        chart_html = visualizer.create_methodology_comparison()
        if chart_html:
            return jsonify({
                'success': True,
                'chart': chart_html
            })
        else:
            return jsonify({
                'success': False,
                'message': 'No methodology data available'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@reports_api.route('/user/<int:user_id>/export/csv', methods=['GET'])
@login_required
def export_user_report_csv(user_id):
    """Экспортирует отчет пользователя в формат CSV"""
    try:
        if not current_user.is_admin and current_user.id != user_id:
            return jsonify({
                'success': False,
                'message': 'Access denied'
            }), 403
        
        # Generate report data
        report_data = enhanced_reports.generate_user_comprehensive_report(user_id)
        if not report_data:
            return jsonify({
                'success': False,
                'message': 'User not found or report could not be generated'
            }), 404
        
        # Export to CSV
        csv_content = enhanced_reports.export_report_to_csv(report_data, 'user')
        if csv_content:
            # Create a BytesIO object from the CSV content
            csv_io = io.StringIO(csv_content)
            
            # Convert to bytes for sending as file
            csv_bytes = csv_io.getvalue().encode('utf-8')
            csv_io_bytes = io.BytesIO(csv_bytes)
            csv_io_bytes.seek(0)
            
            # Create filename
            filename = f"user_{user_id}_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"
            
            return send_file(
                csv_io_bytes,
                mimetype='text/csv',
                as_attachment=True,
                download_name=filename
            )
        else:
            return jsonify({
                'success': False,
                'message': 'Could not generate CSV export'
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@reports_api.route('/system/export/csv', methods=['GET'])
@login_required
def export_system_report_csv():
    """Export system-wide report to CSV"""
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Admin access required'
            }), 403
        
        # Generate report data
        report_data = enhanced_reports.generate_system_wide_report()
        
        # Export to CSV
        csv_content = enhanced_reports.export_report_to_csv(report_data, 'system')
        if csv_content:
            # Create a BytesIO object from the CSV content
            csv_io = io.StringIO(csv_content)
            
            # Convert to bytes for sending as file
            csv_bytes = csv_io.getvalue().encode('utf-8')
            csv_io_bytes = io.BytesIO(csv_bytes)
            csv_io_bytes.seek(0)
            
            # Create filename
            filename = f"system_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"
            
            return send_file(
                csv_io_bytes,
                mimetype='text/csv',
                as_attachment=True,
                download_name=filename
            )
        else:
            return jsonify({
                'success': False,
                'message': 'Could not generate CSV export'
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@reports_api.route('/user/<int:user_id>/dashboard-charts', methods=['GET'])
@login_required
def get_user_dashboard_charts(user_id):
    """Получает все диаграммы дашборда для пользователя"""
    try:
        if not current_user.is_admin and current_user.id != user_id:
            return jsonify({
                'success': False,
                'message': 'Access denied'
            }), 403
        
        charts = visualizer.generate_user_dashboard_charts(user_id)
        return jsonify({
            'success': True,
            'charts': charts
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@reports_api.route('/user/<int:user_id>/recommendations', methods=['GET'])
@login_required
def get_user_recommendations(user_id):
    """Get personalized recommendations for a user"""
    try:
        if not current_user.is_admin and current_user.id != user_id:
            return jsonify({
                'success': False,
                'message': 'Access denied'
            }), 403
        
        # Get user's data
        user = User.query.get_or_404(user_id)
        test_results = TestResult.query.filter_by(user_id=user_id).all()
        career_goals = CareerGoal.query.filter_by(user_id=user_id).all()
        learning_paths = LearningPath.query.filter_by(user_id=user_id).all()
        
        # Get test analysis
        test_analysis = {}
        if test_results:
            latest_result = max(test_results, key=lambda x: x.created_at)
            if latest_result.results:
                try:
                    test_analysis = json.loads(latest_result.results)
                except json.JSONDecodeError:
                    pass
        
        # Generate recommendations
        recommendations = enhanced_reports._generate_user_recommendations(
            user_id, test_analysis, career_goals, learning_paths
        )
        
        return jsonify({
            'success': True,
            'recommendations': recommendations
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@reports_api.route('/user/<int:user_id>/comparative-analysis', methods=['GET'])
@login_required
def get_user_comparative_analysis(user_id):
    """Get comparative analysis of user against other users"""
    try:
        if not current_user.is_admin and current_user.id != user_id:
            return jsonify({
                'success': False,
                'message': 'Access denied'
            }), 403
        
        # Get all users' test results
        all_users_tests = db.session.query(
            TestResult.user_id,
            TestResult.methodology,
            TestResult.results
        ).all()
        
        # Calculate user's average scores
        user_avg_scores = {}
        user_tests = [t for t in all_users_tests if t.user_id == user_id]
        
        for test in user_tests:
            if test.results:
                try:
                    results = json.loads(test.results)
                    if 'scores' in results:
                        for category, score in results['scores'].items():
                            if category not in user_avg_scores:
                                user_avg_scores[category] = []
                            user_avg_scores[category].append(score)
                except json.JSONDecodeError:
                    continue
        
        # Calculate averages for user
        user_averages = {}
        for category, scores in user_avg_scores.items():
            user_averages[category] = sum(scores) / len(scores) if scores else 0
        
        # Calculate overall averages for each category
        all_averages = defaultdict(list)
        for test in all_users_tests:
            if test.results:
                try:
                    results = json.loads(test.results)
                    if 'scores' in results:
                        for category, score in results['scores'].items():
                            all_averages[category].append(score)
                except json.JSONDecodeError:
                    continue
        
        overall_averages = {}
        for category, scores in all_averages.items():
            overall_averages[category] = sum(scores) / len(scores) if scores else 0
        
        # Compare user to overall averages
        comparison = {}
        for category, user_avg in user_averages.items():
            overall_avg = overall_averages.get(category, 0)
            comparison[category] = {
                'user_average': round(user_avg, 2),
                'overall_average': round(overall_avg, 2),
                'difference': round(user_avg - overall_avg, 2),
                'relative_performance': 'above' if user_avg > overall_avg else 'below' if user_avg < overall_avg else 'equal'
            }
        
        # Calculate percentile
        from collections import defaultdict
        user_totals = defaultdict(float)
        user_counts = defaultdict(int)
        
        for test in all_users_tests:
            if test.results:
                try:
                    results = json.loads(test.results)
                    if 'scores' in results:
                        total_score = sum(results['scores'].values())
                        user_totals[test.user_id] += total_score
                        user_counts[test.user_id] += 1
                except json.JSONDecodeError:
                    continue
        
        # Calculate average total score per user
        user_averages = {uid: user_totals[uid] / user_counts[uid] for uid in user_totals}
        
        # Get current user's average
        current_user_avg = user_averages.get(user_id, 0)
        
        # Calculate percentile
        all_averages_list = list(user_averages.values())
        all_averages_list.sort()
        
        if all_averages_list:
            # Find position of current user
            pos = 0
            for avg in all_averages_list:
                if avg <= current_user_avg:
                    pos += 1
                else:
                    break
            
            percentile = (pos / len(all_averages_list)) * 100
        else:
            percentile = 50
        
        analysis = {
            'category_comparison': comparison,
            'total_users_compared': len(set(t.user_id for t in all_users_tests)),
            'user_percentile': round(percentile, 2),
            'interpretation': f"You rank in the top {round(percentile, 1)}th percentile compared to other users."
        }
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


# Import defaultdict for use in the function
from collections import defaultdict