from loguru import logger
from pymongo.collection import Collection
from src.data_csv_loader import load_train_data, load_test_data
from src.data_db_loader import insert_train_samples, remove_train_samples, insert_test_samples, remove_test_samples
from src.utilities.environment import Environment

def data_migration():
    xs_train, ys = load_train_data()
    remove_train_samples()
    insert_train_samples(xs_train, ys)
    
    xs_test = load_test_data()
    remove_test_samples()
    insert_test_samples(xs_test)
    
if __name__ == "__main__":
    if Environment().RUN_MIGRATION is True:
        logger.info('Migrating datasets...')
        data_migration()