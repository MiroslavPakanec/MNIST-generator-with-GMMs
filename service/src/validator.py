from typing import Dict, Union
from src.utilities.exceptions import InvalidSampleLengthException, InvalidSamplePixelValueException, LabelValidationException, ModelNotInitializedException
from src.dtos.mnist_sample import MNISTSample
from sklearn.mixture import GaussianMixture
from sklearn.decomposition import PCA

def validate_sample(sample: MNISTSample) -> None:
    if len(sample) != 784:
        raise InvalidSampleLengthException(len(sample))
    if not all(0 <= pixel <= 255 for pixel in sample):
        raise InvalidSamplePixelValueException()
    
def validate_label(label: int) -> None:
    if label < 0 or label > 9:
        raise LabelValidationException(label)
    
def validate_initialization_dicts(model_dict: Dict[int, GaussianMixture], pca_dict: Dict[int, PCA], label: int) -> None:
    if label not in model_dict.keys():
        raise ModelNotInitializedException()
    if label not in pca_dict.keys():
        raise ModelNotInitializedException()