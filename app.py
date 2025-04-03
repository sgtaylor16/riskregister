from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import secrets
from extensions import db



def create_app():
    flask_app = Flask(__name__)
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{flask_app.root_path}/dbcode/riskregister.db"
    flask_app.secret_key = secrets.token_urlsafe(16)

    db.init_app(flask_app)

    from pages.risks.risks import risks_bp
    from pages .programs.programs import programs_bp
    from pages.main import index_bp
    flask_app.register_blueprint(index_bp)
    flask_app.register_blueprint(risks_bp)
    flask_app.register_blueprint(programs_bp)

    return flask_app

