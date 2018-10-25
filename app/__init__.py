from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

#app = Flask(__name__)
#app.config.from_object(Config)
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    """ from app.api.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth') """

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    return app

from app.data_models import *