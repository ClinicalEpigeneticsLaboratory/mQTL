from sqlalchemy import Table, MetaData
from sqlalchemy import create_engine
from sqlalchemy import select
import pandas as pd

from .url_utils import create_postgres_url


def select_data_from_db(
    age: tuple, sex: tuple, phenotype: tuple, tissue: tuple
) -> dict:
    db_url = create_postgres_url()
    engine = create_engine(db_url)
    samples = Table("samples", MetaData(), autoload_with=engine)

    stmt = (
        samples.select()
        .where(samples.c.age.between(*age))
        .where(samples.c.sex.in_(sex))
        .where(samples.c.phenotype.in_(phenotype))
        .where(samples.c.tissue.in_(tissue))
    )

    with engine.connect() as conn:
        result = pd.DataFrame.from_records(conn.execute(stmt).all())

    return result.to_dict()


def select_samples_from_db(
    age: tuple, sex: tuple, phenotype: tuple, tissue: tuple
) -> tuple:
    db_url = create_postgres_url()
    engine = create_engine(db_url)
    samples = Table("samples", MetaData(), autoload_with=engine)

    stmt = (
        select(samples.c.sample_name)
        .where(samples.c.age.between(*age))
        .where(samples.c.sex.in_(sex))
        .where(samples.c.phenotype.in_(phenotype))
        .where(samples.c.tissue.in_(tissue))
    )

    with engine.connect() as conn:
        result = conn.execute(stmt).all()

    result = tuple(r[0] for r in result)
    return result
