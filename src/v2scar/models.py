import hashlib
import uuid

from flask_sqlalchemy import SQLAlchemy

from .clock import utcnow

db = SQLAlchemy()
GB = 1024**3


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128), default="")
    vmess_uuid = db.Column(db.String(64), default=lambda: str(uuid.uuid4()))
    ss_port = db.Column(db.Integer, unique=True)
    level = db.Column(db.Integer, default=0)
    upload_traffic = db.Column(db.BigInteger, default=0)
    download_traffic = db.Column(db.BigInteger, default=0)
    total_traffic = db.Column(db.BigInteger, default=20 * GB)
    enable = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=utcnow)

    def set_password(self, raw):
        self.password_hash = _hash(raw, "v2scar")

    def check_password(self, raw):
        return self.password_hash == _hash(raw, "v2scar")

    def used_traffic(self):
        return (self.upload_traffic or 0) + (self.download_traffic or 0)

    def overflow(self):
        return self.used_traffic() >= (self.total_traffic or 0)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "uuid": self.vmess_uuid,
            "port": self.ss_port,
            "level": self.level,
            "used": self.used_traffic(),
            "total": self.total_traffic,
            "enable": self.enable,
        }

    def __init__(self, **kw):
        # Cooperative constructor.  The core's override used to swallow every
        # keyword (`kw.get`), so User(username=..., ss_port=...) built a row with
        # NULL username and NULL password_hash -- login could never match and the
        # panel rendered blank names.  Keep the core's uuid/password defaults and
        # map every remaining keyword onto the declared columns.
        import uuid

        self.vmess_uuid = kw.pop("vmess_uuid", str(uuid.uuid4()))
        self.password_hash = kw.pop("password_hash", "")
        columns = set(self.__mapper__.columns.keys())
        for key, value in kw.items():
            if key not in columns:
                raise TypeError(f"User() got an unexpected keyword argument {key!r}")
            setattr(self, key, value)


class Node(db.Model):
    __tablename__ = "nodes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), default="")
    server = db.Column(db.String(256), default="")
    port = db.Column(db.Integer, default=443)
    country = db.Column(db.String(8), default="CN")
    used_traffic = db.Column(db.BigInteger, default=0)
    total_traffic = db.Column(db.BigInteger, default=GB)
    enable = db.Column(db.Boolean, default=True)
    last_seen = db.Column(db.DateTime, nullable=True)


class TrafficLog(db.Model):
    __tablename__ = "traffic_logs"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True)
    node_id = db.Column(db.Integer, index=True)
    upload = db.Column(db.BigInteger, default=0)
    download = db.Column(db.BigInteger, default=0)
    created_at = db.Column(db.DateTime, default=utcnow)


def _hash(pw, salt):
    return hashlib.sha256(f"{salt}:{pw}".encode()).hexdigest()
