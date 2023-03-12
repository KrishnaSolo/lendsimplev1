from flask import Flask
from .config import Config
from .database import db
from .services.auth import auth_bp
from .services.investor import investor_bp
from .services.property import property_blueprint as property_bp
from .services.event import event_bp
from .services.preapprove import pre_approve_bp as preapprove_bp
from .utils.logging import setup_logging


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize database
    db.init_db(app)
    logger = setup_logging()
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(investor_bp)
    app.register_blueprint(property_bp)
    app.register_blueprint(event_bp)
    app.register_blueprint(preapprove_bp)
    app.register_blueprint(approve_bp)

    return app
