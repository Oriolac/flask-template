from flask import Flask
from config import ConfigDev
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(ConfigDev)
    migrate = Migrate(app, db)

    login_manager.init_app(app)
    login_manager.login_view = "login"

    db.init_app(app)
    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    from .main import main_bp
    app.register_blueprint(main_bp)

    return app
