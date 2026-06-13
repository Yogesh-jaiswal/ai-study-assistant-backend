from flask_openapi3 import Info, OpenAPI

from redis import Redis
from routes.v1 import v1_bp
from handlers.error_handlers import register_error_handlers
from middlewares.request_middlewares import register_middleware
from configs.logging_config import configure_logging
from app.extensions import ext
from configs import get_settings
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

    info = Info(
        title = "AI Study Assistant API",
        version = "1.0.0"
    )

    # Create main flask app object
    app = OpenAPI(__name__, info = info)

    # Database configs
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = (
        settings.SQLALCHEMY_TRACK_MODIFICATIONS
    )

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
    app.register_api(v1_bp)

    return app