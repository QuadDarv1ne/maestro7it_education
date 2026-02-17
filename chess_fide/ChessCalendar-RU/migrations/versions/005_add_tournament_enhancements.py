"""Add tournament enhancements

Revision ID: 005
Revises: 004
Create Date: 2026-02-17 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '005'
down_revision = '004'
branch_labels = None
depends_on = None


def upgrade():
    # Добавляем новые поля в таблицу tournament
    op.add_column('tournament', sa.Column('view_count', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('tournament', sa.Column('participants_count', sa.Integer(), nullable=True))
    op.add_column('tournament', sa.Column('rating_type', sa.String(length=50), nullable=True))
    
    # Создаем индексы для новых полей
    op.create_index('idx_view_count', 'tournament', ['view_count'], unique=False)
    op.create_index('idx_participants_count', 'tournament', ['participants_count'], unique=False)
    op.create_index('idx_rating_type', 'tournament', ['rating_type'], unique=False)


def downgrade():
    # Удаляем индексы
    op.drop_index('idx_rating_type', table_name='tournament')
    op.drop_index('idx_participants_count', table_name='tournament')
    op.drop_index('idx_view_count', table_name='tournament')
    
    # Удаляем колонки
    op.drop_column('tournament', 'rating_type')
    op.drop_column('tournament', 'participants_count')
    op.drop_column('tournament', 'view_count')
