from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app import db
from app.models.user import User
from app.models.tournament import Tournament
from app.models.forum import ForumThread, ForumPost
from app.utils.forum import ForumService
from app.utils.reporting import ReportingService

forum_bp = Blueprint('forum', __name__, url_prefix='/forum')


@forum_bp.route("/<int:tournament_id>")
def tournament_forum(tournament_id):
    """Show forum for a tournament"""
    tournament = Tournament.query.get_or_404(tournament_id)
    
    page = request.args.get("page", 1, type=int)
    sort_by = request.args.get("sort_by", "updated")
    
    forum_data = ForumService.get_threads_for_tournament(tournament_id, page=page, sort_by=sort_by)
    
    return render_template("forum/threads.html", 
                           tournament=tournament,
                           threads=forum_data["threads"],
                           pagination=forum_data["pagination"])


@forum_bp.route("/<int:tournament_id>/new-thread", methods=["GET", "POST"])
def create_thread(tournament_id):
    """Create a new thread in tournament forum"""
    if "user_id" not in session:
        flash("Пожалуйста, войдите в систему для создания темы", "warning")
        return redirect(url_for("user.login"))

    tournament = Tournament.query.get_or_404(tournament_id)
    user = User.query.get(session["user_id"])

    if not user or not user.is_regular_user:
        flash("Доступ запрещен", "error")
        return redirect(url_for("main.index"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()

        if not title or not content:
            flash("Заголовок и содержание темы обязательны", "error")
            return render_template("forum/create_thread.html", tournament=tournament)

        try:
            thread = ForumService.create_thread(tournament_id, title, user.id, content)
            flash("Тема успешно создана!", "success")
            return redirect(url_for("forum.thread_detail", thread_id=thread.id))
        except ValueError as e:
            flash(str(e), "error")

    return render_template("forum/create_thread.html", tournament=tournament)


@forum_bp.route("/thread/<int:thread_id>")
def thread_detail(thread_id):
    """Show thread details and posts"""
    thread_data = ForumService.get_thread_with_posts(thread_id)

    if not thread_data:
        flash("Тема не найдена", "error")
        return redirect(url_for("main.index"))

    thread = thread_data["thread"]
    posts = thread_data["posts"]

    # Get current user for permission checks
    current_user = None
    if "user_id" in session:
        current_user = User.query.get(session["user_id"])

    return render_template("forum/thread_detail.html", 
                           thread=thread,
                           posts=posts,
                           current_user=current_user)


@forum_bp.route("/thread/<int:thread_id>/reply", methods=["POST"])
def reply_to_thread(thread_id):
    """Reply to a thread"""
    if "user_id" not in session:
        flash("Пожалуйста, войдите в систему для ответа", "warning")
        return redirect(url_for("user.login"))

    user = User.query.get(session["user_id"])
    if not user or not user.is_regular_user:
        flash("Доступ запрещен", "error")
        return redirect(url_for("main.index"))

    content = request.form.get("content", "").strip()
    if not content:
        flash("Содержание сообщения обязательно", "error")
        return redirect(url_for("forum.thread_detail", thread_id=thread_id))

    try:
        ForumService.create_post(thread_id, user.id, content)
        flash("Ответ успешно добавлен!", "success")
    except ValueError as e:
        flash(str(e), "error")

    return redirect(url_for("forum.thread_detail", thread_id=thread_id))


@forum_bp.route("/post/<int:post_id>/delete/<int:thread_id>")
def delete_post(post_id, thread_id):
    """Delete a post"""
    if "user_id" not in session:
        flash("Пожалуйста, войдите в систему для удаления сообщения", "warning")
        return redirect(url_for("user.login"))

    user = User.query.get(session["user_id"])
    if not user:
        flash("Доступ запрещен", "error")
        return redirect(url_for("main.index"))

    try:
        ForumService.delete_post(post_id, user.id)
        flash("Сообщение успешно удалено!", "success")
    except ValueError as e:
        flash(str(e), "error")

    return redirect(url_for("forum.thread_detail", thread_id=thread_id))


# Reporting routes
@forum_bp.route("/report/submit", methods=["POST"])
def submit_report():
    """Submit a content report"""
    if "user_id" not in session:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    user = User.query.get(session["user_id"])
    if not user or not user.is_regular_user:
        return jsonify({"status": "error", "message": "Access denied"}), 403

    try:
        content_type = request.form.get("content_type")
        content_id = request.form.get("content_id")
        reason = request.form.get("reason")
        description = request.form.get("description", "")

        if not content_type or not content_id or not reason:
            return jsonify({"status": "error", "message": "Missing required fields"}), 400

        report = ReportingService.submit_report(
            reporter_id=user.id,
            reported_type=content_type,
            reported_id=content_id,
            reason=reason,
            description=description
        )

        return jsonify({"status": "success", "message": "Report submitted successfully"})
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": "An error occurred while submitting report"}), 500