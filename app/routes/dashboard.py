from flask import Blueprint, render_template, session
from sqlalchemy.orm.exc import NoResultFound
from app.utils.auth import login_required
from app.models import Post
from app.db import get_db

bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@bp.route("/")
@login_required
def dash():
    db = get_db()
    posts = (
        db.query(Post)
        .filter(Post.user_id == session.get("user_id"))
        .order_by(Post.created_at.desc())
        .all()
    )
    return render_template(
        "dashboard.html", posts=posts, loggedIn=session.get("loggedIn")
    )


@bp.route("/edit/<id>")
@login_required
def edit(id):
    db = get_db()
    try:
        post = db.query(Post).filter(Post.id == id).one()
    except NoResultFound:
        return "Post not found", 404

    return render_template(
        "edit-post.html", post=post, loggedIn=session.get("loggedIn")
    )
