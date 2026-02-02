from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_login import login_required, current_user
from app import db
from app.models import TestResult, TestQuestion
from app.forms import KlimovTestForm, HollandTestForm
from app.pdf_generator import generate_pdf_report
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

# Holland's methodology questions (simplified version)
HOLLAND_QUESTIONS = [
    {
        'id': 1,
        'text': 'Мне нравится работать с техническими устройствами и механизмами',
        'category': 'Реалистический'
    },
    {
        'id': 2,
        'text': 'Я люблю изучать научные теории и проводить эксперименты',
        'category': 'Исследовательский'
    },
    {
        'id': 3,
        'text': 'Мне нравится создавать художественные произведения',
        'category': 'Артистический'
    },
    {
        'id': 4,
        'text': 'Я люблю помогать другим людям и заботиться о них',
        'category': 'Социальный'
    },
    {
        'id': 5,
        'text': 'Мне нравится управлять людьми и принимать деловые решения',
        'category': 'Предпринимательский'
    },
    {
        'id': 6,
        'text': 'Я люблю работать с документами и вести учет',
        'category': 'Конвенциональный'
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
        return render_template('test/holland_test.html', questions=HOLLAND_QUESTIONS)
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
        elif method == 'holland':
            result = calculate_holland_results(answers)
        else:
            return jsonify({'error': 'Неверная методика'}), 400
        
        # Save results to database
        test_result = TestResult(
            user_id=current_user.id,
            methodology=method,
            answers=json.dumps(answers),
            results=json.dumps(result),
            recommendation=generate_recommendation(result, method),
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

@test.route('/results/<int:result_id>/pdf')
@login_required
def export_pdf(result_id):
    """Route for exporting results to PDF"""
    result = TestResult.query.get_or_404(result_id)
    
    # Check if user has permission to view this result
    if result.user_id != current_user.id and not current_user.is_admin:
        flash('У вас нет доступа к этим результатам', 'error')
        return redirect(url_for('main.index'))
    
    results = json.loads(result.results) if result.results else {}
    
    # Generate PDF
    pdf_data = generate_pdf_report(current_user, result, results)
    
    # Create filename
    filename = f"profi_test_results_{result.methodology}_{result.created_at.strftime('%Y%m%d_%H%M')}.pdf"
    
    # Return PDF file
    return send_file(
        io.BytesIO(pdf_data),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=filename
    )

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

def calculate_holland_results(answers):
    """Calculate results for Holland's methodology"""
    scores = {
        'Реалистический': 0,
        'Исследовательский': 0,
        'Артистический': 0,
        'Социальный': 0,
        'Предпринимательский': 0,
        'Конвенциональный': 0
    }
    
    # Calculate scores based on answers
    for question_id, answer in answers.items():
        question = next((q for q in HOLLAND_QUESTIONS if q['id'] == int(question_id)), None)
        if question:
            scores[question['category']] += int(answer)
    
    # Sort categories by score
    sorted_categories = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    return {
        'scores': scores,
        'top_categories': sorted_categories[:3],  # Top 3 categories
        'total_questions': len(answers)
    }

def generate_recommendation(results, method):
    """Generate personalized recommendation based on results"""
    if method == 'klimov':
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
    
    elif method == 'holland':
        top_categories = results['top_categories']
        recommendations = {
            'Реалистический': {
                'title': 'Практические и технические профессии',
                'description': 'Вам подходят профессии, связанные с работой с техникой, инструментами, природой.',
                'professions': ['Механик', 'Строитель', 'Фермер', 'Водитель', 'Техник']
            },
            'Исследовательский': {
                'title': 'Научные и аналитические профессии',
                'description': 'Вам подходят профессии, связанные с наукой, исследованиями, анализом.',
                'professions': ['Ученый', 'Аналитик', 'Инженер-исследователь', 'Программист', 'Математик']
            },
            'Артистический': {
                'title': 'Творческие профессии',
                'description': 'Вам подходят профессии, связанные с искусством, творчеством, самовыражением.',
                'professions': ['Художник', 'Музыкант', 'Актер', 'Дизайнер', 'Писатель']
            },
            'Социальный': {
                'title': 'Педагогические и социальные профессии',
                'description': 'Вам подходят профессии, связанные с работой с людьми, обучением, помощью.',
                'professions': ['Учитель', 'Психолог', 'Социальный работник', 'Врач', 'Тренер']
            },
            'Предпринимательский': {
                'title': 'Бизнес и управление',
                'description': 'Вам подходят профессии, связанные с бизнесом, управлением, предпринимательством.',
                'professions': ['Предприниматель', 'Менеджер', 'Маркетолог', 'Консультант', 'Директор']
            },
            'Конвенциональный': {
                'title': 'Организационные и административные профессии',
                'description': 'Вам подходят профессии, связанные с документооборотом, учетом, организацией.',
                'professions': ['Бухгалтер', 'Секретарь', 'Администратор', 'Аналитик данных', 'Клерк']
            }
        }
        
        recommendation_text = "<h3>Ваши профессиональные типы (по Холланду):</h3><ul>"
        for category, score in top_categories:
            if category in recommendations:
                rec = recommendations[category]
                percentage = (score / (results['total_questions'] * 3)) * 100
                recommendation_text += f"""
                <li>
                    <strong>{category}</strong> ({percentage:.1f}%)
                    <p>{rec['description']}</p>
                    <p><em>Примеры профессий:</em> {', '.join(rec['professions'][:3])}</p>
                </li>
                """
        recommendation_text += "</ul>"
        return recommendation_text
    
    return "Рекомендация не доступна"