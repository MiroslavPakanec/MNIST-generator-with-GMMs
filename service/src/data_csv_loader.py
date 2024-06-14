import numpy as np
import pandas as pd
from typing import List, Dict, Tuple
from numpy.typing import NDArray
from pandas import DataFrame, Series
from src.utilities.environment import Environment

def load_train_data() -> Tuple[DataFrame, Series]:
    df: DataFrame = pd.read_csv(Environment().TRAIN_DATA_PATH)
    xs: DataFrame = df.iloc[:, 1:]
    ys: Series = df.iloc[:, 0]
    return xs, ys

def load_test_data() -> DataFrame:
    xs: DataFrame = pd.read_csv(Environment().TEST_DATA_PATH)
    return xs
