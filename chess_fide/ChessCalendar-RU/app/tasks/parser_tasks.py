"""
Celery задачи для парсинга турниров
"""
from app.celery_app import celery_app
from app import create_app, db
from app.models.tournament import Tournament
from app.utils.fide_parser import FIDEParser
from app.utils.cfr_parser import CFRParser
from app.utils.cache_manager import TournamentCacheManager
from app.utils.metrics import track_celery_task
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@celery_app.task(bind=True, max_retries=3, default_retry_delay=300)
@track_celery_task('parse_fide_tournaments')
def parse_fide_tournaments(self):
    """
    Асинхронный парсинг турниров с FIDE
    Повторяет попытку до 3 раз при ошибке
    """
    app = create_app()
    
    with app.app_context():
        try:
            logger.info("Starting FIDE tournament parsing")
            parser = FIDEParser()
            tournaments = parser.parse_tournaments()
            
            added_count = 0
            updated_count = 0
            
            for tournament_data in tournaments:
                # Проверяем существование турнира
                existing = Tournament.query.filter_by(
                    fide_id=tournament_data.get('fide_id')
                ).first()
                
                if existing:
                    # Обновляем существующий
                    for key, value in tournament_data.items():
                        if hasattr(existing, key):
                            setattr(existing, key, value)
                    existing.updated_at = datetime.utcnow()
                    updated_count += 1
                else:
                    # Создаем новый
                    tournament = Tournament(**tournament_data)
                    db.session.add(tournament)
                    added_count += 1
            
            db.session.commit()
            
            # Инвалидируем кэш
            TournamentCacheManager.invalidate_all()
            
            logger.info(f"FIDE parsing completed: {added_count} added, {updated_count} updated")
            
            return {
                'status': 'success',
                'added': added_count,
                'updated': updated_count,
                'total': len(tournaments)
            }
            
        except Exception as e:
            logger.error(f"FIDE parsing error: {e}")
            # Повторяем задачу
            raise self.retry(exc=e)

@celery_app.task(bind=True, max_retries=3, default_retry_delay=300)
@track_celery_task('parse_cfr_tournaments')
def parse_cfr_tournaments(self):
    """
    Асинхронный парсинг турниров с Российской Федерации Шахмат
    """
    app = create_app()
    
    with app.app_context():
        try:
            logger.info("Starting CFR tournament parsing")
            parser = CFRParser()
            tournaments = parser.parse_tournaments()
            
            added_count = 0
            updated_count = 0
            
            for tournament_data in tournaments:
                # Проверяем существование турнира
                existing = Tournament.query.filter_by(
                    name=tournament_data.get('name'),
                    start_date=tournament_data.get('start_date')
                ).first()
                
                if existing:
                    # Обновляем существующий
                    for key, value in tournament_data.items():
                        if hasattr(existing, key):
                            setattr(existing, key, value)
                    existing.updated_at = datetime.utcnow()
                    updated_count += 1
                else:
                    # Создаем новый
                    tournament = Tournament(**tournament_data)
                    db.session.add(tournament)
                    added_count += 1
            
            db.session.commit()
            
            # Инвалидируем кэш
            TournamentCacheManager.invalidate_all()
            
            logger.info(f"CFR parsing completed: {added_count} added, {updated_count} updated")
            
            return {
                'status': 'success',
                'added': added_count,
                'updated': updated_count,
                'total': len(tournaments)
            }
            
        except Exception as e:
            logger.error(f"CFR parsing error: {e}")
            raise self.retry(exc=e)

@celery_app.task
@track_celery_task('parse_tournament_details')
def parse_tournament_details(tournament_id):
    """
    Асинхронный парсинг детальной информации о турнире
    """
    app = create_app()
    
    with app.app_context():
        try:
            tournament = Tournament.query.get(tournament_id)
            if not tournament:
                logger.error(f"Tournament {tournament_id} not found")
                return {'status': 'error', 'message': 'Tournament not found'}
            
            # Парсим дополнительную информацию
            if tournament.source_url:
                # Здесь логика парсинга деталей
                logger.info(f"Parsing details for tournament {tournament_id}")
                
                # Инвалидируем кэш конкретного турнира
                TournamentCacheManager.invalidate_tournament(tournament_id)
            
            return {'status': 'success', 'tournament_id': tournament_id}
            
        except Exception as e:
            logger.error(f"Tournament details parsing error: {e}")
            return {'status': 'error', 'message': str(e)}

@celery_app.task
def batch_parse_tournaments(tournament_ids):
    """
    Пакетный парсинг нескольких турниров
    """
    results = []
    for tournament_id in tournament_ids:
        result = parse_tournament_details.delay(tournament_id)
        results.append(result.id)
    
    return {
        'status': 'queued',
        'task_ids': results,
        'count': len(results)
    }

@celery_app.task(bind=True, max_retries=5, default_retry_delay=60)
def validate_tournament_data(self, tournament_id):
    """
    Валидация данных турнира
    """
    app = create_app()
    
    with app.app_context():
        try:
            tournament = Tournament.query.get(tournament_id)
            if not tournament:
                return {'status': 'error', 'message': 'Tournament not found'}
            
            errors = tournament.validate()
            
            if errors:
                logger.warning(f"Tournament {tournament_id} validation errors: {errors}")
                return {
                    'status': 'invalid',
                    'tournament_id': tournament_id,
                    'errors': errors
                }
            
            return {
                'status': 'valid',
                'tournament_id': tournament_id
            }
            
        except Exception as e:
            logger.error(f"Validation error: {e}")
            raise self.retry(exc=e)
