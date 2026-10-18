"""subforge — application factory.

Templates live in the project-root templates/ directory (not panel/templates/),
so the template folder is passed explicitly.  Flask(__name__) alone would look
in panel/templates/ and raise TemplateNotFound on "/".  The SQLite file lives in
the project-root instance/ directory for the same reason.

panel/api.py declares its own "/api/..." paths, so the blueprint is registered
WITHOUT a url_prefix; adding one produced the broken double prefix /api/api/... .
"""

from .models import db
from .panel.api import bp
from .panel.web import web
from .seed import seed
from . import paths

paths.ensure_runtime_dirs()

def build_app():
    from flask import Flask
    app = Flask(__name__, template_folder=str(paths.TEMPLATES_DIR),
                instance_path=str(paths.INSTANCE_DIR))
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + str(paths.INSTANCE_DIR / "v2scar.db")
    app.config["SECRET_KEY"] = "dev"
    app.config["API_TOKEN"] = "dev-api-token"
    db.init_app(app)
    app.register_blueprint(bp)
    app.register_blueprint(web)
    with app.app_context():
        db.create_all()
        seed()
    return app

app = build_app()
