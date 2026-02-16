"""Add security fields to user table

Revision ID: 003
Revises: 002_add_security_tables
Create Date: 2026-02-16 20:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002_add_security_tables'
branch_labels = None
depends_on = None


def upgrade():
    """Добавление дополнительных полей безопасности"""
    # Добавляем только поле two_factor_secret, так как остальные уже добавлены в миграции 002
    op.add_column('user', sa.Column('two_factor_secret', sa.String(length=64), nullable=True))
    
    # Создаем индекс для производительности
    op.create_index('idx_user_two_factor_secret', 'user', ['two_factor_secret'])


def downgrade():
    """Откат изменений"""
    op.drop_index('idx_user_two_factor_secret', table_name='user')
    op.drop_column('user', 'two_factor_secret')
