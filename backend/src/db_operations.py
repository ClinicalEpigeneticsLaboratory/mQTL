from typing import Optional

import pymongo
import pandas as pd
from sqlalchemy import select
from sqlalchemy import create_engine
from sqlalchemy import Table, MetaData

from .url_utils import create_postgres_url, create_mongo_url


def select_omics_data_from_db(rs: str, cpg: str, db_name: str = "mQTL") -> pd.DataFrame:
    db_url = create_mongo_url()
    client = pymongo.MongoClient(db_url)
    db = client[db_name]

    gse = pd.DataFrame(db["GSA"].find({"_id": rs})).set_index("_id").T
    epic = pd.DataFrame(db["EPIC"].find({"_id": cpg})).set_index("_id").T

    df = pd.concat((gse, epic), axis=1, join="inner")

    return df


def select_clinical_data_from_db(
    age: tuple,
    sex: tuple,
    sample_group: str,
    tissue: str,
    columns: Optional[list | tuple] = None,
) -> pd.DataFrame:
    db_url = create_postgres_url()
    engine = create_engine(db_url)
    samples = Table("samples", MetaData(), autoload_with=engine)

    stmt = (
        samples.select()
        .where(samples.c.age.between(*age))
        .where(samples.c.sex.in_(sex))
        .where(samples.c.sample_group == sample_group)
        .where(samples.c.tissue == tissue)
    )

    with engine.connect() as conn:
        result = pd.DataFrame.from_records(conn.execute(stmt).all())
        col_names = [c.name for c in samples.c]
        result.columns = col_names

    if columns:
        result = result[columns]

    return result


def select_samples_from_db(
    age: tuple, sex: tuple, sample_group: str, tissue: tuple
) -> list:
    db_url = create_postgres_url()
    engine = create_engine(db_url)

    samples = Table("samples", MetaData(), autoload_with=engine)

    stmt = (
        select(samples.c.sample_name)
        .where(samples.c.age.between(*age))
        .where(samples.c.sex.in_(sex))
        .where(samples.c.sample_group == sample_group)
        .where(samples.c.tissue == tissue)
    )

    with engine.connect() as conn:
        result = conn.execute(stmt).all()

    result = [r[0] for r in result]
    return result
