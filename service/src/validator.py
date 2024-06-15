from typing import Union
from src.utilities.exceptions import InvalidSampleLengthException, InvalidSamplePixelValueException, LabelValidationException, ModelNotInitializedException
from src.dtos.mnist_sample import MNISTSample
from sklearn.mixture import GaussianMixture

def validate_sample(sample: MNISTSample) -> None:
    if len(sample) != 784:
        raise InvalidSampleLengthException(len(sample))
    if not all(0 <= pixel <= 255 for pixel in sample):
        raise InvalidSamplePixelValueException()
    
def validate_label(label: int) -> None:
    if label < 0 or label > 9:
        raise LabelValidationException(label)
    
def validate_model(model: Union[None, GaussianMixture]) -> None:
    if model is None:
        raise ModelNotInitializedException()