from flask import Blueprint
from flask_restx import Api, Resource, fields
from app.models.tournament import Tournament
from app.models.user import User
from app.models.rating import TournamentRating
from app.models.favorite import FavoriteTournament
from app.models.notification import Subscription
from app import db
from datetime import date

api_docs_bp = Blueprint('api_docs', __name__)

# Initialize Flask-RESTX API
api = Api(
    api_docs_bp,
    title='ChessCalendar API',
    version='1.0',
    description='API для шахматного календаря ChessCalendar-RU',
    doc='/docs/'  # Documentation will be available at /api/docs/
)

# Define namespaces
ns_tournaments = api.namespace('tournaments', description='Операции с турнирами')
ns_users = api.namespace('users', description='Операции с пользователями')
ns_ratings = api.namespace('ratings', description='Операции с оценками')
ns_favorites = api.namespace('favorites', description='Операции с избранными турнирами')

# Define models
tournament_model = api.model('Tournament', {
    'id': fields.Integer(required=True, description='ID турнира'),
    'name': fields.String(required=True, description='Название турнира', min_length=1, max_length=200),
    'start_date': fields.Date(required=True, description='Дата начала турнира (формат: YYYY-MM-DD)'),
    'end_date': fields.Date(required=True, description='Дата окончания турнира (формат: YYYY-MM-DD)'),
    'location': fields.String(required=True, description='Место проведения турнира', min_length=1, max_length=100),
    'category': fields.String(required=True, description='Категория турнира', enum=['FIDE', 'National', 'Regional', 'Youth', 'Women', 'Senior', 'Online']),
    'status': fields.String(required=True, description='Статус турнира', enum=['Scheduled', 'Ongoing', 'Completed', 'Cancelled']),
    'description': fields.String(description='Описание турнира', max_length=2000),
    'prize_fund': fields.String(description='Призовой фонд турнира', max_length=200),
    'organizer': fields.String(description='Организатор турнира', max_length=200),
    'fide_id': fields.String(description='FIDE ID турнира', max_length=20),
    'source_url': fields.Url(description='URL источника информации о турнире'),
    'created_at': fields.DateTime(description='Дата создания записи'),
    'updated_at': fields.DateTime(description='Дата последнего обновления'),
    'average_rating': fields.Float(description='Средняя оценка турнира'),
    'total_ratings': fields.Integer(description='Количество оценок турнира')
})

user_model = api.model('User', {
    'id': fields.Integer(required=True, description='ID пользователя'),
    'username': fields.String(required=True, description='Имя пользователя'),
    'email': fields.String(required=True, description='Email пользователя'),
    'is_admin': fields.Boolean(description='Является ли администратором'),
    'is_regular_user': fields.Boolean(description='Является ли обычным пользователем')
})

rating_model = api.model('Rating', {
    'id': fields.Integer(required=True, description='ID оценки'),
    'user_id': fields.Integer(required=True, description='ID пользователя'),
    'tournament_id': fields.Integer(required=True, description='ID турнира'),
    'rating': fields.Integer(required=True, description='Оценка (1-5)'),
    'review': fields.String(description='Отзыв')
})

favorite_model = api.model('Favorite', {
    'id': fields.Integer(required=True, description='ID избранного'),
    'user_id': fields.Integer(required=True, description='ID пользователя'),
    'tournament_id': fields.Integer(required=True, description='ID турнира'),
    'created_at': fields.DateTime(description='Дата добавления в избранное')
})

register_model = api.model('Register', {
    'username': fields.String(required=True, description='Имя пользователя'),
    'email': fields.String(required=True, description='Email пользователя'),
    'password': fields.String(required=True, description='Пароль пользователя')
})

login_model = api.model('Login', {
    'username': fields.String(required=True, description='Имя пользователя'),
    'password': fields.String(required=True, description='Пароль пользователя')
})

rate_model = api.model('Rate', {
    'user_id': fields.Integer(required=True, description='ID пользователя'),
    'rating': fields.Integer(required=True, description='Оценка (1-5)'),
    'review': fields.String(description='Отзыв')
})

@ns_tournaments.route('/')
class TournamentsList(Resource):
    @api.doc('list_tournaments')
    @api.param('page', 'Номер страницы', default=1)
    @api.param('per_page', 'Количество элементов на странице', default=20)
    @api.param('category', 'Категория турнира')
    @api.param('status', 'Статус турнира')
    @api.param('location', 'Место проведения')
    @api.param('search', 'Поисковый запрос')
    @api.marshal_list_with(tournament_model)
    def get(self):
        """Получить список турниров"""
        return [], 200
    
    @api.doc('create_tournament')
    @api.expect(tournament_model)
    @api.marshal_with(tournament_model, code=201)
    def post(self):
        """Создать новый турнир (только для администраторов)"""
        return {}, 201

@ns_tournaments.route('/<int:tournament_id>')
@api.param('tournament_id', 'ID турнира')
class TournamentResource(Resource):
    @api.doc('get_tournament')
    @api.marshal_with(tournament_model)
    def get(self, tournament_id):
        """Получить турнир по ID"""
        return {}, 200
    
    @api.doc('update_tournament')
    @api.expect(tournament_model)
    @api.marshal_with(tournament_model)
    def put(self, tournament_id):
        """Обновить турнир (только для администраторов)"""
        return {}, 200
    
    @api.doc('delete_tournament')
    def delete(self, tournament_id):
        """Удалить турнир (только для администраторов)"""
        return {}, 204

@ns_tournaments.route('/upcoming')
class UpcomingTournaments(Resource):
    @api.doc('get_upcoming_tournaments')
    @api.param('limit', 'Ограничение количества результатов', default=10)
    @api.marshal_list_with(tournament_model)
    def get(self):
        """Получить предстоящие турниры"""
        return [], 200

@ns_tournaments.route('/popular')
class PopularTournaments(Resource):
    @api.doc('get_popular_tournaments')
    @api.param('limit', 'Ограничение количества результатов', default=10)
    @api.marshal_list_with(tournament_model)
    def get(self):
        """Получить популярные турниры"""
        return [], 200

@ns_users.route('/register')
class UserRegistration(Resource):
    @api.doc('register_user')
    @api.expect(register_model)
    @api.marshal_with(user_model, code=201)
    def post(self):
        """Зарегистрировать нового пользователя"""
        return {}, 201

@ns_users.route('/login')
class UserLogin(Resource):
    @api.doc('login_user')
    @api.expect(login_model)
    def post(self):
        """Войти в систему"""
        return {}, 200

@ns_ratings.route('/<int:tournament_id>')
@api.param('tournament_id', 'ID турнира')
class TournamentRatings(Resource):
    @api.doc('get_tournament_ratings')
    @api.marshal_list_with(rating_model)
    def get(self, tournament_id):
        """Получить все оценки для турнира"""
        return [], 200
    
    @api.doc('add_tournament_rating')
    @api.expect(rate_model)
    @api.marshal_with(rating_model, code=201)
    def post(self, tournament_id):
        """Оценить турнир"""
        return {}, 201

@ns_favorites.route('/<int:tournament_id>')
@api.param('tournament_id', 'ID турнира')
class TournamentFavorites(Resource):
    @api.doc('add_favorite')
    @api.param('user_id', 'ID пользователя')
    @api.marshal_with(favorite_model, code=201)
    def post(self, tournament_id):
        """Добавить турнир в избранное"""
        return {}, 201
    
    @api.doc('remove_favorite')
    @api.param('user_id', 'ID пользователя')
    def delete(self, tournament_id):
        """Удалить турнир из избранного"""
        return {}, 200

@ns_users.route('/<int:user_id>/favorites')
@api.param('user_id', 'ID пользователя')
class UserFavorites(Resource):
    @api.doc('get_user_favorites')
    def get(self, user_id):
        """Получить избранные турниры пользователя"""
        return {}, 200

@api.route('/health')
class HealthCheck(Resource):
    def get(self):
        """Проверка работоспособности API"""
        return {
            'status': 'healthy',
            'service': 'ChessCalendar API',
            'timestamp': '2026-02-15T00:00:00Z'
        }

# Add a general documentation route
@api_docs_bp.route('/swagger/')
def swagger_ui():
    """Route to serve Swagger UI"""
    from flask import redirect
    return redirect('/api/docs/')