from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, Field
from tasks import analyse, celery_app
from src.src import select_data_from_db, select_samples_from_db

api_app = FastAPI()


# Celery tasks
@api_app.get("/result/{task_id}")
async def get_status(task_id: str) -> dict:
    result = celery_app.AsyncResult(task_id)
    if result.ready():
        return {"TaskID": task_id, "Status": result.status, "Result": result.get()}
    return {"TaskID": task_id, "Status": result.status, "Result": None}


@api_app.get("/status")
async def status() -> dict:
    celery_val = celery_app.control.ping()
    return {
        "Celery": celery_val,
    }


class ToAnalyse(BaseModel):
    samples: tuple[str, ...] = Field(
        min_length=3, default=("EPIxPUMxKx007", "EPIxPUMxKx012", "EPIxPUMxKx013")
    )
    cpg: str = "cg00000029"
    rs: str = "rs116587930"
    model_type: str = "OLS"
    reg: float = 1.0

    @property
    def values(self) -> list:
        return [self.samples, self.cpg, self.rs, self.model_type, self.reg]


@api_app.post("/analyse")
async def start_analyse(to_analyse: ToAnalyse) -> dict:
    task = analyse.delay(*to_analyse.values)
    return {"TaskID": task.id}


# Normal tasks
class QuerySlice(BaseModel):
    age: tuple[int, int] = (1, 100)
    sex: tuple[str, ...] = Field(max_length=2, min_length=1, default=("Male", "Female"))
    phenotype: tuple[str, ...] = Field(
        max_length=2, min_length=1, default=("Healthy sample", "Melanoma")
    )
    tissue: tuple[str, ...] = Field(
        max_length=2, min_length=1, default=("Blood", "Swab")
    )

    @property
    def values(self) -> list:
        return [self.age, self.sex, self.phenotype, self.tissue]


@api_app.post("/data")
async def data(query_slice: QuerySlice) -> dict:
    result = select_data_from_db(*query_slice.values)
    return result


@api_app.post("/samples")
async def samples(query_slice: QuerySlice) -> tuple:
    result = select_samples_from_db(*query_slice.values)
    return result
