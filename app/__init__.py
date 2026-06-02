from flask_openapi3 import Info, OpenAPI

from routes.v1 import v1_bp
from handlers.error_handlers import register_error_handlers
from middlewares.request_middlewares import register_middleware
from configs.logging_config import configure_logging
from app.extensions import (
    db,
    limiter,
    migrate
)
from configs.settings import settings
import models

def create_app():
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
    limiter.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # Register middlewares, error handlers, and blueprints
    register_middleware(app)
    register_error_handlers(app)
    app.register_api(v1_bp)

    return app