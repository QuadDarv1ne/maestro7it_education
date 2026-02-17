"""
Tournament Repository
Централизованное управление запросами к турнирам
"""
from typing import List, Optional, Dict, Any
from datetime import date, datetime, timedelta
from sqlalchemy import and_, or_, func
from app import db
from app.models.tournament import Tournament
from app.models.favorite import FavoriteTournament


class TournamentRepository:
    """Репозиторий для работы с турнирами"""
    
    @staticmethod
    def get_by_id(tournament_id: int) -> Optional[Tournament]:
        """Получить турнир по ID"""
        return Tournament.query.get(tournament_id)
    
    @staticmethod
    def get_by_fide_id(fide_id: str) -> Optional[Tournament]:
        """Получить турнир по FIDE ID"""
        return Tournament.query.filter_by(fide_id=fide_id).first()
    
    @staticmethod
    def get_by_name_and_date(name: str, start_date: date) -> Optional[Tournament]:
        """Получить турнир по названию и дате начала"""
        return Tournament.query.filter_by(
            name=name,
            start_date=start_date
        ).first()
    
    @staticmethod
    def get_all(limit: Optional[int] = None, offset: int = 0) -> List[Tournament]:
        """Получить все турниры"""
        query = Tournament.query.order_by(Tournament.start_date.desc())
        if limit:
            query = query.limit(limit).offset(offset)
        return query.all()
    
    @staticmethod
    def get_upcoming(limit: Optional[int] = None) -> List[Tournament]:
        """Получить предстоящие турниры"""
        query = Tournament.query.filter(
            Tournament.start_date >= date.today(),
            Tournament.status.in_(['Scheduled', 'Registration Open'])
        ).order_by(Tournament.start_date)
        
        if limit:
            query = query.limit(limit)
        
        return query.all()
    
    @staticmethod
    def get_ongoing() -> List[Tournament]:
        """Получить текущие турниры"""
        return Tournament.query.filter_by(status='Ongoing').all()
    
    @staticmethod
    def get_completed(limit: Optional[int] = None) -> List[Tournament]:
        """Получить завершенные турниры"""
        query = Tournament.query.filter_by(status='Completed').order_by(
            Tournament.end_date.desc()
        )
        
        if limit:
            query = query.limit(limit)
        
        return query.all()
    
    @staticmethod
    def get_by_status(status: str, limit: Optional[int] = None) -> List[Tournament]:
        """Получить турниры по статусу"""
        query = Tournament.query.filter_by(status=status)
        
        if limit:
            query = query.limit(limit)
        
        return query.all()
    
    @staticmethod
    def get_by_category(category: str, limit: Optional[int] = None) -> List[Tournament]:
        """Получить турниры по категории"""
        query = Tournament.query.filter_by(category=category)
        
        if limit:
            query = query.limit(limit)
        
        return query.all()
    
    @staticmethod
    def get_by_location(location: str, limit: Optional[int] = None) -> List[Tournament]:
        """Получить турниры по локации"""
        query = Tournament.query.filter(
            Tournament.location.ilike(f'%{location}%')
        )
        
        if limit:
            query = query.limit(limit)
        
        return query.all()
    
    @staticmethod
    def get_by_date_range(start_date: date, end_date: date) -> List[Tournament]:
        """Получить турниры в диапазоне дат"""
        return Tournament.query.filter(
            Tournament.start_date >= start_date,
            Tournament.start_date <= end_date
        ).order_by(Tournament.start_date).all()
    
    @staticmethod
    def get_with_location(limit: Optional[int] = 100) -> List[Tournament]:
        """Получить турниры с указанной локацией (для карты)"""
        query = Tournament.query.filter(
            Tournament.location.isnot(None)
        )
        
        if limit:
            query = query.limit(limit)
        
        return query.all()
    
    @staticmethod
    def search(
        query_text: Optional[str] = None,
        category: Optional[str] = None,
        status: Optional[str] = None,
        location: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[Tournament]:
        """Поиск турниров с фильтрами"""
        query = Tournament.query
        
        # Текстовый поиск
        if query_text:
            search_filter = or_(
                Tournament.name.ilike(f'%{query_text}%'),
                Tournament.location.ilike(f'%{query_text}%'),
                Tournament.organizer.ilike(f'%{query_text}%')
            )
            query = query.filter(search_filter)
        
        # Фильтры
        if category:
            query = query.filter_by(category=category)
        
        if status:
            query = query.filter_by(status=status)
        
        if location:
            query = query.filter(Tournament.location.ilike(f'%{location}%'))
        
        if start_date:
            query = query.filter(Tournament.start_date >= start_date)
        
        if end_date:
            query = query.filter(Tournament.start_date <= end_date)
        
        # Сортировка и пагинация
        query = query.order_by(Tournament.start_date.desc())
        
        if limit:
            query = query.limit(limit).offset(offset)
        
        return query.all()
    
    @staticmethod
    def get_similar(tournament: Tournament, limit: int = 5) -> List[Tournament]:
        """Получить похожие турниры"""
        similar = Tournament.query.filter(
            Tournament.id != tournament.id,
            Tournament.category == tournament.category,
            Tournament.location.ilike(f'%{tournament.location}%')
        ).limit(limit).all()
        
        # Если недостаточно, добавляем по категории
        if len(similar) < limit:
            exclude_ids = [t.id for t in similar] + [tournament.id]
            additional = Tournament.query.filter(
                Tournament.id.notin_(exclude_ids),
                Tournament.category == tournament.category
            ).limit(limit - len(similar)).all()
            similar.extend(additional)
        
        return similar
    
    @staticmethod
    def count_all() -> int:
        """Подсчитать все турниры"""
        return Tournament.query.count()
    
    @staticmethod
    def count_by_status(status: str) -> int:
        """Подсчитать турниры по статусу"""
        return Tournament.query.filter_by(status=status).count()
    
    @staticmethod
    def count_by_category(category: str) -> int:
        """Подсчитать турниры по категории"""
        return Tournament.query.filter_by(category=category).count()
    
    @staticmethod
    def get_statistics() -> Dict[str, Any]:
        """Получить статистику по турнирам"""
        total = Tournament.query.count()
        scheduled = Tournament.query.filter_by(status='Scheduled').count()
        ongoing = Tournament.query.filter_by(status='Ongoing').count()
        completed = Tournament.query.filter_by(status='Completed').count()
        
        # Статистика по категориям
        categories = db.session.query(
            Tournament.category,
            func.count(Tournament.id).label('count')
        ).group_by(Tournament.category).all()
        
        category_stats = {cat: count for cat, count in categories}
        
        return {
            'total': total,
            'scheduled': scheduled,
            'ongoing': ongoing,
            'completed': completed,
            'by_category': category_stats
        }
    
    @staticmethod
    def create(tournament_data: Dict[str, Any]) -> Tournament:
        """Создать новый турнир"""
        tournament = Tournament(**tournament_data)
        db.session.add(tournament)
        db.session.commit()
        return tournament
    
    @staticmethod
    def update(tournament: Tournament, data: Dict[str, Any]) -> Tournament:
        """Обновить турнир"""
        for key, value in data.items():
            if hasattr(tournament, key):
                setattr(tournament, key, value)
        
        db.session.commit()
        return tournament
    
    @staticmethod
    def delete(tournament: Tournament) -> bool:
        """Удалить турнир"""
        try:
            db.session.delete(tournament)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False


class FavoriteRepository:
    """Репозиторий для работы с избранными турнирами"""
    
    @staticmethod
    def is_favorite(user_id: int, tournament_id: int) -> bool:
        """Проверить, в избранном ли турнир"""
        return FavoriteTournament.query.filter_by(
            user_id=user_id,
            tournament_id=tournament_id
        ).first() is not None
    
    @staticmethod
    def get_favorite(user_id: int, tournament_id: int) -> Optional[FavoriteTournament]:
        """Получить запись избранного"""
        return FavoriteTournament.query.filter_by(
            user_id=user_id,
            tournament_id=tournament_id
        ).first()
    
    @staticmethod
    def get_user_favorites(user_id: int) -> List[FavoriteTournament]:
        """Получить все избранные турниры пользователя"""
        return FavoriteTournament.query.filter_by(user_id=user_id).all()
    
    @staticmethod
    def get_user_favorite_tournaments(user_id: int) -> List[Tournament]:
        """Получить турниры из избранного пользователя"""
        favorites = FavoriteTournament.query.filter_by(user_id=user_id).all()
        return [fav.tournament for fav in favorites if fav.tournament]
    
    @staticmethod
    def count_favorites(tournament_id: int) -> int:
        """Подсчитать количество добавлений в избранное"""
        return FavoriteTournament.query.filter_by(
            tournament_id=tournament_id
        ).count()
    
    @staticmethod
    def count_user_favorites(user_id: int) -> int:
        """Подсчитать количество избранных у пользователя"""
        return FavoriteTournament.query.filter_by(user_id=user_id).count()
    
    @staticmethod
    def add_favorite(user_id: int, tournament_id: int) -> Optional[FavoriteTournament]:
        """Добавить турнир в избранное"""
        # Проверяем, не добавлен ли уже
        existing = FavoriteRepository.get_favorite(user_id, tournament_id)
        if existing:
            return existing
        
        favorite = FavoriteTournament(
            user_id=user_id,
            tournament_id=tournament_id
        )
        db.session.add(favorite)
        db.session.commit()
        return favorite
    
    @staticmethod
    def remove_favorite(user_id: int, tournament_id: int) -> bool:
        """Удалить турнир из избранного"""
        favorite = FavoriteRepository.get_favorite(user_id, tournament_id)
        if not favorite:
            return False
        
        try:
            db.session.delete(favorite)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False
    
    @staticmethod
    def toggle_favorite(user_id: int, tournament_id: int) -> tuple[bool, str]:
        """Переключить статус избранного"""
        if FavoriteRepository.is_favorite(user_id, tournament_id):
            success = FavoriteRepository.remove_favorite(user_id, tournament_id)
            return success, 'removed' if success else 'error'
        else:
            favorite = FavoriteRepository.add_favorite(user_id, tournament_id)
            return favorite is not None, 'added' if favorite else 'error'
