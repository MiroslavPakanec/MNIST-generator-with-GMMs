import pandas as pd
from typing import Dict, List, Tuple
from src.utilities.environment import Environment
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.mongo_client import MongoClient
from pandas import DataFrame, Series
from loguru import logger

connection_string: str = f'mongodb://db:{Environment().MONGO_DB_PORT}/'
client: MongoClient = MongoClient(connection_string)
db: Database = client[Environment().MONGO_DB_NAME]
train_collection: Collection = db[Environment().MONGO_DB_TRAIN_COLLECTION_NAME]
test_collection: Collection = db[Environment().MONGO_DB_TEST_COLLECTION_NAME]

def load_train_data() -> Tuple[DataFrame, Series]:
    cursor = train_collection.find()
    samples: List[Dict[int, List[int]]] = list(cursor)
    xs: List[int][int] = []
    ys: List[int] = []
    for sample in samples:
        xs.append(sample['data'])
        ys.append(sample['label'])
    return pd.DataFrame(xs), pd.Series(ys)

def insert_train_samples(xs: DataFrame, ys: Series) -> None:
    logger.info('inserting train samples...')
    samples: List[Dict] = [{'data': row.tolist(), 'label': label} for row, label in zip(xs.values, ys)]
    train_collection.insert_many(samples)
    logger.info('[DONE] inserting train samples')

def remove_train_samples() -> None:
    logger.info('removing train samples')
    train_collection.delete_many({})
    logger.info('[DONE] removing train samples')

def insert_test_samples(xs: DataFrame) -> None: 
    logger.info('inserting test samples')
    samples: List[Dict] = [{'data': row.tolist()} for row in xs.values]
    test_collection.insert_many(samples)
    logger.info('[DONE] inserting test samples')

def remove_test_samples() -> None:
    logger.info('removing test samples')
    test_collection.delete_many({})
    logger.info('[DONE] removing test samples')