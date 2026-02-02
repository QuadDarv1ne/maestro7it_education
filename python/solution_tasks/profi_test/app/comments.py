from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Comment, TestResult
from datetime import datetime

comments = Blueprint('comments', __name__)

@comments.route('/test/<int:test_id>/comments')
@login_required
def test_comments(test_id):
    """View comments for a test result"""
    test_result = TestResult.query.get_or_404(test_id)
    
    # Check if user has permission to view this result
    if test_result.user_id != current_user.id and not current_user.is_admin:
        flash('У вас нет доступа к этим результатам', 'error')
        return redirect(url_for('main.index'))
    
    # Get comments for this test
    comments = Comment.query.filter_by(test_result_id=test_id).order_by(
        Comment.created_at.desc()
    ).all()
    
    return render_template('comments/list.html', test_result=test_result, comments=comments)

@comments.route('/test/<int:test_id>/comment', methods=['POST'])
@login_required
def add_comment(test_id):
    """Add a comment to a test result"""
    test_result = TestResult.query.get_or_404(test_id)
    
    # Check if user has permission to comment
    if test_result.user_id != current_user.id and not current_user.is_admin:
        return jsonify({'error': 'Нет доступа'}), 403
    
    content = request.form.get('content')
    
    if not content or len(content.strip()) < 3:
        return jsonify({'error': 'Комментарий должен содержать минимум 3 символа'}), 400
    
    # Create new comment
    comment = Comment(
        test_result_id=test_id,
        user_id=current_user.id,
        content=content.strip()
    )
    
    db.session.add(comment)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'comment': {
            'id': comment.id,
            'content': comment.content,
            'username': current_user.username,
            'created_at': comment.created_at.strftime('%d.%m.%Y %H:%M')
        }
    })

@comments.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    """Delete a comment"""
    comment = Comment.query.get_or_404(comment_id)
    
    # Check if user can delete this comment
    if comment.user_id != current_user.id and not current_user.is_admin:
        return jsonify({'error': 'Нет доступа'}), 403
    
    db.session.delete(comment)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Комментарий удален'})

@comments.route('/comment/<int:comment_id>/edit', methods=['POST'])
@login_required
def edit_comment(comment_id):
    """Edit a comment"""
    comment = Comment.query.get_or_404(comment_id)
    
    # Check if user can edit this comment
    if comment.user_id != current_user.id:
        return jsonify({'error': 'Нет доступа'}), 403
    
    content = request.form.get('content')
    
    if not content or len(content.strip()) < 3:
        return jsonify({'error': 'Комментарий должен содержать минимум 3 символа'}), 400
    
    comment.content = content.strip()
    comment.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'comment': {
            'id': comment.id,
            'content': comment.content,
            'updated_at': comment.updated_at.strftime('%d.%m.%Y %H:%M')
        }
    })