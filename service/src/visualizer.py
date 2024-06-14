import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

from src.utilities.environment import Environment
from src.validator import validate_sample
from src.dtos.mnist_sample import MNISTSample

def get_image(sample: MNISTSample) -> bytes:
    validate_sample(sample)
    sample_array = np.array(sample).reshape(28, 28)
    img_buffer = BytesIO()
    plt.imshow(sample_array, cmap='gray')
    plt.axis('off') 
    plt.savefig(img_buffer, format='png', bbox_inches='tight', pad_inches=0)
    plt.close()
    img_buffer.seek(0)
    return img_buffer.getvalue()