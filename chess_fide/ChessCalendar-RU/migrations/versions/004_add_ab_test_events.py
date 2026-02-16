"""Add AB test events table

Revision ID: 004
Revises: 003
Create Date: 2026-02-16

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade():
    """Create ab_test_events table"""
    op.create_table(
        'ab_test_events',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('test_name', sa.String(length=100), nullable=False),
        sa.Column('user_id', sa.String(length=100), nullable=False),
        sa.Column('variant', sa.String(length=50), nullable=False),
        sa.Column('event', sa.String(length=100), nullable=False),
        sa.Column('value', sa.Float(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.Column('user_agent', sa.String(length=500), nullable=True),
        sa.Column('ip_address', sa.String(length=50), nullable=True),
        sa.Column('session_id', sa.String(length=100), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for better query performance
    op.create_index('ix_ab_test_events_test_name', 'ab_test_events', ['test_name'])
    op.create_index('ix_ab_test_events_user_id', 'ab_test_events', ['user_id'])
    op.create_index('ix_ab_test_events_variant', 'ab_test_events', ['variant'])
    op.create_index('ix_ab_test_events_event', 'ab_test_events', ['event'])
    op.create_index('ix_ab_test_events_timestamp', 'ab_test_events', ['timestamp'])
    
    # Composite index for common queries
    op.create_index(
        'ix_ab_test_events_test_variant',
        'ab_test_events',
        ['test_name', 'variant', 'event']
    )


def downgrade():
    """Drop ab_test_events table"""
    op.drop_index('ix_ab_test_events_test_variant', table_name='ab_test_events')
    op.drop_index('ix_ab_test_events_timestamp', table_name='ab_test_events')
    op.drop_index('ix_ab_test_events_event', table_name='ab_test_events')
    op.drop_index('ix_ab_test_events_variant', table_name='ab_test_events')
    op.drop_index('ix_ab_test_events_user_id', table_name='ab_test_events')
    op.drop_index('ix_ab_test_events_test_name', table_name='ab_test_events')
    op.drop_table('ab_test_events')
