"""
This file imports app and adds app context in celery worker.
"""

from app.factory import create_app
from app.celery_app import celery_app as celery

def init_worker():
    """Initialize the Celery worker with Flask app context."""
    app = create_app()

    class FlaskTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = FlaskTask

init_worker()