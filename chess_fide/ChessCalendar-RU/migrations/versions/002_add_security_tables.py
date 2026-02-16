"""
Добавление таблиц для безопасности и аудита

Revision ID: 002_add_security_tables
Revises: 001_add_indexes
Create Date: 2024-02-16
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers
revision = '002_add_security_tables'
down_revision = '001_add_indexes'
branch_labels = None
depends_on = None


def upgrade():
    """Создание таблиц безопасности"""
    
    # Таблица audit_log
    op.create_table(
        'audit_log',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('action', sa.String(length=50), nullable=False),
        sa.Column('resource', sa.String(length=50), nullable=False),
        sa.Column('resource_id', sa.Integer(), nullable=True),
        sa.Column('details', sa.JSON(), nullable=True),
        sa.Column('ip_address', sa.String(length=45), nullable=True),
        sa.Column('user_agent', sa.String(length=255), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Индексы для audit_log
    op.create_index('ix_audit_log_user_id', 'audit_log', ['user_id'])
    op.create_index('ix_audit_log_action', 'audit_log', ['action'])
    op.create_index('ix_audit_log_resource', 'audit_log', ['resource'])
    op.create_index('ix_audit_log_resource_id', 'audit_log', ['resource_id'])
    op.create_index('ix_audit_log_timestamp', 'audit_log', ['timestamp'])
    
    # Составной индекс для частых запросов
    op.create_index(
        'ix_audit_log_user_timestamp',
        'audit_log',
        ['user_id', 'timestamp']
    )
    
    op.create_index(
        'ix_audit_log_resource_lookup',
        'audit_log',
        ['resource', 'resource_id', 'timestamp']
    )
    
    # Таблица login_attempt
    op.create_table(
        'login_attempt',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=80), nullable=False),
        sa.Column('ip_address', sa.String(length=45), nullable=False),
        sa.Column('success', sa.Boolean(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('user_agent', sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Индексы для login_attempt
    op.create_index('ix_login_attempt_username', 'login_attempt', ['username'])
    op.create_index('ix_login_attempt_ip_address', 'login_attempt', ['ip_address'])
    op.create_index('ix_login_attempt_success', 'login_attempt', ['success'])
    op.create_index('ix_login_attempt_timestamp', 'login_attempt', ['timestamp'])
    
    # Составной индекс для проверки брутфорса
    op.create_index(
        'ix_login_attempt_bruteforce',
        'login_attempt',
        ['username', 'ip_address', 'success', 'timestamp']
    )
    
    # Таблица two_factor_secret
    op.create_table(
        'two_factor_secret',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('secret', sa.String(length=255), nullable=False),
        sa.Column('enabled', sa.Boolean(), nullable=False),
        sa.Column('backup_codes', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('last_used', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )
    
    # Индексы для two_factor_secret
    op.create_index('ix_two_factor_secret_user_id', 'two_factor_secret', ['user_id'], unique=True)
    op.create_index('ix_two_factor_secret_enabled', 'two_factor_secret', ['enabled'])
    
    # Добавляем поля в таблицу user для 2FA
    op.add_column('user', sa.Column('two_factor_enabled', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('user', sa.Column('failed_login_attempts', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('user', sa.Column('locked_until', sa.DateTime(), nullable=True))
    op.add_column('user', sa.Column('password_changed_at', sa.DateTime(), nullable=True))
    op.add_column('user', sa.Column('require_password_change', sa.Boolean(), nullable=False, server_default='false'))
    
    # Индексы для новых полей user
    op.create_index('ix_user_two_factor_enabled', 'user', ['two_factor_enabled'])
    op.create_index('ix_user_locked_until', 'user', ['locked_until'])


def downgrade():
    """Удаление таблиц безопасности"""
    
    # Удаляем индексы и поля из user
    op.drop_index('ix_user_locked_until', table_name='user')
    op.drop_index('ix_user_two_factor_enabled', table_name='user')
    
    op.drop_column('user', 'require_password_change')
    op.drop_column('user', 'password_changed_at')
    op.drop_column('user', 'locked_until')
    op.drop_column('user', 'failed_login_attempts')
    op.drop_column('user', 'two_factor_enabled')
    
    # Удаляем таблицу two_factor_secret
    op.drop_index('ix_two_factor_secret_enabled', table_name='two_factor_secret')
    op.drop_index('ix_two_factor_secret_user_id', table_name='two_factor_secret')
    op.drop_table('two_factor_secret')
    
    # Удаляем таблицу login_attempt
    op.drop_index('ix_login_attempt_bruteforce', table_name='login_attempt')
    op.drop_index('ix_login_attempt_timestamp', table_name='login_attempt')
    op.drop_index('ix_login_attempt_success', table_name='login_attempt')
    op.drop_index('ix_login_attempt_ip_address', table_name='login_attempt')
    op.drop_index('ix_login_attempt_username', table_name='login_attempt')
    op.drop_table('login_attempt')
    
    # Удаляем таблицу audit_log
    op.drop_index('ix_audit_log_resource_lookup', table_name='audit_log')
    op.drop_index('ix_audit_log_user_timestamp', table_name='audit_log')
    op.drop_index('ix_audit_log_timestamp', table_name='audit_log')
    op.drop_index('ix_audit_log_resource_id', table_name='audit_log')
    op.drop_index('ix_audit_log_resource', table_name='audit_log')
    op.drop_index('ix_audit_log_action', table_name='audit_log')
    op.drop_index('ix_audit_log_user_id', table_name='audit_log')
    op.drop_table('audit_log')
