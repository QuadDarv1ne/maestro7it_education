"""
Advanced Analytics Module for Profi Test
Provides comprehensive analytics and insights for user behavior and test results
"""
from datetime import datetime, timedelta
from collections import defaultdict
import json
import plotly.graph_objs as go
import plotly.offline as pyo
from app import db
from app.models import User, TestResult, Notification, CareerGoal, LearningPath
import pandas as pd
import numpy as np
from sqlalchemy import func, extract


class AdvancedAnalytics:
    def __init__(self):
        self.data_cache = {}
    
    def get_user_engagement_stats(self):
        """
        Get comprehensive user engagement statistics
        """
        try:
            # Total users
            total_users = User.query.count()
            
            # Active users (users who have taken tests)
            active_users = db.session.query(func.count(func.distinct(TestResult.user_id))).scalar()
            
            # Users with recent activity (last 30 days)
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            recent_users = User.query.filter(User.created_at >= thirty_days_ago).count()
            
            # Users with notifications
            users_with_notifications = db.session.query(func.count(func.distinct(Notification.user_id))).scalar()
            
            # Users with career goals
            users_with_goals = db.session.query(func.count(func.distinct(CareerGoal.user_id))).scalar()
            
            # Users with learning paths
            users_with_paths = db.session.query(func.count(func.distinct(LearningPath.user_id))).scalar()
            
            stats = {
                'total_users': total_users,
                'active_users': active_users,
                'recent_users': recent_users,
                'users_with_notifications': users_with_notifications,
                'users_with_goals': users_with_goals,
                'users_with_paths': users_with_paths,
                'engagement_rate': round((active_users / total_users * 100) if total_users > 0 else 0, 2)
            }
            
            return stats
        except Exception as e:
            print(f"Error getting user engagement stats: {str(e)}")
            return {}
    
    def get_test_completion_statistics(self):
        """
        Get statistics about test completions
        """
        try:
            # Overall test statistics
            total_tests = TestResult.query.count()
            klimov_tests = TestResult.query.filter_by(methodology='klimov').count()
            holland_tests = TestResult.query.filter_by(methodology='holland').count()
            
            # Tests by month
            tests_by_month = db.session.query(
                extract('year', TestResult.created_at).label('year'),
                extract('month', TestResult.created_at).label('month'),
                func.count(TestResult.id)
            ).group_by(
                extract('year', TestResult.created_at),
                extract('month', TestResult.created_at)
            ).order_by(
                extract('year', TestResult.created_at),
                extract('month', TestResult.created_at)
            ).all()
            
            # Average time to complete tests (if completed_at is available)
            avg_completion_time = None  # Placeholder for future enhancement
            
            stats = {
                'total_tests': total_tests,
                'klimov_tests': klimov_tests,
                'holland_tests': holland_tests,
                'tests_by_month': [{'year': int(row[0]), 'month': int(row[1]), 'count': row[2]} for row in tests_by_month],
                'avg_completion_time': avg_completion_time
            }
            
            return stats
        except Exception as e:
            print(f"Error getting test completion stats: {str(e)}")
            return {}
    
    def get_popular_categories(self):
        """
        Get popular professional categories based on test results
        """
        try:
            # Get all test results
            all_results = TestResult.query.all()
            
            klimov_categories = defaultdict(int)
            holland_categories = defaultdict(int)
            
            for result in all_results:
                if result.results:
                    try:
                        results_dict = json.loads(result.results)
                        
                        if result.methodology == 'klimov' and 'scores' in results_dict:
                            for category, score in results_dict['scores'].items():
                                klimov_categories[category] += score
                        
                        elif result.methodology == 'holland' and 'scores' in results_dict:
                            for category, score in results_dict['scores'].items():
                                holland_categories[category] += score
                                
                    except json.JSONDecodeError:
                        continue
            
            # Normalize scores by dividing by number of tests in each methodology
            klimov_total_tests = TestResult.query.filter_by(methodology='klimov').count()
            holland_total_tests = TestResult.query.filter_by(methodology='holland').count()
            
            for category in klimov_categories:
                klimov_categories[category] = klimov_categories[category] / max(klimov_total_tests, 1)
                
            for category in holland_categories:
                holland_categories[category] = holland_categories[category] / max(holland_total_tests, 1)
            
            # Sort by popularity
            sorted_klimov = sorted(klimov_categories.items(), key=lambda x: x[1], reverse=True)
            sorted_holland = sorted(holland_categories.items(), key=lambda x: x[1], reverse=True)
            
            return {
                'klimov_popular': sorted_klimov[:10],  # Top 10
                'holland_popular': sorted_holland[:10]  # Top 10
            }
        except Exception as e:
            print(f"Error getting popular categories: {str(e)}")
            return {'klimov_popular': [], 'holland_popular': []}
    
    def get_career_goal_statistics(self):
        """
        Get statistics about career goals
        """
        try:
            # Total career goals
            total_goals = CareerGoal.query.count()
            
            # Goals by status
            goals_by_status = db.session.query(
                CareerGoal.current_status,
                func.count(CareerGoal.id)
            ).group_by(CareerGoal.current_status).all()
            
            # Goals by priority
            goals_by_priority = db.session.query(
                CareerGoal.priority,
                func.count(CareerGoal.id)
            ).group_by(CareerGoal.priority).all()
            
            # Goals by user (distribution)
            goals_per_user = db.session.query(
                func.count(CareerGoal.id)
            ).group_by(CareerGoal.user_id).all()
            
            # Calculate average goals per user
            avg_goals_per_user = sum([count[0] for count in goals_per_user]) / len(goals_per_user) if goals_per_user else 0
            
            stats = {
                'total_goals': total_goals,
                'goals_by_status': dict(goals_by_status),
                'goals_by_priority': dict(goals_by_priority),
                'avg_goals_per_user': round(avg_goals_per_user, 2),
                'status_distribution': {status: count for status, count in goals_by_status}
            }
            
            return stats
        except Exception as e:
            print(f"Error getting career goal stats: {str(e)}")
            return {}
    
    def get_learning_path_statistics(self):
        """
        Get statistics about learning paths
        """
        try:
            # Total learning paths
            total_paths = LearningPath.query.count()
            
            # Paths by status
            paths_by_status = db.session.query(
                LearningPath.status,
                func.count(LearningPath.id)
            ).group_by(LearningPath.status).all()
            
            # Paths by difficulty
            paths_by_difficulty = db.session.query(
                LearningPath.difficulty_level,
                func.count(LearningPath.id)
            ).group_by(LearningPath.difficulty_level).all()
            
            # Completion rate
            completed_paths = LearningPath.query.filter_by(status='completed').count()
            completion_rate = round((completed_paths / total_paths * 100) if total_paths > 0 else 0, 2)
            
            # Average duration
            avg_duration = db.session.query(
                func.avg(LearningPath.duration_weeks)
            ).filter(LearningPath.duration_weeks.isnot(None)).scalar()
            
            stats = {
                'total_paths': total_paths,
                'paths_by_status': dict(paths_by_status),
                'paths_by_difficulty': dict(paths_by_difficulty),
                'completion_rate': completion_rate,
                'avg_duration_weeks': round(avg_duration, 2) if avg_duration else 0,
                'completed_paths': completed_paths
            }
            
            return stats
        except Exception as e:
            print(f"Error getting learning path stats: {str(e)}")
            return {}
    
    def generate_engagement_chart(self):
        """
        Generate a chart showing user engagement over time
        """
        try:
            # Get daily user activity for the last 30 days
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            daily_activity = db.session.query(
                func.date(TestResult.created_at).label('date'),
                func.count(TestResult.id).label('test_count')
            ).filter(
                TestResult.created_at >= thirty_days_ago
            ).group_by(
                func.date(TestResult.created_at)
            ).order_by(
                func.date(TestResult.created_at)
            ).all()
            
            if not daily_activity:
                return None
            
            dates = [row.date for row in daily_activity]
            counts = [row.test_count for row in daily_activity]
            
            fig = go.Figure(data=go.Scatter(x=dates, y=counts, mode='lines+markers'))
            fig.update_layout(
                title='User Engagement Over Time (Last 30 Days)',
                xaxis_title='Date',
                yaxis_title='Number of Test Completions',
                template='plotly_white'
            )
            
            chart_html = pyo.plot(fig, output_type='div', include_plotlyjs=False)
            return chart_html
        except Exception as e:
            print(f"Error generating engagement chart: {str(e)}")
            return None
    
    def generate_category_comparison_chart(self):
        """
        Generate a chart comparing popular categories across methodologies
        """
        try:
            categories = self.get_popular_categories()
            
            klimov_cats = [cat[0] for cat in categories['klimov_popular'][:5]]
            klimov_scores = [cat[1] for cat in categories['klimov_popular'][:5]]
            
            holland_cats = [cat[0] for cat in categories['holland_popular'][:5]]
            holland_scores = [cat[1] for cat in categories['holland_popular'][:5]]
            
            fig = go.Figure(data=[
                go.Bar(name='Klimov Method', x=klimov_cats, y=klimov_scores),
                go.Bar(name='Holland Method', x=holland_cats, y=holland_scores)
            ])
            
            fig.update_layout(
                title='Popular Professional Categories Comparison',
                xaxis_title='Categories',
                yaxis_title='Average Score',
                barmode='group',
                template='plotly_white'
            )
            
            chart_html = pyo.plot(fig, output_type='div', include_plotlyjs=False)
            return chart_html
        except Exception as e:
            print(f"Error generating category comparison chart: {str(e)}")
            return None
    
    def generate_completion_rate_chart(self):
        """
        Generate a pie chart showing test completion rates
        """
        try:
            stats = self.get_test_completion_statistics()
            
            labels = ['Klimov Tests', 'Holland Tests']
            values = [stats['klimov_tests'], stats['holland_tests']]
            
            fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
            fig.update_layout(
                title='Distribution of Completed Tests',
                template='plotly_white'
            )
            
            chart_html = pyo.plot(fig, output_type='div', include_plotlyjs=False)
            return chart_html
        except Exception as e:
            print(f"Error generating completion rate chart: {str(e)}")
            return None
    
    def generate_comprehensive_report(self):
        """
        Generate a comprehensive analytics report
        """
        try:
            report = {
                'timestamp': datetime.utcnow(),
                'user_engagement': self.get_user_engagement_stats(),
                'test_statistics': self.get_test_completion_statistics(),
                'popular_categories': self.get_popular_categories(),
                'career_goals': self.get_career_goal_statistics(),
                'learning_paths': self.get_learning_path_statistics(),
                'charts': {
                    'engagement_chart': self.generate_engagement_chart(),
                    'category_comparison': self.generate_category_comparison_chart(),
                    'completion_rate': self.generate_completion_rate_chart()
                }
            }
            
            return report
        except Exception as e:
            print(f"Error generating comprehensive report: {str(e)}")
            return {}
    
    def export_to_csv(self, filename=None):
        """
        Export analytics data to CSV format
        """
        try:
            if not filename:
                filename = f"analytics_export_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"
            
            # Get comprehensive data
            report = self.generate_comprehensive_report()
            
            # Convert to DataFrame
            data = []
            
            # Add user engagement data
            engagement = report['user_engagement']
            for key, value in engagement.items():
                data.append(['User Engagement', key, value])
            
            # Add test statistics
            test_stats = report['test_statistics']
            for key, value in test_stats.items():
                if isinstance(value, list):
                    continue  # Skip complex objects for CSV
                data.append(['Test Statistics', key, value])
            
            # Add popular categories
            categories = report['popular_categories']
            for method, cats in categories.items():
                for cat_name, score in cats[:5]:  # Top 5
                    data.append(['Popular Categories', f'{method}_{cat_name}', score])
            
            df = pd.DataFrame(data, columns=['Category', 'Metric', 'Value'])
            df.to_csv(filename, index=False)
            
            return filename
        except Exception as e:
            print(f"Error exporting to CSV: {str(e)}")
            return None


# Global instance
advanced_analytics_instance = AdvancedAnalytics()