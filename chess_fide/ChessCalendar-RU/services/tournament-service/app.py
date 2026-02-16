"""
Tournament Service - Микросервис для управления турнирами
"""
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from celery import Celery
import os

app = Flask(__name__)

# Конфигурация базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///tournaments.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Конфигурация Celery
app.config['CELERY_BROKER_URL'] = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
app.config['CELERY_RESULT_BACKEND'] = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

db = SQLAlchemy(app)

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

class Tournament(db.Model):
    __tablename__ = 'tournaments'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default='Scheduled')
    description = db.Column(db.Text)
    prize_fund = db.Column(db.String(200))
    organizer = db.Column(db.String(200))
    fide_id = db.Column(db.String(20), unique=True)
    source_url = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'location': self.location,
            'category': self.category,
            'status': self.status,
            'description': self.description,
            'prize_fund': self.prize_fund,
            'organizer': self.organizer,
            'fide_id': self.fide_id,
            'source_url': self.source_url,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# Создание таблиц
with app.app_context():
    db.create_all()

@app.route('/tournaments', methods=['GET'])
def get_tournaments():
    """Получить список турниров"""
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)
    
    query = Tournament.query
    
    # Фильтры
    category = request.args.get('category')
    if category:
        query = query.filter(Tournament.category == category)
    
    status = request.args.get('status')
    if status:
        query = query.filter(Tournament.status == status)
    
    location = request.args.get('location')
    if location:
        query = query.filter(Tournament.location.contains(location))
    
    # Пагинация
    tournaments = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'tournaments': [t.to_dict() for t in tournaments.items],
        'pagination': {
            'page': page,
            'pages': tournaments.pages,
            'per_page': per_page,
            'total': tournaments.total
        }
    })

@app.route('/tournaments', methods=['POST'])
def create_tournament():
    """Создать новый турнир"""
    data = request.get_json()
    
    tournament = Tournament(
        name=data['name'],
        start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date(),
        end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date(),
        location=data['location'],
        category=data['category'],
        status=data.get('status', 'Scheduled'),
        description=data.get('description'),
        prize_fund=data.get('prize_fund'),
        organizer=data.get('organizer'),
        fide_id=data.get('fide_id'),
        source_url=data.get('source_url')
    )
    
    db.session.add(tournament)
    db.session.commit()
    
    return jsonify(tournament.to_dict()), 201

@app.route('/tournaments/<int:tournament_id>', methods=['GET'])
def get_tournament(tournament_id):
    """Получить турнир по ID"""
    tournament = Tournament.query.get_or_404(tournament_id)
    return jsonify(tournament.to_dict())

@app.route('/tournaments/<int:tournament_id>', methods=['PUT'])
def update_tournament(tournament_id):
    """Обновить турнир"""
    tournament = Tournament.query.get_or_404(tournament_id)
    data = request.get_json()
    
    for field in ['name', 'location', 'category', 'status', 'description', 'prize_fund', 'organizer', 'fide_id', 'source_url']:
        if field in data:
            setattr(tournament, field, data[field])
    
    if 'start_date' in data:
        tournament.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
    
    if 'end_date' in data:
        tournament.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
    
    tournament.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify(tournament.to_dict())

@app.route('/tournaments/<int:tournament_id>', methods=['DELETE'])
def delete_tournament(tournament_id):
    """Удалить турнир"""
    tournament = Tournament.query.get_or_404(tournament_id)
    db.session.delete(tournament)
    db.session.commit()
    return '', 204

@app.route('/health', methods=['GET'])
def health_check():
    """Проверка состояния сервиса"""
    return jsonify({
        'status': 'healthy',
        'service': 'tournament-service',
        'timestamp': datetime.utcnow().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)