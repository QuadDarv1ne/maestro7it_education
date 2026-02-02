from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Rating, TestResult, Comment

ratings = Blueprint('ratings', __name__)

@ratings.route('/rate/test/<int:test_id>', methods=['POST'])
@login_required
def rate_test(test_id):
    """Rate a test result (like/dislike)"""
    test_result = TestResult.query.get_or_404(test_id)
    
    # Check if user is trying to rate their own test
    if test_result.user_id == current_user.id:
        return jsonify({'error': 'Нельзя оценивать свои собственные результаты'}), 400
    
    rating_type = request.json.get('rating_type')
    if rating_type not in ['like', 'dislike']:
        return jsonify({'error': 'Неверный тип оценки. Используйте "like" или "dislike"'}), 400
    
    # Check if user already rated this test
    existing_rating = Rating.query.filter_by(
        user_id=current_user.id,
        test_result_id=test_id
    ).first()
    
    if existing_rating:
        if existing_rating.rating_type == rating_type:
            # User is un-rating (clicking same button again)
            db.session.delete(existing_rating)
            db.session.commit()
            return jsonify({
                'success': True,
                'action': 'unrated',
                'message': 'Оценка удалена',
                'likes': Rating.query.filter_by(test_result_id=test_id, rating_type='like').count(),
                'dislikes': Rating.query.filter_by(test_result_id=test_id, rating_type='dislike').count()
            })
        else:
            # User is changing rating
            existing_rating.rating_type = rating_type
            db.session.commit()
            return jsonify({
                'success': True,
                'action': 'changed',
                'message': 'Оценка изменена',
                'likes': Rating.query.filter_by(test_result_id=test_id, rating_type='like').count(),
                'dislikes': Rating.query.filter_by(test_result_id=test_id, rating_type='dislike').count()
            })
    else:
        # Create new rating
        rating = Rating(
            user_id=current_user.id,
            test_result_id=test_id,
            rating_type=rating_type
        )
        db.session.add(rating)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'action': 'rated',
            'message': 'Результат оценен',
            'likes': Rating.query.filter_by(test_result_id=test_id, rating_type='like').count(),
            'dislikes': Rating.query.filter_by(test_result_id=test_id, rating_type='dislike').count()
        })

@ratings.route('/rate/comment/<int:comment_id>', methods=['POST'])
@login_required
def rate_comment(comment_id):
    """Rate a comment (like/dislike)"""
    comment = Comment.query.get_or_404(comment_id)
    
    # Check if user is trying to rate their own comment
    if comment.user_id == current_user.id:
        return jsonify({'error': 'Нельзя оценивать свои собственные комментарии'}), 400
    
    rating_type = request.json.get('rating_type')
    if rating_type not in ['like', 'dislike']:
        return jsonify({'error': 'Неверный тип оценки. Используйте "like" или "dislike"'}), 400
    
    # Check if user already rated this comment
    existing_rating = Rating.query.filter_by(
        user_id=current_user.id,
        comment_id=comment_id
    ).first()
    
    if existing_rating:
        if existing_rating.rating_type == rating_type:
            # User is un-rating (clicking same button again)
            db.session.delete(existing_rating)
            db.session.commit()
            return jsonify({
                'success': True,
                'action': 'unrated',
                'message': 'Оценка удалена',
                'likes': Rating.query.filter_by(comment_id=comment_id, rating_type='like').count(),
                'dislikes': Rating.query.filter_by(comment_id=comment_id, rating_type='dislike').count()
            })
        else:
            # User is changing rating
            existing_rating.rating_type = rating_type
            db.session.commit()
            return jsonify({
                'success': True,
                'action': 'changed',
                'message': 'Оценка изменена',
                'likes': Rating.query.filter_by(comment_id=comment_id, rating_type='like').count(),
                'dislikes': Rating.query.filter_by(comment_id=comment_id, rating_type='dislike').count()
            })
    else:
        # Create new rating
        rating = Rating(
            user_id=current_user.id,
            comment_id=comment_id,
            rating_type=rating_type
        )
        db.session.add(rating)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'action': 'rated',
            'message': 'Комментарий оценен',
            'likes': Rating.query.filter_by(comment_id=comment_id, rating_type='like').count(),
            'dislikes': Rating.query.filter_by(comment_id=comment_id, rating_type='dislike').count()
        })

@ratings.route('/test/<int:test_id>/rating_status')
@login_required
def test_rating_status(test_id):
    """Get current rating status for a test result"""
    rating = Rating.query.filter_by(
        user_id=current_user.id,
        test_result_id=test_id
    ).first()
    
    likes = Rating.query.filter_by(test_result_id=test_id, rating_type='like').count()
    dislikes = Rating.query.filter_by(test_result_id=test_id, rating_type='dislike').count()
    
    return jsonify({
        'current_rating': rating.rating_type if rating else None,
        'likes': likes,
        'dislikes': dislikes
    })

@ratings.route('/comment/<int:comment_id>/rating_status')
@login_required
def comment_rating_status(comment_id):
    """Get current rating status for a comment"""
    rating = Rating.query.filter_by(
        user_id=current_user.id,
        comment_id=comment_id
    ).first()
    
    likes = Rating.query.filter_by(comment_id=comment_id, rating_type='like').count()
    dislikes = Rating.query.filter_by(comment_id=comment_id, rating_type='dislike').count()
    
    return jsonify({
        'current_rating': rating.rating_type if rating else None,
        'likes': likes,
        'dislikes': dislikes
    })