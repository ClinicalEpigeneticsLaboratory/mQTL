import pandas as pd
from celery_app import celery_app
from src.mQTL import mQTL


@celery_app.task(track_started=True)
def add(x, y):
    return x + y


@celery_app.task(track_started=True)
def mul(x, y):
    return x * y


@celery_app.task(track_started=True)
def div(x, y):
    return x / y


@celery_app.task(track_started=True)
def analyse(samples: list, cpg: str, rs: str, model_type: str, reg: float):
    analysis = mQTL(samples, cpg, rs, model_type, reg)
    analysis.load_data()

    table_a, table_b, predictions = analysis.model()
    plot = analysis.plot()

    return {
        "tableA": table_a,
        "tableB": table_b,
        "Predictions": predictions,
        "Plot": plot,
    }
