import os

from paradigmatic.app.v1.core.celery_app import celery_app


@celery_app.task(acks_late=True)
def example_task(word: str) -> str:
    return f"test task returns {word}"


dir_path = os.path.dirname(os.path.realpath(__file__))


