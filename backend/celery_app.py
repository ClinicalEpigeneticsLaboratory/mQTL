from os import environ
from celery import Celery
from src.url_utils import create_broker_url, create_backend_url

celery_app = Celery(include=["tasks"])

celery_app.conf.broker_url = create_broker_url()
celery_app.conf.result_backend = create_backend_url()

celery_app.conf.timezone = environ["POETRY_TIMEZONE"]
celery_app.conf.broker_connection_retry = True
