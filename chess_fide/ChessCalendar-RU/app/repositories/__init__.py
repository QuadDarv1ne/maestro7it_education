"""
Repositories Package
Централизованное управление доступом к данным
"""
from .tournament_repository import TournamentRepository, FavoriteRepository

__all__ = ['TournamentRepository', 'FavoriteRepository']
