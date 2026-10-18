import datetime

from flask import Blueprint, current_app, jsonify, request

from ..models import GB, Node, TrafficLog, User, db
from .sub import generate_subscription

bp = Blueprint("api", __name__)


def _current_user():
    from flask import session

    uid = session.get("user_id")
    return User.query.get(uid) if uid else None


@bp.get("/api/subscribe")
def subscribe():
    # The subscription token IS the credential for this endpoint, so an absent
    # or malformed token is an authentication failure (401), not a missing
    # resource. A well-formed token that matches no user is a genuine 404.
    token = request.args.get("token", "")
    if not token.isdigit():
        return jsonify({"error": "token required"}), 401
    user = User.query.get(int(token))
    if not user:
        return jsonify({"error": "no such user"}), 404
    nodes = Node.query.filter_by(enable=True).all()
    return generate_subscription(user, nodes, request.args.get("sub_type", "vmess"))


@bp.post("/api/traffic")
def traffic():
    if request.headers.get("X-API-Token") != current_app.config.get("API_TOKEN", "dev-api-token"):
        return jsonify({"error": "unauthorized"}), 401
    d = request.get_json(force=True, silent=True) or {}
    node = Node.query.get(d.get("node_id"))
    if not node:
        return jsonify({"error": "node not found"}), 404
    node.last_seen = datetime.datetime.now(datetime.UTC).replace(tzinfo=None)
    for u in d.get("users", []):
        user = User.query.get(u.get("id"))
        if not user:
            continue
        user.upload_traffic = (user.upload_traffic or 0) + u.get("upload", 0)
        user.download_traffic = (user.download_traffic or 0) + u.get("download", 0)
        if user.overflow():
            user.enable = False
        db.session.add(
            TrafficLog(
                user_id=user.id,
                node_id=node.id,
                upload=u.get("upload", 0),
                download=u.get("download", 0),
            )
        )
    db.session.commit()
    return jsonify({"status": "ok"})


@bp.post("/api/admin/users")
def admin_add_user():
    if not (_u := _current_user()) or not _u.is_admin:
        return jsonify({"error": "admin required"}), 403
    d = request.get_json(force=True, silent=True) or {}
    user = User(
        username=d["username"],
        ss_port=d.get("port", 8388),
        total_traffic=d.get("traffic", 20 * GB),
        level=d.get("level", 0),
    )
    user.set_password(d.get("password", ""))
    db.session.add(user)
    db.session.commit()
    return jsonify({"status": "success", "user": user.to_dict()})


@bp.get("/api/health")
def health():
    return jsonify({"status": "ok", "users": User.query.count(), "nodes": Node.query.count()})


@bp.get("/api/admin/analytics")
def analytics():
    if not (_u := _current_user()) or not _u.is_admin:
        return jsonify({"error": "admin required"}), 403
    return jsonify(
        {
            "users": User.query.count(),
            "nodes": Node.query.count(),
            "active": sum(1 for u in User.query.all() if u.enable),
        }
    )
