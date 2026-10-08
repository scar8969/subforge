from ..models import Node, User
from .api import _current_user

from flask import Blueprint, render_template, redirect, url_for, session, flash, request as _req

web = Blueprint("web", __name__)

@web.route("/")
def index():
    if not session.get("user_id"):
        return redirect(url_for("web.login"))
    return render_template("dashboard.html", user=_current_user(),
                           nodes=Node.query.order_by(Node.id).all())

@web.route("/login", methods=["GET", "POST"])
def login():
    if _req.method == "POST":
        u = User.query.filter_by(username=_req.form.get("username", "")).first()
        if u and u.check_password(_req.form.get("password", "")):
            session["user_id"] = u.id
            return redirect(url_for("web.index"))
        flash("Invalid username or password", "error")
    return render_template("login.html")

@web.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("web.login"))

@web.route("/users")
def users():
    if not session.get("user_id"):
        return redirect(url_for("web.login"))
    return render_template("admin.html", users=User.query.order_by(User.id).all(),
                           user=_current_user())
