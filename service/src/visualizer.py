import seaborn as sns
import numpy as np
from io import BytesIO
from typing import Dict
import matplotlib.pyplot as plt
from numpy.typing import NDArray
from src.utilities.environment import Environment
from src.validator import validate_sample

def get_sample_image(sample: np.ndarray) -> bytes:
    validate_sample(sample)
    sample_array = np.array(sample).reshape(28, 28)
    img_buffer = BytesIO()
    plt.imshow(sample_array, cmap='gray')
    plt.axis('off') 
    plt.savefig(img_buffer, format='png', bbox_inches='tight', pad_inches=0)
    plt.close()
    img_buffer.seek(0)
    return img_buffer.getvalue()

def get_cluster_image(clusters: Dict[int, np.ndarray], cluster_to_digit_mapping: NDArray[np.int64]) -> bytes:
    img_buffer = BytesIO()
    for key, cluster in clusters.items():
        plt.scatter(cluster[:, 0], cluster[:, 1], label=f'Digit: {cluster_to_digit_mapping[key]}', s=10)
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.title('GMM Clusters on MNIST Data (PCA-reduced)')
    plt.legend()
    plt.savefig(img_buffer, format='png', bbox_inches='tight', pad_inches=0)
    plt.close()
    img_buffer.seek(0)
    return img_buffer.getvalue()

def get_confusion_matrix_image(confusion_matrix: np.ndarray, accuracy: float) -> bytes:
    sns.heatmap(confusion_matrix, annot=True, fmt='d', cmap='Blues')
    plt.xlabel('Predicted Labels')
    plt.ylabel('True Labels')
    plt.title(f'Confusion Matrix (accuracy - {accuracy:.2f})')

    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf.getvalue()