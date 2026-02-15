#!/usr/bin/env python
"""
Management script for ChessCalendar-RU application
Provides various administrative functions and maintenance tasks
"""

import os
import sys
import argparse
from datetime import datetime, timedelta

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.tournament import Tournament
from app.models.user import User
from app.models.notification import Notification, Subscription
from app.utils.backup import DatabaseBackupManager, DataExportManager
from app.utils.notifications import notification_service
from app.utils.fide_parser import FIDEParses
from app.utils.cfr_parser import CFRParser


def create_admin_user(username, email, password):
    """Create a new admin user"""
    app = create_app()
    
    with app.app_context():
        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            print(f"User {username} already exists!")
            return False
        
        # Create admin user
        admin = User(username=username, email=email, password=password, is_admin=True)
        db.session.add(admin)
        db.session.commit()
        
        print(f"Admin user '{username}' created successfully!")
        print(f"API Key: {admin.api_key}")
        return True


def backup_database():
    """Create a backup of the database"""
    app = create_app()
    
    with app.app_context():
        backup_manager = DatabaseBackupManager("chess_calendar.db")
        backup_path = backup_manager.create_compressed_backup()
        print(f"Database backup created: {backup_path}")
        return backup_path


def export_data(format_type='json'):
    """Export tournament data to specified format"""
    app = create_app()
    
    with app.app_context():
        export_manager = DataExportManager("chess_calendar.db")
        
        if format_type.lower() == 'json':
            output_path = f"tournaments_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            success = export_manager.export_tournaments_to_json(output_path)
        elif format_type.lower() == 'csv':
            output_path = f"tournaments_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            success = export_manager.export_tournaments_to_csv(output_path)
        else:
            print(f"Unsupported format: {format_type}")
            return False
        
        if success:
            print(f"Data exported successfully to: {output_path}")
            return output_path
        else:
            print("Failed to export data")
            return False


def clean_old_notifications(days=30):
    """Remove notifications older than specified days"""
    app = create_app()
    
    with app.app_context():
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        old_notifications = Notification.query.filter(Notification.created_at < cutoff_date).all()
        
        count = len(old_notifications)
        for notification in old_notifications:
            db.session.delete(notification)
        
        db.session.commit()
        print(f"Removed {count} old notifications (older than {days} days)")
        return count


def update_tournaments():
    """Manually update tournaments from all sources"""
    app = create_app()
    
    with app.app_context():
        from app.utils.updater import updater
        updater.update_all_sources()
        print("Tournament update completed")


def validate_tournaments():
    """Validate all tournament data"""
    app = create_app()
    
    with app.app_context():
        tournaments = Tournament.query.all()
        errors = []
        
        for tournament in tournaments:
            validation_errors = tournament.validate()
            if validation_errors:
                errors.append({
                    'tournament_id': tournament.id,
                    'tournament_name': tournament.name,
                    'errors': validation_errors
                })
        
        if errors:
            print(f"Found {len(errors)} tournaments with validation errors:")
            for error in errors:
                print(f"  Tournament {error['tournament_id']} ({error['tournament_name']}):")
                for err in error['errors']:
                    print(f"    - {err}")
        else:
            print("All tournaments passed validation!")
        
        return errors


def show_statistics():
    """Show application statistics"""
    app = create_app()
    
    with app.app_context():
        total_tournaments = Tournament.query.count()
        total_users = User.query.count()
        total_notifications = Notification.query.count()
        total_subscriptions = Subscription.query.count()
        
        print("Application Statistics:")
        print(f"  Total Tournaments: {total_tournaments}")
        print(f"  Total Users: {total_users}")
        print(f"  Total Notifications: {total_notifications}")
        print(f"  Total Subscriptions: {total_subscriptions}")
        
        # Show tournaments by category
        categories = db.session.query(Tournament.category, db.func.count(Tournament.id)).group_by(Tournament.category).all()
        print("\nTournaments by Category:")
        for cat, count in categories:
            print(f"  {cat}: {count}")


def main():
    parser = argparse.ArgumentParser(description='ChessCalendar-RU Management Script')
    parser.add_argument('--action', '-a', required=True,
                        choices=['create-admin', 'backup', 'export', 'clean-notifications', 
                                'update-tournaments', 'validate', 'stats'],
                        help='Action to perform')
    
    parser.add_argument('--username', help='Username for admin creation')
    parser.add_argument('--email', help='Email for admin creation')
    parser.add_argument('--password', help='Password for admin creation')
    parser.add_argument('--format', help='Format for export (json or csv)', default='json')
    parser.add_argument('--days', type=int, help='Number of days for cleaning old notifications', default=30)
    
    args = parser.parse_args()
    
    if args.action == 'create-admin':
        if not all([args.username, args.email, args.password]):
            print("Username, email, and password are required for admin creation")
            return
        create_admin_user(args.username, args.email, args.password)
    
    elif args.action == 'backup':
        backup_database()
    
    elif args.action == 'export':
        export_data(args.format)
    
    elif args.action == 'clean-notifications':
        clean_old_notifications(args.days)
    
    elif args.action == 'update-tournaments':
        update_tournaments()
    
    elif args.action == 'validate':
        validate_tournaments()
    
    elif args.action == 'stats':
        show_statistics()


if __name__ == '__main__':
    main()