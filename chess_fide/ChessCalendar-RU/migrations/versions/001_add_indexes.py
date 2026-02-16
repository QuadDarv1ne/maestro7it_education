"""
Добавление индексов для оптимизации запросов

Revision ID: 001_add_indexes
Revises: 
Create Date: 2024-02-16
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '001_add_indexes'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Создание индексов для оптимизации"""
    
    # Индексы для таблицы tournaments
    op.create_index(
        'ix_tournaments_start_date',
        'tournament',
        ['start_date'],
        unique=False
    )
    
    op.create_index(
        'ix_tournaments_end_date',
        'tournament',
        ['end_date'],
        unique=False
    )
    
    op.create_index(
        'ix_tournaments_category',
        'tournament',
        ['category'],
        unique=False
    )
    
    op.create_index(
        'ix_tournaments_status',
        'tournament',
        ['status'],
        unique=False
    )
    
    op.create_index(
        'ix_tournaments_location',
        'tournament',
        ['location'],
        unique=False
    )
    
    # Составной индекс для частых запросов
    op.create_index(
        'ix_tournaments_status_start_date',
        'tournament',
        ['status', 'start_date'],
        unique=False
    )
    
    op.create_index(
        'ix_tournaments_category_start_date',
        'tournament',
        ['category', 'start_date'],
        unique=False
    )
    
    # Полнотекстовый индекс для поиска (PostgreSQL)
    # Для SQLite будет пропущен
    try:
        op.execute("""
            CREATE INDEX IF NOT EXISTS ix_tournaments_name_trgm 
            ON tournament USING gin (name gin_trgm_ops)
        """)
        
        op.execute("""
            CREATE INDEX IF NOT EXISTS ix_tournaments_description_trgm 
            ON tournament USING gin (description gin_trgm_ops)
        """)
    except Exception:
        # SQLite не поддерживает GIN индексы
        pass
    
    # Индексы для таблицы users
    op.create_index(
        'ix_users_email',
        'user',
        ['email'],
        unique=True
    )
    
    op.create_index(
        'ix_users_username',
        'user',
        ['username'],
        unique=True
    )
    
    op.create_index(
        'ix_users_is_active',
        'user',
        ['is_active'],
        unique=False
    )
    
    op.create_index(
        'ix_users_created_at',
        'user',
        ['created_at'],
        unique=False
    )
    
    # Индексы для таблицы favorites
    op.create_index(
        'ix_favorites_user_id',
        'favorite',
        ['user_id'],
        unique=False
    )
    
    op.create_index(
        'ix_favorites_tournament_id',
        'favorite',
        ['tournament_id'],
        unique=False
    )
    
    # Уникальный составной индекс
    op.create_index(
        'ix_favorites_user_tournament',
        'favorite',
        ['user_id', 'tournament_id'],
        unique=True
    )
    
    # Индексы для таблицы ratings
    op.create_index(
        'ix_ratings_user_id',
        'rating',
        ['user_id'],
        unique=False
    )
    
    op.create_index(
        'ix_ratings_tournament_id',
        'rating',
        ['tournament_id'],
        unique=False
    )
    
    op.create_index(
        'ix_ratings_rating',
        'rating',
        ['rating'],
        unique=False
    )
    
    # Индексы для таблицы notifications
    op.create_index(
        'ix_notifications_user_id',
        'notification',
        ['user_id'],
        unique=False
    )
    
    op.create_index(
        'ix_notifications_is_read',
        'notification',
        ['is_read'],
        unique=False
    )
    
    op.create_index(
        'ix_notifications_created_at',
        'notification',
        ['created_at'],
        unique=False
    )
    
    # Составной индекс для непрочитанных уведомлений
    op.create_index(
        'ix_notifications_user_unread',
        'notification',
        ['user_id', 'is_read', 'created_at'],
        unique=False
    )
    
    # Индексы для таблицы tournament_subscriptions
    op.create_index(
        'ix_subscriptions_user_id',
        'tournament_subscription',
        ['user_id'],
        unique=False
    )
    
    op.create_index(
        'ix_subscriptions_tournament_id',
        'tournament_subscription',
        ['tournament_id'],
        unique=False
    )
    
    # Индексы для таблицы reports
    op.create_index(
        'ix_reports_user_id',
        'report',
        ['user_id'],
        unique=False
    )
    
    op.create_index(
        'ix_reports_status',
        'report',
        ['status'],
        unique=False
    )
    
    op.create_index(
        'ix_reports_created_at',
        'report',
        ['created_at'],
        unique=False
    )


def downgrade():
    """Удаление индексов"""
    
    # Tournaments
    op.drop_index('ix_tournaments_start_date', table_name='tournament')
    op.drop_index('ix_tournaments_end_date', table_name='tournament')
    op.drop_index('ix_tournaments_category', table_name='tournament')
    op.drop_index('ix_tournaments_status', table_name='tournament')
    op.drop_index('ix_tournaments_location', table_name='tournament')
    op.drop_index('ix_tournaments_status_start_date', table_name='tournament')
    op.drop_index('ix_tournaments_category_start_date', table_name='tournament')
    
    # PostgreSQL полнотекстовые индексы
    try:
        op.execute("DROP INDEX IF EXISTS ix_tournaments_name_trgm")
        op.execute("DROP INDEX IF EXISTS ix_tournaments_description_trgm")
    except Exception:
        pass
    
    # Users
    op.drop_index('ix_users_email', table_name='user')
    op.drop_index('ix_users_username', table_name='user')
    op.drop_index('ix_users_is_active', table_name='user')
    op.drop_index('ix_users_created_at', table_name='user')
    
    # Favorites
    op.drop_index('ix_favorites_user_id', table_name='favorite')
    op.drop_index('ix_favorites_tournament_id', table_name='favorite')
    op.drop_index('ix_favorites_user_tournament', table_name='favorite')
    
    # Ratings
    op.drop_index('ix_ratings_user_id', table_name='rating')
    op.drop_index('ix_ratings_tournament_id', table_name='rating')
    op.drop_index('ix_ratings_rating', table_name='rating')
    
    # Notifications
    op.drop_index('ix_notifications_user_id', table_name='notification')
    op.drop_index('ix_notifications_is_read', table_name='notification')
    op.drop_index('ix_notifications_created_at', table_name='notification')
    op.drop_index('ix_notifications_user_unread', table_name='notification')
    
    # Subscriptions
    op.drop_index('ix_subscriptions_user_id', table_name='tournament_subscription')
    op.drop_index('ix_subscriptions_tournament_id', table_name='tournament_subscription')
    
    # Reports
    op.drop_index('ix_reports_user_id', table_name='report')
    op.drop_index('ix_reports_status', table_name='report')
    op.drop_index('ix_reports_created_at', table_name='report')
