from os import environ


def create_postgres_url(
    host=environ.get("POETRY_DB_HOST"),
    user=environ.get("POETRY_DB_USER"),
    passwd=environ.get("POETRY_DB_PASS"),
    port=environ.get("POETRY_DB_PORT"),
    db_name=environ.get("POETRY_DB_NAME"),
) -> str:
    return f"postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db_name}"


def create_mongo_url(
    host=environ.get("POETRY_MONGO_HOST"),
    user=environ.get("POETRY_MONGO_USER"),
    passwd=environ.get("POETRY_MONGO_PASS"),
    port=environ.get("POETRY_MONGO_PORT"),
) -> str:
    return f"mongodb://{user}:{passwd}@{host}:{port}/"


def create_broker_url(
    user=environ.get("POETRY_RABBITMQ_USER"),
    passwd=environ.get("POETRY_RABBITMQ_PASS"),
    port=environ.get("POETRY_RABBITMQ_PORT"),
) -> str:
    return f"pyamqp://{user}:{passwd}@rabbitmq:{port}//"


def create_backend_url(
    user=environ.get("POETRY_RABBITMQ_USER"),
    passwd=environ.get("POETRY_RABBITMQ_PASS"),
    port=environ.get("POETRY_RABBITMQ_PORT"),
) -> str:
    return f"rpc://{user}:{passwd}@rabbitmq:{port}"
