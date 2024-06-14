from pydantic_settings import BaseSettings

from src.utilities.singleton import singleton


@singleton
class Environment(BaseSettings):
    ENVIRONMENT: str = 'production'

    HOST_IP: str
    CONTAINER_PORT: int
    COMPOSE_PROJECT_NAME: str

    TRAIN_DATA_PATH: str
    TEST_DATA_PATH: str

    MONGO_DB_PORT: int
    MONGO_DB_NAME: str
    MONGO_DB_TRAIN_COLLECTION_NAME: str
    MONGO_DB_TEST_COLLECTION_NAME: str
    RUN_MIGRATION: bool
