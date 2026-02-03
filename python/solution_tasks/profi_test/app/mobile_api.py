# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, TestResult, TestQuestion
import json

mobile_api = Blueprint('mobile_api', __name__)

@mobile_api.route('/auth/login', methods=['POST'])
def mobile_login():
    """API конечная точка для входа в мобильное приложение"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'success': False, 'message': 'Email и пароль обязательны'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if user and user.check_password(data['password']):
        login_user(user)
        return jsonify({
            'success': True,
            'token': user.id,  # В реальном приложении используйте JWT
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_admin': user.is_admin
            }
        })
    else:
        return jsonify({'success': False, 'message': 'Неверный email или пароль'}), 401

@mobile_api.route('/auth/register', methods=['POST'])
def mobile_register():
    """API endpoint for mobile app registration"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'success': False, 'message': 'Все поля обязательны'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'success': False, 'message': 'Пользователь с таким email уже существует'}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'success': False, 'message': 'Пользователь с таким именем уже существует'}), 400
    
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Регистрация успешна',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    })

@mobile_api.route('/test/methodologies')
@login_required
def get_methodologies():
    """Получает доступные методики тестирования"""
    methodologies = [
        {
            'id': 'klimov',
            'name': 'Методика Климова',
            'description': 'Определение профессиональной склонности',
            'questions_count': 20
        },
        {
            'id': 'holland',
            'name': 'Методика Холланда',
            'description': 'Профессиональные типы личности',
            'questions_count': 6
        }
    ]
    
    return jsonify({'success': True, 'methodologies': methodologies})

@mobile_api.route('/test/questions/<methodology>')
@login_required
def get_questions(methodology):
    """Получает вопросы для конкретной методики"""
    questions = TestQuestion.query.filter_by(methodology=methodology).order_by(TestQuestion.question_number).all()
    
    if not questions:
        return jsonify({'success': False, 'message': 'Вопросы не найдены'}), 404
    
    questions_data = []
    for question in questions:
        questions_data.append({
            'id': question.id,
            'number': question.question_number,
            'text': question.text,
            'category': question.category
        })
    
    return jsonify({
        'success': True,
        'questions': questions_data,
        'methodology': methodology
    })

@mobile_api.route('/test/submit', methods=['POST'])
@login_required
def submit_test():
    """Отправляет результаты теста"""
    data = request.get_json()
    
    if not data or not data.get('methodology') or not data.get('answers'):
        return jsonify({'success': False, 'message': 'Некорректные данные'}), 400
    
    # Calculate results (similar to web version)
    methodology = data['methodology']
    answers = data['answers']
    
    if methodology == 'klimov':
        results = calculate_klimov_results(answers)
    elif methodology == 'holland':
        results = calculate_holland_results(answers)
    else:
        return jsonify({'success': False, 'message': 'Неизвестная методика'}), 400
    
    # Save test result
    test_result = TestResult(
        user_id=current_user.id,
        methodology=methodology,
        answers=json.dumps(answers),
        results=json.dumps(results),
        recommendation=generate_recommendation(methodology, results)
    )
    
    db.session.add(test_result)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'result_id': test_result.id,
        'results': results,
        'recommendation': test_result.recommendation
    })

@mobile_api.route('/user/results')
@login_required
def get_user_results():
    """Получает результаты тестов пользователя"""
    results = TestResult.query.filter_by(user_id=current_user.id).order_by(
        TestResult.created_at.desc()
    ).all()
    
    results_data = []
    for result in results:
        try:
            results_dict = json.loads(result.results) if result.results else {}
            results_data.append({
                'id': result.id,
                'methodology': result.methodology,
                'created_at': result.created_at.isoformat(),
                'formatted_date': result.created_at.strftime('%d.%m.%Y'),
                'results': results_dict,
                'recommendation': result.recommendation
            })
        except:
            results_data.append({
                'id': result.id,
                'methodology': result.methodology,
                'created_at': result.created_at.isoformat(),
                'formatted_date': result.created_at.strftime('%d.%m.%Y'),
                'results': {},
                'recommendation': result.recommendation
            })
    
    return jsonify({
        'success': True,
        'results': results_data
    })

def calculate_klimov_results(answers):
    """Calculate results for Klimov methodology"""
    categories = {
        'Человек-природа': 0,
        'Человек-техника': 0,
        'Человек-человек': 0,
        'Человек-знаковая система': 0,
        'Человек-художественный образ': 0
    }
    
    # Mapping of questions to categories (simplified)
    question_mapping = {
        1: 'Человек-природа', 2: 'Человек-техника', 3: 'Человек-человек',
        4: 'Человек-знаковая система', 5: 'Человек-художественный образ',
        # ... add more mappings
    }
    
    for question_id, answer in answers.items():
        category = question_mapping.get(int(question_id))
        if category:
            categories[category] += answer
    
    dominant_category = max(categories, key=categories.get)
    
    return {
        'scores': categories,
        'dominant_category': dominant_category,
        'total_questions': len(answers)
    }

def calculate_holland_results(answers):
    """Calculate results for Holland methodology"""
    categories = {
        'Реалистический': 0,
        'Исследовательский': 0,
        'Артистический': 0,
        'Социальный': 0,
        'Предпринимательский': 0,
        'Конвенциональный': 0
    }
    
    # Mapping of questions to categories (simplified)
    question_mapping = {
        1: ['Реалистический', 'Исследовательский'],
        2: ['Артистический', 'Социальный'],
        3: ['Предпринимательский', 'Конвенциональный'],
        # ... add more mappings
    }
    
    for question_id, answer in answers.items():
        question_categories = question_mapping.get(int(question_id), [])
        if len(question_categories) == 2:
            categories[question_categories[0]] += answer
            categories[question_categories[1]] += (3 - answer)  # Inverse scoring
    
    # Get top 3 categories
    sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)
    top_categories = sorted_categories[:3]
    
    return {
        'scores': categories,
        'top_categories': top_categories,
        'total_questions': len(answers)
    }

def generate_recommendation(methodology, results):
    """Generate personalized recommendation"""
    if methodology == 'klimov':
        dominant = results['dominant_category']
        recommendations = {
            'Человек-природа': 'Вам подходят профессии, связанные с природой, биологией, экологией.',
            'Человек-техника': 'Вы склонны к техническим профессиям, инженерии, ремеслам.',
            'Человек-человек': 'Вам подходят профессии, связанные с работой с людьми.',
            'Человек-знаковая система': 'Вы склонны к аналитической и организационной работе.',
            'Человек-художественный образ': 'Вам подходят творческие профессии, искусство.'
        }
        return recommendations.get(dominant, 'Рекомендация будет доступна после анализа.')
    
    elif methodology == 'holland':
        top_cats = [cat[0] for cat in results['top_categories'][:2]]
        return f'Ваши основные профессиональные типы: {", ".join(top_cats)}. Рассмотрите профессии, сочетающие эти сферы.'
    
    return 'Персональная рекомендация будет доступна после анализа ваших результатов.'