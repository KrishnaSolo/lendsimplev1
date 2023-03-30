from flask import Flask
from backend.services.property import PropertyEncoder
from backend.config import Config
from backend.database import init_db
from backend.services.auth import auth_bp
from backend.services.investor import investor_bp
from backend.services.property import property_blueprint as property_bp
from backend.services.event import event_bp
from backend.services.preapprove import pre_approve_bp as preapprove_bp
from backend.utils.logging import setup_logging


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.json_encoder = PropertyEncoder

    # Initialize database
    init_db(app)
    logger = setup_logging()
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(investor_bp)
    app.register_blueprint(property_bp)
    app.register_blueprint(event_bp)
    app.register_blueprint(preapprove_bp)

    return app
