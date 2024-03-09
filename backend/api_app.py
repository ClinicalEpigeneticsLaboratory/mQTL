from celery import Celery
from fastapi import FastAPI
from sqlalchemy import create_engine
from pydantic import BaseModel, Field
from sqlalchemy.exc import SQLAlchemyError
from pymongo.errors import ConnectionFailure
from pymongo import MongoClient

from tasks import analyse, celery_app
from src.url_utils import create_postgres_url, create_mongo_url
from src.url_utils import create_broker_url, create_backend_url
from src.db_operations import select_samples_from_db

api_app = FastAPI()


@api_app.get("/test-mongo")
def test_mongodb_connection():
    try:
        client = MongoClient(create_mongo_url())
        db = client["mQTL"]

        db.command("serverStatus")
        client.close()

        return {"Mongo": "ok"}

    except ConnectionFailure:
        return {"Mongo": "Failed to connect to MongoDB"}


@api_app.get("/test-postgres")
def test_postgres_connection():
    try:
        engine = create_engine(create_postgres_url())
        with engine.connect():
            return {"Postgres": "ok"}

    except SQLAlchemyError:
        return {"Postgres": "Failed to connect to PostgresDB"}


@api_app.get("/test-celery")
def test_celery():
    app = Celery(include=["tasks"])

    app.conf.broker_url = create_broker_url()
    app.conf.result_backend = create_backend_url()

    response = app.control.ping()

    if response:
        return {"Celery": "ok"}

    return {"Celery": "Failed to ping Celery"}


class ToAnalyse(BaseModel):
    age: tuple[int, int] = (1, 100)
    sex: tuple[str, ...] = Field(max_length=2, min_length=1, default=("Male", "Female"))
    sample_group: str = "Healthy sample"
    tissue: str = "Blood"
    phenotype: str = "epigenetic_age"
    cpg: str = "cg24851651"
    rs: str = "rs1671064"

    @property
    def samples_characteristics(self) -> dict:
        return {
            "age": self.age,
            "sex": self.sex,
            "sample_group": self.sample_group,
            "tissue": self.tissue,
        }

    @property
    def params(self) -> dict:
        return {
            "cpg": self.cpg,
            "rs": self.rs,
            "phenotype": self.phenotype,
        }


@api_app.post("/analyse")
async def start_analyse(to_analyse: ToAnalyse) -> dict:
    task = analyse.delay(to_analyse.samples_characteristics, **to_analyse.params)
    return {"TaskID": task.id}


@api_app.get("/result/{task_id}")
async def get_status(task_id: str) -> dict:
    result = celery_app.AsyncResult(task_id)
    if result.ready():
        return {"TaskID": task_id, "Status": result.status, "Result": result.get()}
    return {"TaskID": task_id, "Status": result.status, "Result": None}


class QuerySamples(BaseModel):
    age: tuple[int, int] = (1, 100)
    sex: tuple[str, ...] = Field(max_length=2, min_length=1, default=("Male", "Female"))
    sample_group: str = "Healthy sample"
    tissue: str = "Blood"

    @property
    def values(self) -> dict:
        return {
            "age": self.age,
            "sex": self.sex,
            "sample_group": self.sample_group,
            "tissue": self.tissue,
        }


@api_app.post("/samples")
async def samples(query: QuerySamples) -> list:
    result = select_samples_from_db(**query.values)
    return result
