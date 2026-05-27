from flask_openapi3 import Info, OpenAPI

from routes.v1 import v1_bp
from handlers.error_handlers import register_error_handlers
from middlewares.request_middlewares import register_middleware
from configs.logging_config import configure_logging
from .extensions import limiter

def create_app():
    # Configure root logger
    configure_logging()

    info = Info(
        title = "AI Study Assistant API",
        version = "1.0.0"
    )

    # Create main flask app object
    app = OpenAPI(__name__, info = info)

    # Initialize rate limiter
    limiter.init_app(app)

    # Register middlewares, error handlers, and blueprints
    register_middleware(app)
    register_error_handlers(app)
    app.register_api(v1_bp)

    return app