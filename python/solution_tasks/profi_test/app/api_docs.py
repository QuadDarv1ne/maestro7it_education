"""
API Documentation and Swagger UI Integration
"""
from flask import Blueprint, jsonify, render_template
from flask_restx import Api, Resource, Namespace
import json

# Create blueprint for API documentation
api_docs_bp = Blueprint('api_docs', __name__, url_prefix='/api/docs')

# Инициализация Flask-RESTX API
api = Api(
    None,  # Will be initialized later
    version='1.0',
    title='Profi Test API Documentation',
    description='Система профориентации Maestro7IT - API Documentation',
    doc='/swagger/',
    prefix='/api'
)

# Create namespaces
test_ns = Namespace('test', description='Тестирование API')
user_ns = Namespace('user', description='Пользовательские API')
career_ns = Namespace('career', description='Карьерное развитие API')
analytics_ns = Namespace('analytics', description='Аналитика API')

# Register namespaces
api.add_namespace(test_ns)
api.add_namespace(user_ns)
api.add_namespace(career_ns)
api.add_namespace(analytics_ns)

# Test API Models
test_question_model = api.model('TestQuestion', {
    'id': {'type': 'integer', 'description': 'ID вопроса'},
    'methodology': {'type': 'string', 'description': 'Методика (klimov/holland)'},
    'question_number': {'type': 'integer', 'description': 'Номер вопроса'},
    'text': {'type': 'string', 'description': 'Текст вопроса'},
    'category': {'type': 'string', 'description': 'Категория профессиональной сферы'}
})

test_result_model = api.model('TestResult', {
    'id': {'type': 'integer', 'description': 'ID результата'},
    'methodology': {'type': 'string', 'description': 'Методика'},
    'dominant_category': {'type': 'string', 'description': 'Доминирующая категория'},
    'scores': {'type': 'object', 'description': 'Баллы по категориям'},
    'recommendation': {'type': 'string', 'description': 'Персональная рекомендация'},
    'created_at': {'type': 'string', 'format': 'date-time', 'description': 'Дата создания'}
})

# User API Models
user_model = api.model('User', {
    'id': {'type': 'integer', 'description': 'ID пользователя'},
    'username': {'type': 'string', 'description': 'Имя пользователя'},
    'email': {'type': 'string', 'description': 'Email пользователя'},
    'created_at': {'type': 'string', 'format': 'date-time', 'description': 'Дата регистрации'}
})

# Career API Models
career_goal_model = api.model('CareerGoal', {
    'id': {'type': 'integer', 'description': 'ID цели'},
    'title': {'type': 'string', 'description': 'Название цели'},
    'description': {'type': 'string', 'description': 'Описание'},
    'target_date': {'type': 'string', 'format': 'date', 'description': 'Планируемая дата'},
    'current_status': {'type': 'string', 'description': 'Статус (planning/in_progress/achieved/paused)'},
    'priority': {'type': 'integer', 'description': 'Приоритет (1-5)'}
})

# Analytics API Models
analytics_model = api.model('Analytics', {
    'total_users': {'type': 'integer', 'description': 'Общее количество пользователей'},
    'total_tests': {'type': 'integer', 'description': 'Общее количество тестов'},
    'methodology_distribution': {'type': 'object', 'description': 'Распределение по методикам'},
    'category_distribution': {'type': 'object', 'description': 'Распределение по категориям'}
})

@test_ns.route('/questions/<string:methodology>')
class TestQuestions(Resource):
    @api.doc('get_test_questions')
    @api.param('methodology', 'Методика тестирования (klimov или holland)')
    @api.response(200, 'Success', [test_question_model])
    @api.response(400, 'Invalid methodology')
    def get(self, methodology):
        """Получить вопросы для тестирования по методике"""
        valid_methodologies = ['klimov', 'holland']
        if methodology not in valid_methodologies:
            return {'error': f'Invalid methodology. Use: {", ".join(valid_methodologies)}'}, 400
        
        # Return sample data structure
        return {
            'methodology': methodology,
            'total_questions': 40 if methodology == 'klimov' else 36,
            'questions': [
                {
                    'id': 1,
                    'question_number': 1,
                    'text': 'Пример вопроса',
                    'category': 'человек-техника' if methodology == 'klimov' else 'Реалистический'
                }
            ]
        }

@test_ns.route('/submit')
class SubmitTest(Resource):
    @api.doc('submit_test')
    @api.expect(api.model('TestSubmission', {
        'methodology': {'type': 'string', 'required': True},
        'answers': {'type': 'object', 'required': True}
    }))
    @api.response(200, 'Success', test_result_model)
    @api.response(400, 'Validation Error')
    def post(self):
        """Отправить результаты теста"""
        return {
            'id': 1,
            'methodology': 'klimov',
            'dominant_category': 'человек-техника',
            'scores': {'человек-техника': 85, 'человек-человек': 70},
            'recommendation': 'Рекомендуем рассмотреть технические специальности',
            'created_at': '2024-01-01T10:00:00Z'
        }

@user_ns.route('/<int:user_id>')
class UserDetail(Resource):
    @api.doc('get_user')
    @api.param('user_id', 'ID пользователя')
    @api.response(200, 'Success', user_model)
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Получить информацию о пользователе"""
        return {
            'id': user_id,
            'username': 'testuser',
            'email': 'test@example.com',
            'created_at': '2024-01-01T10:00:00Z'
        }

@career_ns.route('/goals')
class CareerGoals(Resource):
    @api.doc('get_career_goals')
    @api.response(200, 'Success', [career_goal_model])
    def get(self):
        """Получить карьерные цели пользователя"""
        return [
            {
                'id': 1,
                'title': 'Стать программистом',
                'description': 'Развить навыки программирования',
                'target_date': '2025-12-31',
                'current_status': 'in_progress',
                'priority': 5
            }
        ]

@analytics_ns.route('/overview')
class AnalyticsOverview(Resource):
    @api.doc('get_analytics')
    @api.response(200, 'Success', analytics_model)
    def get(self):
        """Получить аналитику системы"""
        return {
            'total_users': 1250,
            'total_tests': 2100,
            'methodology_distribution': {
                'klimov': 1200,
                'holland': 900
            },
            'category_distribution': {
                'человек-техника': 350,
                'человек-человек': 280,
                'человек-природа': 180
            }
        }

@api_docs_bp.route('/')
def api_documentation():
    """Страница документации API"""
    return render_template('api_docs/index.html')

@api_docs_bp.route('/swagger')
def swagger_ui():
    """Swagger UI для API документации"""
    return render_template('api_docs/swagger.html')

def init_api_docs(app):
    """Инициализация документации API с Flask приложением"""
    api.init_app(app)
    app.register_blueprint(api_docs_bp)