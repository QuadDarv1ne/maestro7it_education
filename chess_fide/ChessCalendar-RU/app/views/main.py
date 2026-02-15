from flask import Blueprint, render_template, jsonify, request
from app import db
from app.models.tournament import Tournament
from app.utils.fide_parser import FIDEParses
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Главная страница с календарем турниров"""
    tournaments = Tournament.query.order_by(Tournament.start_date).all()
    return render_template('index.html', tournaments=tournaments)

@main_bp.route('/api/tournaments')
def api_tournaments():
    """API для получения турниров"""
    tournaments = Tournament.query.all()
    return jsonify([t.to_dict() for t in tournaments])

@main_bp.route('/api/tournaments/<int:tournament_id>')
def api_tournament_detail(tournament_id):
    """API для получения деталей турнира"""
    tournament = Tournament.query.get_or_404(tournament_id)
    return jsonify(tournament.to_dict())

@main_bp.route('/update')
def update_tournaments():
    """Ручное обновление турниров из источников"""
    try:
        parser = FIDEParses()
        new_tournaments = parser.get_tournaments_russia(2026)
        
        updated_count = 0
        for tourney_data in new_tournaments:
            # Проверяем, существует ли турнир
            existing = Tournament.query.filter_by(
                name=tourney_data['name'],
                start_date=tourney_data['start_date']
            ).first()
            
            if not existing:
                tournament = Tournament(**tourney_data)
                db.session.add(tournament)
                updated_count += 1
        
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': f'Добавлено {updated_count} новых турниров'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@main_bp.route('/about')
def about():
    """Страница о проекте"""
    return render_template('about.html')