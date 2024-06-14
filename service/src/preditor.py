import numpy as np
from typing import Dict, List
from numpy.typing import NDArray
from pandas import DataFrame, Series
from scipy.stats import multivariate_normal
from src.dtos.mnist_sample import MNISTSample
from src.data_csv_loader import load_train_data
from src.data_db_loader import load_train_data
from src.validator import validate_sample, validate_label

def get_prediction(sample: MNISTSample) -> int:
    validate_sample(sample)
    xs, ys = load_train_data()
    labels: List[int] = list(ys.unique())
    priors: Dict[int, float] = _get_priors(xs, ys, labels)
    means: Dict[int, NDArray[np.float64]] = _get_means(xs, ys, labels)
    covariances: Dict[int, NDArray[np.float64]] = _get_covariances(xs, ys, labels)

    log_posterios: Dict[int, NDArray[np.float64]] = _get_log_posteriors(sample, labels, means, covariances, priors)
    posteriors: Dict[int, NDArray[np.float64]] = _normilize_posterios(log_posterios, labels)
    pred = _get_most_likely_label(posteriors)
    return int(pred)

def get_sample(label: int) -> MNISTSample:
    validate_label(label)
    xs, ys = load_train_data()
    labels: List[int] = list(ys.unique())
    means: Dict[int, NDArray[np.float64]] = _get_means(xs, ys, labels)
    covariances: Dict[int, NDArray[np.float64]] = _get_covariances(xs, ys, labels)
    sample = multivariate_normal.rvs(means[label], covariances[label])
    sample = _get_scaled_sample(sample)
    return sample    

def get_sample_mean(label: int) -> MNISTSample:
    validate_label(label)
    xs, ys = load_train_data()
    labels: List[int] = list(ys.unique())
    means: Dict[int, NDArray[np.float64]] = _get_means(xs, ys, labels)
    sample_mean = _get_scaled_sample(means[label])
    return sample_mean

def _get_scaled_sample(sample: MNISTSample) -> MNISTSample:
    min_val = sample.min()
    max_val = sample.max()
    normalized_sample = (sample - min_val) / (max_val - min_val)
    scaled_sample = (normalized_sample * 255).astype(np.uint8)
    return scaled_sample

def _get_priors(xs: DataFrame, ys: Series, labels: List[int]) -> Dict[int, float]:
    priors: Dict[int, float] = {}
    for y in labels: 
        priors[y] = len(xs[ys == y]) / len(xs)
    return priors

def _get_covariances(xs: DataFrame, ys: Series, labels: List[int]) -> Dict[int, NDArray[np.float64]]:
    covariances: Dict[int, NDArray[np.float64]] = {}
    for y in labels: 
        covariances[y] = np.cov(xs[ys == y].T)
    return covariances

def _get_means(xs: DataFrame, ys: Series, labels: List[int]) -> Dict[int, NDArray[np.float64]]:
    means: Dict[int, NDArray[np.float64]] = {}
    for y in labels:
        means[y] = xs[ys == y].mean().values
    return means

def _get_log_posteriors(sample: MNISTSample, labels: List[int], means: Dict[int, NDArray[np.float64]], covariances: Dict[int, NDArray[np.float64]], priors: Dict[int, float]) -> Dict[int, NDArray[np.float64]]:
    log_posteriors: Dict[int, NDArray[np.float64]] = {}
    for y in labels:
        log_likelihood: NDArray[np.float64] = multivariate_normal.logpdf(sample, mean=means[y], cov=covariances[y], allow_singular=True)
        log_posteriors[y] = log_likelihood + np.log(priors[y])
    return log_posteriors

def _normilize_posterios(log_posteriors: Dict[int, NDArray[np.float64]], labels: List[int]) -> Dict[int, NDArray[np.float64]]:
    max_log_posterior = max(log_posteriors.values())
    posteriors: Dict[int, NDArray[np.float64]] = {y: np.exp(log_posteriors[y] - max_log_posterior) for y in labels} # Prevent underflow with the log-sum-exp
    total_posterior = sum(posteriors.values())
    for y in labels:
        posteriors[y] /= total_posterior
    return posteriors

def _get_most_likely_label(posteriors: Dict[int, NDArray[np.float64]]) -> int:
    return max(posteriors, key=posteriors.get)
        