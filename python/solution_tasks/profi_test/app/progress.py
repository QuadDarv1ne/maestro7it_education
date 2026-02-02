from flask import Blueprint, jsonify, render_template
from flask_login import login_required, current_user
from app import db
from app.models import TestResult, UserProgress
import json
from datetime import datetime

progress_bp = Blueprint('progress', __name__)

@progress_bp.route('/progress')
@login_required
def user_progress():
    """Просмотр прогресса пользователя"""
    # Получаем все результаты тестов пользователя
    test_results = TestResult.query.filter_by(user_id=current_user.id).order_by(
        TestResult.created_at.asc()
    ).all()
    
    # Формируем данные для графиков
    progress_data = []
    for result in test_results:
        try:
            results_dict = json.loads(result.results) if result.results else {}
            scores = results_dict.get('scores', {})
            
            progress_data.append({
                'id': result.id,
                'methodology': result.methodology,
                'created_at': result.created_at.isoformat(),
                'formatted_date': result.created_at.strftime('%d.%m.%Y'),
                'scores': scores,
                'dominant_category': results_dict.get('dominant_category', 'Не определено')
            })
        except:
            # Если не удается разобрать JSON, используем базовые данные
            progress_data.append({
                'id': result.id,
                'methodology': result.methodology,
                'created_at': result.created_at.isoformat(),
                'formatted_date': result.created_at.strftime('%d.%m.%Y'),
                'scores': {},
                'dominant_category': 'Не определено'
            })
    
    return render_template('progress/overview.html', progress_data=progress_data)

@progress_bp.route('/progress/export')
@login_required
def export_progress():
    """Экспорт данных прогресса"""
    test_results = TestResult.query.filter_by(user_id=current_user.id).order_by(
        TestResult.created_at.asc()
    ).all()
    
    export_data = []
    for result in test_results:
        try:
            results_dict = json.loads(result.results) if result.results else {}
            export_data.append({
                'test_id': result.id,
                'methodology': result.methodology,
                'created_at': result.created_at.isoformat(),
                'date': result.created_at.strftime('%d.%m.%Y'),
                'scores': results_dict.get('scores', {}),
                'dominant_category': results_dict.get('dominant_category', 'Не определено'),
                'recommendation': result.recommendation
            })
        except:
            export_data.append({
                'test_id': result.id,
                'methodology': result.methodology,
                'created_at': result.created_at.isoformat(),
                'date': result.created_at.strftime('%d.%m.%Y'),
                'scores': {},
                'dominant_category': 'Не определено',
                'recommendation': result.recommendation
            })
    
    # Создаем CSV-подобный формат
    csv_lines = [
        'ID теста;Методика;Дата;Доминирующая категория;Рекомендация;Баллы'
    ]
    
    for record in export_data:
        scores_str = ';'.join([f"{k}:{v}" for k, v in record['scores'].items()])
        line = f"{record['test_id']};{record['methodology']};{record['date']};{record['dominant_category']};{record['recommendation']};{scores_str}"
        csv_lines.append(line)
    
    csv_content = '\n'.join(csv_lines)
    
    from flask import Response
    return Response(
        csv_content,
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename=progress_export_{current_user.username}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'}
    )

@progress_bp.route('/progress/compare/<int:result1_id>/<int:result2_id>')
@login_required
def compare_results(result1_id, result2_id):
    """Сравнение двух результатов тестов"""
    result1 = TestResult.query.filter_by(id=result1_id, user_id=current_user.id).first_or_404()
    result2 = TestResult.query.filter_by(id=result2_id, user_id=current_user.id).first_or_404()
    
    try:
        results1_dict = json.loads(result1.results) if result1.results else {}
        results2_dict = json.loads(result2.results) if result2.results else {}
        
        scores1 = results1_dict.get('scores', {})
        scores2 = results2_dict.get('scores', {})
        
        comparison_data = {
            'result1': {
                'id': result1.id,
                'methodology': result1.methodology,
                'date': result1.created_at.strftime('%d.%m.%Y'),
                'scores': scores1,
                'dominant_category': results1_dict.get('dominant_category', 'Не определено')
            },
            'result2': {
                'id': result2.id,
                'methodology': result2.methodology,
                'date': result2.created_at.strftime('%d.%m.%Y'),
                'scores': scores2,
                'dominant_category': results2_dict.get('dominant_category', 'Не определено')
            },
            'changes': {}
        }
        
        # Рассчитываем изменения
        all_categories = set(scores1.keys()) | set(scores2.keys())
        for category in all_categories:
            score1 = scores1.get(category, 0)
            score2 = scores2.get(category, 0)
            change = score2 - score1
            comparison_data['changes'][category] = {
                'previous': score1,
                'current': score2,
                'change': change,
                'improvement': change > 0,
                'deterioration': change < 0
            }
        
    except Exception as e:
        comparison_data = {
            'result1': {
                'id': result1.id,
                'methodology': result1.methodology,
                'date': result1.created_at.strftime('%d.%m.%Y'),
                'scores': {},
                'dominant_category': 'Ошибка при чтении данных'
            },
            'result2': {
                'id': result2.id,
                'methodology': result2.methodology,
                'date': result2.created_at.strftime('%d.%m.%Y'),
                'scores': {},
                'dominant_category': 'Ошибка при чтении данных'
            },
            'changes': {},
            'error': str(e)
        }
    
    return render_template('progress/compare.html', comparison_data=comparison_data)

@progress_bp.route('/progress/api/data')
@login_required
def api_progress_data():
    """API для получения данных прогресса в формате JSON"""
    test_results = TestResult.query.filter_by(user_id=current_user.id).order_by(
        TestResult.created_at.asc()
    ).all()
    
    data = []
    for result in test_results:
        try:
            results_dict = json.loads(result.results) if result.results else {}
            scores = results_dict.get('scores', {})
            
            data.append({
                'id': result.id,
                'methodology': result.methodology,
                'timestamp': result.created_at.timestamp(),
                'date': result.created_at.strftime('%d.%m.%Y'),
                'scores': scores,
                'dominant_category': results_dict.get('dominant_category', 'Не определено')
            })
        except:
            data.append({
                'id': result.id,
                'methodology': result.methodology,
                'timestamp': result.created_at.timestamp(),
                'date': result.created_at.strftime('%d.%m.%Y'),
                'scores': {},
                'dominant_category': 'Не определено'
            })
    
    return jsonify(data)