from flask import Flask

from redis import Redis
from routes.v1 import v1_bp
from handlers.error_handlers import register_error_handlers
from middlewares.request_middlewares import register_middleware
from configs.logging_config import configure_logging
import app.extensions as ext
from app.commands.seed_blueprints import seed_exam_blueprints_command
from configs import get_settings
from app.security.jwt_keys import ensure_jwt_keys
import models

def create_app():
    """
    Creates the flask app object.
    Configures configurations.
    Initializes extensions.
    Registers middlewares, error handlers, and blueprints.
    """
    # Get the settings object
    settings = get_settings()
    
    # Configure root logger
    configure_logging()

    # Ensure JWT keys exist
    ensure_jwt_keys(settings)

    # Create main flask app object
    app = Flask(__name__)

    # Database configs
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = (
        settings.SQLALCHEMY_TRACK_MODIFICATIONS
    )

    # Register DB seeding command
    app.cli.add_command(seed_exam_blueprints_command)

    # Initialize extensions
    ext.limiter.init_app(app)
    ext.db.init_app(app)
    ext.migrate.init_app(app, ext.db)
    ext.redis_client = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        decode_responses=True
    )

    # Verify Redis connection on server startup
    try:
        ext.redis_client.ping()
    except Exception:
        raise RuntimeError("Failed to connect Redis")

    # Register middlewares, error handlers, and blueprints
    register_middleware(app)
    register_error_handlers(app)
    app.register_blueprint(v1_bp)

    return app