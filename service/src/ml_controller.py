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
from src.validator import validate_model, validate_sample, validate_label

MODEL: Union[None, GaussianMixture] = None

def initialize_model() -> None:
    global MODEL
    xs, ys = load_train_data()
    pca = PCA(n_components=Environment().PCA_COMPONENTS)
    xs_pca = pca.fit_transform(xs.to_numpy())
    model: GaussianMixture = GaussianMixture(n_components=Environment().GMM_COMPONENTS)
    model.fit(xs_pca)
    MODEL = model


def get_clusters_evaluation() -> Tuple[Dict[int, np.ndarray], np.ndarray, float, np.ndarray]:
    validate_model(MODEL)
    xs, ys = load_train_data()
    ys_numpy: np.ndarray = ys.to_numpy()
    pca = PCA(n_components=Environment().PCA_COMPONENTS)
    xs_pca: np.ndarray = pca.fit_transform(xs)
    gmm_labels: NDArray[np.int8] = MODEL.predict(xs_pca)

    clusters: Dict[int, np.ndarray] = _get_clusters(xs_pca, gmm_labels)
    cluster_to_digit_mapping: np.ndarray = _get_cluster_to_digit_mappings(gmm_labels, ys_numpy)
    predicted_digits: np.ndarray = cluster_to_digit_mapping[gmm_labels]
    accuracy: float = _get_accuracy(ys_numpy, predicted_digits)
    confusion_matrix: np.ndarray = _get_confusion_matrix(ys_numpy, predicted_digits)
    return clusters, cluster_to_digit_mapping, accuracy, confusion_matrix

def generate_sample(label: int) -> np.ndarray:
    validate_model(MODEL)
    validate_label(label)
    
    while True:    
        xs, ys = MODEL.sample()
        if ys[0] == label:
            return xs

    # # Calculate the accuracy
    # accuracy = accuracy_score(y, predicted_digits)
    # print(f'Clustering Accuracy: {accuracy:.2f}')

    # Plot the confusion matrix
    # cm = confusion_matrix(y, predicted_digits)
    # plt.figure(figsize=(10, 8))
    # sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    # plt.xlabel('Predicted Labels')
    # plt.ylabel('True Labels')
    # plt.title('Confusion Matrix for GMM Clustering on MNIST')
    # plt.show()

    # # Visualize the clusters with actual digit labels in the legend
    # plt.figure(figsize=(8, 6))
    # for i in range(n_components_gmm):
    #     cluster_data = X_pca[gmm_labels == i]
    #     actual_label = cluster_to_digit_mapping[i]
    #     plt.scatter(cluster_data[:, 0], cluster_data[:, 1], label=f'Digit {actual_label}', s=10)

    # plt.xlabel('Principal Component 1')
    # plt.ylabel('Principal Component 2')
    # plt.title('GMM Clusters on MNIST Data (PCA-reduced) with Digit Labels')
    # plt.legend()
    # plt.show()

    return clusters

def _get_accuracy(ys_true: np.ndarray, ys_pred: np.ndarray) -> float:
    accuracy: float = accuracy_score(ys_true, ys_pred)
    return accuracy

def _get_confusion_matrix(ys_true: np.ndarray, ys_pred: np.ndarray) -> np.ndarray:
    cm: np.ndarray = confusion_matrix(ys_true, ys_pred)
    return cm

def _get_clusters(xs_pca: np.ndarray, gmm_labels: NDArray[np.int8]) -> Dict[int, np.ndarray]:
    clusters: Dict[int, np.ndarray] = {}
    for i in range(Environment().GMM_COMPONENTS):
        clusters[i] = xs_pca[gmm_labels == i]
    return clusters

def _get_cluster_to_digit_mappings(gmm_labels: np.ndarray, ys: np.ndarray) -> np.ndarray:
    cluster_to_digit_mapping: np.ndarray = np.zeros(Environment().GMM_COMPONENTS, dtype=int)
    for i in range(Environment().GMM_COMPONENTS):
        cluster_indices: np.ndarray = np.where(gmm_labels == i)[0]
        true_labels: np.ndarray = ys[cluster_indices]
        most_common_label = np.bincount(true_labels).argmax()
        cluster_to_digit_mapping[i] = most_common_label
    return cluster_to_digit_mapping



# def get_prediction(sample: MNISTSample) -> int:
#     validate_sample(sample)
#     xs, ys = load_train_data()
#     labels: List[int] = list(ys.unique())

#     priors: Dict[int, float] = _get_priors(xs, ys, labels)
#     means: Dict[int, np.ndarray] = _get_means(xs, ys, labels)
#     covariances: Dict[int, np.ndarray] = _get_covariances(xs, ys, labels)

#     log_posterios: Dict[int, np.ndarray] = _get_log_posteriors(sample, labels, means, covariances, priors)
#     posteriors: Dict[int, np.ndarray] = _normilize_posterios(log_posterios, labels)
#     pred = _get_most_likely_label(posteriors)
#     return int(pred)

# def get_sample(label: int) -> MNISTSample:
#     validate_label(label)
#     xs, ys = load_train_data()
#     labels: List[int] = list(ys.unique())
#     means: Dict[int, np.ndarray] = _get_means(xs, ys, labels)
#     covariances: Dict[int, np.ndarray] = _get_covariances(xs, ys, labels)
#     sample = multivariate_normal.rvs(means[label], covariances[label])
#     sample = _get_scaled_sample(sample)
#     return sample    

# def get_sample_mean(label: int) -> MNISTSample:
#     validate_label(label)
#     xs, ys = load_train_data()
#     labels: List[int] = list(ys.unique())
#     means: Dict[int, np.ndarray] = _get_means(xs, ys, labels)
#     sample_mean = _get_scaled_sample(means[label])
#     return sample_mean

# def _get_scaled_sample(sample: MNISTSample) -> MNISTSample:
#     min_val = sample.min()
#     max_val = sample.max()
#     normalized_sample = (sample - min_val) / (max_val - min_val)
#     scaled_sample = (normalized_sample * 255).astype(np.uint8)
#     return scaled_sample

# def _get_priors(xs: DataFrame, ys: Series, labels: List[int]) -> Dict[int, float]:
#     priors: Dict[int, float] = {}
#     for y in labels: 
#         priors[y] = len(xs[ys == y]) / len(xs)
#     return priors

# def _get_covariances(xs: DataFrame, ys: Series, labels: List[int]) -> Dict[int, np.ndarray]:
#     covariances: Dict[int, np.ndarray] = {}
#     for y in labels: 
#         covariances[y] = np.cov(xs[ys == y].T)
#     return covariances

# def _get_means(xs: DataFrame, ys: Series, labels: List[int]) -> Dict[int, np.ndarray]:
#     means: Dict[int, np.ndarray] = {}
#     for y in labels:
#         means[y] = xs[ys == y].mean().values
#     return means

# def _get_log_posteriors(sample: MNISTSample, labels: List[int], means: Dict[int, np.ndarray], covariances: Dict[int, np.ndarray], priors: Dict[int, float]) -> Dict[int, np.ndarray]:
#     log_posteriors: Dict[int, np.ndarray] = {}
#     for y in labels:
#         log_likelihood: np.ndarray = multivariate_normal.logpdf(sample, mean=means[y], cov=covariances[y], allow_singular=True)
#         log_posteriors[y] = log_likelihood + np.log(priors[y])
#     return log_posteriors

# def _normilize_posterios(log_posteriors: Dict[int, np.ndarray], labels: List[int]) -> Dict[int, np.ndarray]:
#     max_log_posterior = max(log_posteriors.values())
#     posteriors: Dict[int, np.ndarray] = {y: np.exp(log_posteriors[y] - max_log_posterior) for y in labels} # Prevent underflow with the log-sum-exp
#     total_posterior = sum(posteriors.values())
#     for y in labels:
#         posteriors[y] /= total_posterior
#     return posteriors

# def _get_most_likely_label(posteriors: Dict[int, np.ndarray]) -> int:
#     return max(posteriors, key=posteriors.get)
        