# -*- coding: utf-8 -*-
"""
Модуль расширенных отчетов для ПрофиТест
Предоставляет комплексные возможности отчетности с детальной аналитикой
"""
from datetime import datetime, timedelta
from app import db
from app.models import User, TestResult, CareerGoal, LearningPath, Notification
import json
from collections import defaultdict
import pandas as pd
from io import StringIO
import csv


class EnhancedReports:
    """
    Расширенные отчеты для системы ПрофиТест.
    Предоставляет комплексные аналитические отчеты и статистику пользователей.
    """
    def __init__(self):
        pass
    
    def generate_user_comprehensive_report(self, user_id):
        """
        Генерирует комплексный отчет для конкретного пользователя
        """
        try:
            user = User.query.get(user_id)
            if not user:
                return None
            
            # Get user's test results
            test_results = TestResult.query.filter_by(user_id=user_id).all()
            
            # Get user's career goals
            career_goals = CareerGoal.query.filter_by(user_id=user_id).all()
            
            # Get user's learning paths
            learning_paths = LearningPath.query.filter_by(user_id=user_id).all()
            
            # Get user's notifications
            notifications = Notification.query.filter_by(user_id=user_id).all()
            
            # Calculate various metrics
            total_tests = len(test_results)
            total_goals = len(career_goals)
            total_paths = len(learning_paths)
            total_notifications = len(notifications)
            
            # Calculate test methodology distribution
            methodology_counts = defaultdict(int)
            for result in test_results:
                methodology_counts[result.methodology] += 1
            
            # Calculate goal status distribution
            goal_statuses = defaultdict(int)
            for goal in career_goals:
                goal_statuses[goal.current_status] += 1
            
            # Calculate path status distribution
            path_statuses = defaultdict(int)
            for path in learning_paths:
                path_statuses[path.status] += 1
            
            # Calculate learning path completion rate
            completed_paths = len([p for p in learning_paths if p.status == 'completed'])
            completion_rate = (completed_paths / total_paths * 100) if total_paths > 0 else 0
            
            # Get latest test result for recommendations
            latest_test = None
            if test_results:
                latest_test = max(test_results, key=lambda x: x.created_at)
            
            # Analyze test results if available
            test_analysis = {}
            if latest_test and latest_test.results:
                try:
                    results = json.loads(latest_test.results)
                    test_analysis = results
                except json.JSONDecodeError:
                    pass
            
            report = {
                'user_info': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'created_at': user.created_at.isoformat(),
                    'is_admin': user.is_admin
                },
                'summary_metrics': {
                    'total_tests_completed': total_tests,
                    'total_career_goals': total_goals,
                    'total_learning_paths': total_paths,
                    'total_notifications': total_notifications,
                    'learning_path_completion_rate': round(completion_rate, 2),
                    'account_age_days': (datetime.utcnow() - user.created_at).days
                },
                'test_analysis': test_analysis,
                'methodology_distribution': dict(methodology_counts),
                'goal_status_distribution': dict(goal_statuses),
                'path_status_distribution': dict(path_statuses),
                'timeline': {
                    'first_test_date': min((tr.created_at for tr in test_results), default=None),
                    'last_test_date': max((tr.created_at for tr in test_results), default=None),
                    'first_goal_date': min((cg.created_at for cg in career_goals), default=None),
                    'last_goal_date': max((cg.created_at for cg in career_goals), default=None),
                    'first_path_date': min((lp.created_at for lp in learning_paths), default=None),
                    'last_path_date': max((lp.created_at for lp in learning_paths), default=None)
                },
                'recommendations': self._generate_user_recommendations(user_id, test_analysis, career_goals, learning_paths),
                'comparative_analysis': self._get_user_comparative_analysis(user_id)
            }
            
            return report
        except Exception as e:
            print(f"Error generating user comprehensive report: {str(e)}")
            return None
    
    def _generate_user_recommendations(self, user_id, test_analysis, career_goals, learning_paths):
        """
        Generate personalized recommendations for the user
        """
        recommendations = []
        
        # Based on test results
        if test_analysis:
            if 'dominant_category' in test_analysis:
                recommendations.append({
                    'type': 'category_based',
                    'priority': 'high',
                    'title': 'Focus on Dominant Category',
                    'description': f"Your dominant professional category is '{test_analysis['dominant_category']}'. Focus on developing skills in this area.",
                    'action_items': [
                        f"Research careers in {test_analysis['dominant_category']}",
                        f"Take additional assessments in {test_analysis['dominant_category']}",
                        f"Join communities related to {test_analysis['dominant_category']}"
                    ]
                })
            
            if 'scores' in test_analysis:
                # Find categories with high scores
                high_scoring_categories = [cat for cat, score in test_analysis['scores'].items() if score >= 7]
                if high_scoring_categories:
                    recommendations.append({
                        'type': 'high_score_focus',
                        'priority': 'medium',
                        'title': 'Leverage Your Strengths',
                        'description': f"You have high scores in: {', '.join(high_scoring_categories)}. Consider careers in these areas.",
                        'action_items': [f"Explore career options in {cat}" for cat in high_scoring_categories[:2]]
                    })
        
        # Based on career goals
        if not career_goals:
            recommendations.append({
                'type': 'goal_setting',
                'priority': 'high',
                'title': 'Set Career Goals',
                'description': 'You haven\'t set any career goals yet. Setting goals will help guide your learning journey.',
                'action_items': [
                    'Define your short-term career objectives',
                    'Set long-term career aspirations',
                    'Create SMART career goals'
                ]
            })
        else:
            active_goals = [g for g in career_goals if g.current_status in ['planning', 'in_progress']]
            if not active_goals:
                recommendations.append({
                    'type': 'goal_activation',
                    'priority': 'medium',
                    'title': 'Activate Your Goals',
                    'description': 'You have set career goals but none are currently active. Consider working on your goals.',
                    'action_items': [
                        'Review your existing goals',
                        'Choose which goals to prioritize',
                        'Create action plans for your goals'
                    ]
                })
        
        # Based on learning paths
        if not learning_paths:
            recommendations.append({
                'type': 'learning_path_creation',
                'priority': 'medium',
                'title': 'Create Learning Paths',
                'description': 'Create structured learning paths to achieve your career goals.',
                'action_items': [
                    'Identify skills needed for your desired career',
                    'Create a learning plan',
                    'Enroll in relevant courses'
                ]
            })
        else:
            in_progress_paths = [p for p in learning_paths if p.status == 'in_progress']
            if not in_progress_paths:
                recommendations.append({
                    'type': 'path_activation',
                    'priority': 'medium',
                    'title': 'Start Learning',
                    'description': 'You have created learning paths but none are in progress. Begin your learning journey.',
                    'action_items': [
                        'Select a learning path to start',
                        'Allocate time for learning',
                        'Track your progress regularly'
                    ]
                })
        
        return recommendations
    
    def _get_user_comparative_analysis(self, user_id):
        """
        Get comparative analysis against other users
        """
        try:
            user = User.query.get(user_id)
            if not user:
                return {}
            
            # Get all users' test results
            all_users_tests = db.session.query(
                TestResult.user_id,
                TestResult.methodology,
                TestResult.results
            ).all()
            
            # Calculate user's average scores
            user_avg_scores = {}
            user_tests = [t for t in all_users_tests if t.user_id == user_id]
            
            for test in user_tests:
                if test.results:
                    try:
                        results = json.loads(test.results)
                        if 'scores' in results:
                            for category, score in results['scores'].items():
                                if category not in user_avg_scores:
                                    user_avg_scores[category] = []
                                user_avg_scores[category].append(score)
                    except json.JSONDecodeError:
                        continue
            
            # Calculate averages for user
            user_averages = {}
            for category, scores in user_avg_scores.items():
                user_averages[category] = sum(scores) / len(scores) if scores else 0
            
            # Calculate overall averages for each category
            all_averages = defaultdict(list)
            for test in all_users_tests:
                if test.results:
                    try:
                        results = json.loads(test.results)
                        if 'scores' in results:
                            for category, score in results['scores'].items():
                                all_averages[category].append(score)
                    except json.JSONDecodeError:
                        continue
            
            overall_averages = {}
            for category, scores in all_averages.items():
                overall_averages[category] = sum(scores) / len(scores) if scores else 0
            
            # Compare user to overall averages
            comparison = {}
            for category, user_avg in user_averages.items():
                overall_avg = overall_averages.get(category, 0)
                comparison[category] = {
                    'user_average': round(user_avg, 2),
                    'overall_average': round(overall_avg, 2),
                    'difference': round(user_avg - overall_avg, 2),
                    'relative_performance': 'above' if user_avg > overall_avg else 'below' if user_avg < overall_avg else 'equal'
                }
            
            return {
                'category_comparison': comparison,
                'total_users_compared': len(set(t.user_id for t in all_users_tests)),
                'user_ranking_percentile': self._calculate_user_percentile(user_id, all_users_tests)
            }
        except Exception as e:
            print(f"Error in comparative analysis: {str(e)}")
            return {}
    
    def _calculate_user_percentile(self, user_id, all_users_tests):
        """
        Calculate user's percentile ranking compared to other users
        """
        try:
            # Calculate total scores for each user
            user_totals = defaultdict(float)
            user_counts = defaultdict(int)
            
            for test in all_users_tests:
                if test.results:
                    try:
                        results = json.loads(test.results)
                        if 'scores' in results:
                            total_score = sum(results['scores'].values())
                            user_totals[test.user_id] += total_score
                            user_counts[test.user_id] += 1
                    except json.JSONDecodeError:
                        continue
            
            # Calculate average total score per user
            user_averages = {uid: user_totals[uid] / user_counts[uid] for uid in user_totals}
            
            # Get current user's average
            current_user_avg = user_averages.get(user_id, 0)
            
            # Calculate percentile
            all_averages = list(user_averages.values())
            all_averages.sort()
            
            if not all_averages:
                return 50  # Middle percentile if no data
            
            # Find position of current user
            pos = 0
            for avg in all_averages:
                if avg <= current_user_avg:
                    pos += 1
                else:
                    break
            
            percentile = (pos / len(all_averages)) * 100
            return round(percentile, 2)
        except Exception as e:
            print(f"Error calculating percentile: {str(e)}")
            return 50
    
    def generate_system_wide_report(self):
        """
        Generate a system-wide report with aggregate statistics
        """
        try:
            # Get all users
            all_users = User.query.all()
            
            # Get all test results
            all_test_results = TestResult.query.all()
            
            # Get all career goals
            all_career_goals = CareerGoal.query.all()
            
            # Get all learning paths
            all_learning_paths = LearningPath.query.all()
            
            # Calculate system-wide metrics
            total_users = len(all_users)
            total_tests = len(all_test_results)
            total_goals = len(all_career_goals)
            total_paths = len(all_learning_paths)
            
            # Calculate active users (users who have taken tests)
            active_users = len(set(tr.user_id for tr in all_test_results))
            
            # Calculate test methodology distribution
            methodology_dist = defaultdict(int)
            for result in all_test_results:
                methodology_dist[result.methodology] += 1
            
            # Calculate goal status distribution
            goal_status_dist = defaultdict(int)
            for goal in all_career_goals:
                goal_status_dist[goal.current_status] += 1
            
            # Calculate path status distribution
            path_status_dist = defaultdict(int)
            for path in all_learning_paths:
                path_status_dist[path.status] += 1
            
            # Calculate completion rates
            completed_paths = len([p for p in all_learning_paths if p.status == 'completed'])
            path_completion_rate = (completed_paths / total_paths * 100) if total_paths > 0 else 0
            
            # Calculate user engagement metrics
            users_with_goals = len(set(g.user_id for g in all_career_goals))
            users_with_paths = len(set(p.user_id for p in all_learning_paths))
            
            # Calculate average values
            avg_tests_per_user = total_tests / total_users if total_users > 0 else 0
            avg_goals_per_user = total_goals / total_users if total_users > 0 else 0
            avg_paths_per_user = total_paths / total_users if total_users > 0 else 0
            
            # Get top categories from test results
            all_categories = defaultdict(float)
            category_counts = defaultdict(int)
            
            for result in all_test_results:
                if result.results:
                    try:
                        results = json.loads(result.results)
                        if 'scores' in results:
                            for category, score in results['scores'].items():
                                all_categories[category] += score
                                category_counts[category] += 1
                    except json.JSONDecodeError:
                        continue
            
            # Calculate average scores for each category
            avg_category_scores = {}
            for category in all_categories:
                avg_category_scores[category] = all_categories[category] / category_counts[category]
            
            # Sort categories by average score
            sorted_categories = sorted(avg_category_scores.items(), key=lambda x: x[1], reverse=True)
            
            report = {
                'timestamp': datetime.utcnow().isoformat(),
                'system_metrics': {
                    'total_users': total_users,
                    'total_tests': total_tests,
                    'total_goals': total_goals,
                    'total_paths': total_paths,
                    'active_users': active_users,
                    'user_engagement_rate': round((active_users / total_users * 100) if total_users > 0 else 0, 2)
                },
                'averages': {
                    'avg_tests_per_user': round(avg_tests_per_user, 2),
                    'avg_goals_per_user': round(avg_goals_per_user, 2),
                    'avg_paths_per_user': round(avg_paths_per_user, 2)
                },
                'distributions': {
                    'methodology_distribution': dict(methodology_dist),
                    'goal_status_distribution': dict(goal_status_dist),
                    'path_status_distribution': dict(path_status_dist)
                },
                'engagement_metrics': {
                    'users_with_goals_percentage': round((users_with_goals / total_users * 100) if total_users > 0 else 0, 2),
                    'users_with_paths_percentage': round((users_with_paths / total_users * 100) if total_users > 0 else 0, 2),
                    'path_completion_rate': round(path_completion_rate, 2)
                },
                'top_categories': sorted_categories[:10],  # Top 10 categories
                'recommendations': self._generate_system_recommendations(
                    total_users, active_users, path_completion_rate, avg_category_scores
                )
            }
            
            return report
        except Exception as e:
            print(f"Error generating system-wide report: {str(e)}")
            return {}
    
    def _generate_system_recommendations(self, total_users, active_users, path_completion_rate, avg_category_scores):
        """
        Generate system-wide recommendations
        """
        recommendations = []
        
        engagement_rate = (active_users / total_users * 100) if total_users > 0 else 0
        
        if engagement_rate < 50:
            recommendations.append({
                'type': 'engagement',
                'priority': 'high',
                'title': 'Low User Engagement',
                'description': f'Only {engagement_rate}% of users are active. Consider implementing engagement strategies.',
                'action_items': [
                    'Send targeted emails to inactive users',
                    'Create onboarding tutorials',
                    'Offer incentives for completing first test'
                ]
            })
        
        if path_completion_rate < 30:
            recommendations.append({
                'type': 'completion_rate',
                'priority': 'medium',
                'title': 'Low Learning Path Completion Rate',
                'description': f'Only {path_completion_rate}% of learning paths are completed. Consider improving path quality.',
                'action_items': [
                    'Analyze reasons for path abandonment',
                    'Shorten learning paths',
                    'Add milestones and rewards'
                ]
            })
        
        # Suggest popular categories for content creation
        if avg_category_scores:
            top_categories = sorted(avg_category_scores.items(), key=lambda x: x[1], reverse=True)[:3]
            recommendations.append({
                'type': 'content_strategy',
                'priority': 'medium',
                'title': 'Popular Categories Identified',
                'description': f'Top categories: {", ".join([cat[0] for cat in top_categories])}. Create more content in these areas.',
                'action_items': [f'Develop resources for {cat[0]} professionals' for cat in top_categories]
            })
        
        return recommendations
    
    def export_report_to_csv(self, report_data, report_type='user'):
        """
        Export report data to CSV format
        """
        try:
            if report_type == 'user':
                # Flatten user report for CSV
                flattened_data = []
                
                # Add user info
                user_info = report_data.get('user_info', {})
                summary_metrics = report_data.get('summary_metrics', {})
                
                row = {
                    'user_id': user_info.get('id'),
                    'username': user_info.get('username'),
                    'email': user_info.get('email'),
                    'created_at': user_info.get('created_at'),
                    'is_admin': user_info.get('is_admin'),
                    'total_tests_completed': summary_metrics.get('total_tests_completed'),
                    'total_career_goals': summary_metrics.get('total_career_goals'),
                    'total_learning_paths': summary_metrics.get('total_learning_paths'),
                    'learning_path_completion_rate': summary_metrics.get('learning_path_completion_rate'),
                    'account_age_days': summary_metrics.get('account_age_days')
                }
                
                flattened_data.append(row)
                
                # Convert to CSV
                output = StringIO()
                writer = csv.DictWriter(output, fieldnames=row.keys())
                writer.writeheader()
                writer.writerows(flattened_data)
                
                return output.getvalue()
            
            elif report_type == 'system':
                # Flatten system report for CSV
                flattened_data = []
                
                system_metrics = report_data.get('system_metrics', {})
                averages = report_data.get('averages', {})
                
                row = {
                    'timestamp': report_data.get('timestamp'),
                    'total_users': system_metrics.get('total_users'),
                    'total_tests': system_metrics.get('total_tests'),
                    'total_goals': system_metrics.get('total_goals'),
                    'total_paths': system_metrics.get('total_paths'),
                    'active_users': system_metrics.get('active_users'),
                    'user_engagement_rate': system_metrics.get('user_engagement_rate'),
                    'avg_tests_per_user': averages.get('avg_tests_per_user'),
                    'avg_goals_per_user': averages.get('avg_goals_per_user'),
                    'avg_paths_per_user': averages.get('avg_paths_per_user')
                }
                
                flattened_data.append(row)
                
                # Convert to CSV
                output = StringIO()
                writer = csv.DictWriter(output, fieldnames=row.keys())
                writer.writeheader()
                writer.writerows(flattened_data)
                
                return output.getvalue()
                
        except Exception as e:
            print(f"Error exporting report to CSV: {str(e)}")
            return None
    
    def generate_user_progress_report(self, user_id):
        """
        Generate a detailed progress report for a user
        """
        try:
            user = User.query.get(user_id)
            if not user:
                return None
            
            # Get all user data
            test_results = TestResult.query.filter_by(user_id=user_id).order_by(TestResult.created_at).all()
            career_goals = CareerGoal.query.filter_by(user_id=user_id).all()
            learning_paths = LearningPath.query.filter_by(user_id=user_id).all()
            
            # Calculate progress metrics
            progress_metrics = {
                'total_tests': len(test_results),
                'total_goals': len(career_goals),
                'total_paths': len(learning_paths),
                'completed_paths': len([p for p in learning_paths if p.status == 'completed']),
                'in_progress_goals': len([g for g in career_goals if g.current_status == 'in_progress']),
                'achieved_goals': len([g for g in career_goals if g.current_status == 'achieved'])
            }
            
            # Calculate progress over time
            progress_timeline = []
            for result in test_results:
                progress_timeline.append({
                    'date': result.created_at.isoformat(),
                    'type': 'test',
                    'methodology': result.methodology,
                    'id': result.id
                })
            
            for goal in career_goals:
                progress_timeline.append({
                    'date': goal.created_at.isoformat(),
                    'type': 'goal',
                    'status': goal.current_status,
                    'title': goal.title,
                    'id': goal.id
                })
            
            for path in learning_paths:
                progress_timeline.append({
                    'date': path.created_at.isoformat(),
                    'type': 'path',
                    'status': path.status,
                    'title': path.title,
                    'id': path.id
                })
            
            # Sort timeline by date
            progress_timeline.sort(key=lambda x: x['date'])
            
            # Calculate growth indicators
            if len(test_results) >= 2:
                first_result = test_results[0]
                last_result = test_results[-1]
                
                # Calculate if there's improvement in scores (simplified)
                initial_score_sum = 0
                final_score_sum = 0
                
                if first_result.results:
                    try:
                        initial_results = json.loads(first_result.results)
                        if 'scores' in initial_results:
                            initial_score_sum = sum(initial_results['scores'].values())
                    except json.JSONDecodeError:
                        pass
                
                if last_result.results:
                    try:
                        final_results = json.loads(last_result.results)
                        if 'scores' in final_results:
                            final_score_sum = sum(final_results['scores'].values())
                    except json.JSONDecodeError:
                        pass
                
                growth_indicator = 'positive' if final_score_sum > initial_score_sum else 'negative' if final_score_sum < initial_score_sum else 'neutral'
            else:
                growth_indicator = 'insufficient_data'
            
            report = {
                'user': {
                    'id': user.id,
                    'username': user.username
                },
                'progress_metrics': progress_metrics,
                'progress_timeline': progress_timeline,
                'growth_indicator': growth_indicator,
                'milestones': self._identify_user_milestones(test_results, career_goals, learning_paths),
                'development_trajectory': self._analyze_development_trajectory(test_results, career_goals, learning_paths)
            }
            
            return report
        except Exception as e:
            print(f"Error generating user progress report: {str(e)}")
            return None
    
    def _identify_user_milestones(self, test_results, career_goals, learning_paths):
        """
        Identify important milestones in user's journey
        """
        milestones = []
        
        if test_results:
            milestones.append({
                'date': test_results[0].created_at,
                'type': 'first_test',
                'description': 'Completed first professional test',
                'significance': 'high'
            })
            
            if len(test_results) >= 5:
                milestones.append({
                    'date': test_results[4].created_at,
                    'type': 'five_tests',
                    'description': 'Completed 5 professional tests',
                    'significance': 'medium'
                })
        
        if career_goals:
            milestones.append({
                'date': career_goals[0].created_at,
                'type': 'first_goal',
                'description': 'Created first career goal',
                'significance': 'high'
            })
        
        if learning_paths:
            milestones.append({
                'date': learning_paths[0].created_at,
                'type': 'first_path',
                'description': 'Created first learning path',
                'significance': 'medium'
            })
            
            completed_paths = [p for p in learning_paths if p.status == 'completed']
            if completed_paths:
                milestones.append({
                    'date': completed_paths[0].created_at,
                    'type': 'first_completion',
                    'description': 'Completed first learning path',
                    'significance': 'high'
                })
        
        # Sort milestones by date
        milestones.sort(key=lambda x: x['date'])
        return milestones
    
    def _analyze_development_trajectory(self, test_results, career_goals, learning_paths):
        """
        Analyze user's development trajectory
        """
        trajectory = {
            'stage': 'exploration',
            'characteristics': [],
            'next_steps': []
        }
        
        # Determine stage based on activity
        total_activities = len(test_results) + len(career_goals) + len(learning_paths)
        
        if total_activities < 3:
            trajectory['stage'] = 'initial_exploration'
            trajectory['characteristics'] = ['Just starting', 'Exploring options', 'Low activity level']
            trajectory['next_steps'] = ['Take more tests', 'Set career goals', 'Create learning paths']
        elif total_activities < 10:
            trajectory['stage'] = 'active_exploration'
            trajectory['characteristics'] = ['Moderate activity', 'Building foundation', 'Setting goals']
            trajectory['next_steps'] = ['Complete learning paths', 'Achieve first goals', 'Deepen specialization']
        elif total_activities < 20:
            trajectory['stage'] = 'focused_development'
            trajectory['characteristics'] = ['Consistent activity', 'Clear direction', 'Skill building']
            trajectory['next_steps'] = ['Advance to next level', 'Expand expertise', 'Achieve major goals']
        else:
            trajectory['stage'] = 'advanced_practice'
            trajectory['characteristics'] = ['High activity', 'Expertise building', 'Leadership potential']
            trajectory['next_steps'] = ['Mentor others', 'Share knowledge', 'Innovate solutions']
        
        return trajectory


# Global instance
enhanced_reports = EnhancedReports()