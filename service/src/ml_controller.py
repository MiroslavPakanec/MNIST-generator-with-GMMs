import numpy as np
from loguru import logger
from typing import Dict, List, Tuple, Union
from numpy.typing import NDArray
from pandas import DataFrame, Series
from sklearn.decomposition import PCA
from sklearn.mixture import GaussianMixture
from sklearn.metrics import accuracy_score, confusion_matrix
from scipy.stats import multivariate_normal
from src.utilities.environment import Environment
from src.dtos.mnist_sample import MNISTSample
from src.data_csv_loader import load_train_data
from src.data_db_loader import load_train_data
from src.validator import validate_initialization_dicts, validate_sample, validate_label

PCA_DICT = {}
MODEL_DICT = {}

def initialize() -> None:
    global MODEL_DICT
    global PCA_DICT
    xs, ys = load_train_data()
    labels = ys.unique()
    for label in labels:
        pca = PCA(n_components=Environment().PCA_COMPONENTS)
        xs_pca = pca.fit_transform(xs[ys == label].to_numpy())
        model: GaussianMixture = GaussianMixture(n_components=Environment().GMM_COMPONENTS)
        model.fit(xs_pca)
        MODEL_DICT[label] = model
        PCA_DICT[label] = pca

def generate_sample(label: int) -> np.ndarray:
    validate_label(label)
    validate_initialization_dicts(MODEL_DICT, PCA_DICT, label)
    pca = PCA_DICT[label]
    model = MODEL_DICT[label]
    xs_pca, _ = model.sample()
    xs = pca.inverse_transform(xs_pca)
    return xs[0]


def get_clusters(label: int) -> Dict[int, np.ndarray]:
    validate_label(label)
    validate_initialization_dicts(MODEL_DICT, PCA_DICT, label)
    xs, ys = load_train_data()
    pca = PCA_DICT[label]
    model = MODEL_DICT[label]
    xs_pca = pca.transform(xs[ys == label].to_numpy())
    gmm_labels = model.predict(xs_pca)
    clusters: Dict[int, np.ndarray] = {}
    for i in range(Environment().GMM_COMPONENTS):
        clusters[i] = xs_pca[gmm_labels == i]
    return clusters