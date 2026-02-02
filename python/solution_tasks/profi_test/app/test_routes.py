from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import TestResult, TestQuestion
from app.forms import KlimovTestForm, HollandTestForm
import json
from datetime import datetime

test = Blueprint('test', __name__)

# Klimov's methodology questions
KLIMOV_QUESTIONS = [
    {
        'id': 1,
        'text': 'Предпочитаю работать с техникой и механизмами',
        'category': 'Человек-техника'
    },
    {
        'id': 2,
        'text': 'Люблю общаться с людьми и помогать им',
        'category': 'Человек-человек'
    },
    {
        'id': 3,
        'text': 'Интересуюсь природой и живыми организмами',
        'category': 'Человек-природа'
    },
    {
        'id': 4,
        'text': 'Предпочитаю работать с информацией и данными',
        'category': 'Человек-знаковая система'
    },
    {
        'id': 5,
        'text': 'Увлекаюсь творчеством и художественными занятиями',
        'category': 'Человек-художественный образ'
    },
    {
        'id': 6,
        'text': 'Люблю ремонтировать и настраивать оборудование',
        'category': 'Человек-техника'
    },
    {
        'id': 7,
        'text': 'Предпочитаю работать в команде',
        'category': 'Человек-человек'
    },
    {
        'id': 8,
        'text': 'Интересуюсь экологией и охраной окружающей среды',
        'category': 'Человек-природа'
    },
    {
        'id': 9,
        'text': 'Люблю анализировать информацию и решать логические задачи',
        'category': 'Человек-знаковая система'
    },
    {
        'id': 10,
        'text': 'Увлекаюсь дизайном и визуальным творчеством',
        'category': 'Человек-художественный образ'
    },
    {
        'id': 11,
        'text': 'Предпочитаю практическую работу с инструментами',
        'category': 'Человек-техника'
    },
    {
        'id': 12,
        'text': 'Люблю обучать и воспитывать других',
        'category': 'Человек-человек'
    },
    {
        'id': 13,
        'text': 'Интересуюсь биологией и медициной',
        'category': 'Человек-природа'
    },
    {
        'id': 14,
        'text': 'Предпочитаю работу с компьютерами и программами',
        'category': 'Человек-знаковая система'
    },
    {
        'id': 15,
        'text': 'Увлекаюсь музыкой и表演艺术',
        'category': 'Человек-художественный образ'
    },
    {
        'id': 16,
        'text': 'Люблю строить и проектировать',
        'category': 'Человек-техника'
    },
    {
        'id': 17,
        'text': 'Предпочитаю социальную работу',
        'category': 'Человек-человек'
    },
    {
        'id': 18,
        'text': 'Интересуюсь сельским хозяйством и животноводством',
        'category': 'Человек-природа'
    },
    {
        'id': 19,
        'text': 'Люблю работать с числами и статистикой',
        'category': 'Человек-знаковая система'
    },
    {
        'id': 20,
        'text': 'Увлекаюсь литературой и писательством',
        'category': 'Человек-художественный образ'
    }
]

@test.route('/methodology')
def methodology():
    """Page with methodology selection"""
    return render_template('test/methodology.html')

@test.route('/test/<method>')
@login_required
def take_test(method):
    """Route for taking the test"""
    if method == 'klimov':
        return render_template('test/klimov_test.html', questions=KLIMOV_QUESTIONS)
    elif method == 'holland':
        # TODO: Add Holland methodology questions
        flash('Методика Холланда пока недоступна', 'warning')
        return redirect(url_for('test.methodology'))
    else:
        flash('Неверная методика', 'error')
        return redirect(url_for('test.methodology'))

@test.route('/submit_test/<method>', methods=['POST'])
@login_required
def submit_test(method):
    """Route for submitting test results"""
    try:
        answers = request.get_json()
        
        if method == 'klimov':
            result = calculate_klimov_results(answers)
        else:
            return jsonify({'error': 'Неверная методика'}), 400
        
        # Save results to database
        test_result = TestResult(
            user_id=current_user.id,
            methodology=method,
            answers=json.dumps(answers),
            results=json.dumps(result),
            recommendation=generate_recommendation(result),
            completed_at=datetime.utcnow()
        )
        
        db.session.add(test_result)
        db.session.commit()
        
        return jsonify({'success': True, 'result_id': test_result.id})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@test.route('/results/<int:result_id>')
@login_required
def view_results(result_id):
    """Route for viewing test results"""
    result = TestResult.query.get_or_404(result_id)
    
    # Check if user has permission to view this result
    if result.user_id != current_user.id and not current_user.is_admin:
        flash('У вас нет доступа к этим результатам', 'error')
        return redirect(url_for('main.index'))
    
    answers = json.loads(result.answers) if result.answers else {}
    results = json.loads(result.results) if result.results else {}
    
    return render_template('test/results.html', 
                         result=result, 
                         answers=answers, 
                         results=results)

def calculate_klimov_results(answers):
    """Calculate results for Klimov's methodology"""
    scores = {
        'Человек-природа': 0,
        'Человек-техника': 0,
        'Человек-человек': 0,
        'Человек-знаковая система': 0,
        'Человек-художественный образ': 0
    }
    
    # Calculate scores based on answers
    for question_id, answer in answers.items():
        question = next((q for q in KLIMOV_QUESTIONS if q['id'] == int(question_id)), None)
        if question:
            scores[question['category']] += int(answer)
    
    # Find dominant category
    dominant_category = max(scores, key=scores.get)
    max_score = scores[dominant_category]
    
    return {
        'scores': scores,
        'dominant_category': dominant_category,
        'max_score': max_score,
        'total_questions': len(answers)
    }

def generate_recommendation(results):
    """Generate personalized recommendation based on results"""
    category = results['dominant_category']
    score = results['max_score']
    total = results['total_questions']
    percentage = (score / (total * 3)) * 100  # Assuming 3-point scale
    
    recommendations = {
        'Человек-природа': {
            'title': 'Естественные науки и экология',
            'description': 'Вам подойдут профессии, связанные с природой, биологией, экологией, сельским хозяйством.',
            'professions': ['Биолог', 'Эколог', 'Ветеринар', 'Агроном', 'Геолог']
        },
        'Человек-техника': {
            'title': 'Технические специальности',
            'description': 'Вам подойдут профессии, связанные с техникой, инженерией, строительством, IT.',
            'professions': ['Инженер', 'Программист', 'Строитель', 'Механик', 'Электрик']
        },
        'Человек-человек': {
            'title': 'Социальные профессии',
            'description': 'Вам подойдут профессии, связанные с работой с людьми, обучением, медициной.',
            'professions': ['Учитель', 'Врач', 'Психолог', 'Социальный работник', 'Менеджер']
        },
        'Человек-знаковая система': {
            'title': 'Информационные технологии и аналитика',
            'description': 'Вам подойдут профессии, связанные с обработкой информации, анализом данных, финансами.',
            'professions': ['Аналитик', 'Бухгалтер', 'Программист', 'Экономист', 'Юрист']
        },
        'Человек-художественный образ': {
            'title': 'Творческие профессии',
            'description': 'Вам подойдут профессии, связанные с искусством, дизайном, медиа, литературой.',
            'professions': ['Дизайнер', 'Художник', 'Журналист', 'Режиссер', 'Музыкант']
        }
    }
    
    if category in recommendations:
        rec = recommendations[category]
        return f"""
        <h3>{rec['title']}</h3>
        <p>{rec['description']}</p>
        <p><strong>Подходящие профессии:</strong> {', '.join(rec['professions'])}</p>
        <p><strong>Уровень соответствия:</strong> {percentage:.1f}%</p>
        """
    
    return "Рекомендация не доступна"