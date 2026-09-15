"""
Миграция для добавления таблиц тегов и комментариев
"""
from alembic import op
import sqlalchemy as sa


def upgrade():
    """Добавление таблиц для тегов и комментариев"""
    
    # Таблица тегов
    op.create_table(
        'tag',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('slug', sa.String(length=60), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('color', sa.String(length=7), nullable=True),
        sa.Column('usage_count', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
        sa.UniqueConstraint('slug')
    )
    op.create_index(op.f('ix_tag_slug'), 'tag', ['slug'], unique=True)
    op.create_index(op.f('ix_tag_name'), 'tag', ['name'], unique=True)
    op.create_index(op.f('ix_tag_usage'), 'tag', ['usage_count'], unique=False, postgresql_using='btree')
    
    # Таблица связей тегов с турнирами
    op.create_table(
        'tag_tournament',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tag_id', sa.Integer(), nullable=False),
        sa.Column('tournament_id', sa.Integer(), nullable=False),
        sa.Column('added_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['tag_id'], ['tag.id']),
        sa.ForeignKeyConstraint(['tournament_id'], ['tournament.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('tag_id', 'tournament_id', name='uq_tag_tournament')
    )
    op.create_index(op.f('ix_tag_tournament_tag_id'), 'tag_tournament', ['tag_id'], unique=False)
    op.create_index(op.f('ix_tag_tournament_tournament_id'), 'tag_tournament', ['tournament_id'], unique=False)
    op.create_index('idx_tournament_tags', 'tag_tournament', ['tournament_id', 'tag_id'], unique=False)
    
    # Таблица комментариев
    op.create_table(
        'tournament_comment',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tournament_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('parent_id', sa.Integer(), nullable=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('is_deleted', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['parent_id'], ['tournament_comment.id']),
        sa.ForeignKeyConstraint(['tournament_id'], ['tournament.id']),
        sa.ForeignKeyConstraint(['user_id'], ['user.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tournament_comment_tournament_id'), 'tournament_comment', ['tournament_id'], unique=False)
    op.create_index(op.f('ix_tournament_comment_user_id'), 'tournament_comment', ['user_id'], unique=False)
    op.create_index(op.f('ix_tournament_comment_parent_id'), 'tournament_comment', ['parent_id'], unique=False)
    op.create_index('idx_tournament_created', 'tournament_comment', ['tournament_id', 'created_at'], unique=False)
    op.create_index('idx_user_created', 'tournament_comment', ['user_id', 'created_at'], unique=False)


def downgrade():
    """Удаление таблиц тегов и комментариев"""
    op.drop_table('tournament_comment')
    op.drop_table('tag_tournament')
    op.drop_table('tag')
