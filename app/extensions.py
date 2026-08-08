from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from configs.limiter import limiter

__all__ = ["limiter"]

# Initialize SQLAlchemy and Migrate instances for database operations
db = SQLAlchemy()
migrate = Migrate()
redis_client = None