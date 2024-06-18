import numpy as np
from io import BytesIO
from typing import Dict
import matplotlib.pyplot as plt

def get_sample_image(sample: np.ndarray, label: int) -> bytes:
    sample_array = np.array(sample).reshape(28, 28)
    img_buffer = BytesIO()
    plt.imshow(sample_array, cmap='gray')
    plt.axis('off') 
    plt.title(f'Sample of digit: {label}')
    plt.savefig(img_buffer, format='png', bbox_inches='tight', pad_inches=0)
    plt.close()
    img_buffer.seek(0)
    return img_buffer.getvalue()

def get_clusters_image(clusters: Dict[int, np.ndarray], label: int) -> bytes:
    img_buffer = BytesIO()
    plt.figure(figsize=(10, 8))
    for key, cluster in clusters.items():
        plt.scatter(cluster[:, 0], cluster[:, 1], label=f'Cluster: {key}', s=10)
        plt.xlabel('Principal Component 1')
        plt.ylabel('Principal Component 2')
        plt.title(f'GMM Clusters on MNIST Data (PCA-reduced), Digit {label}')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left') 
    plt.tight_layout()
    plt.savefig(img_buffer, format='png', bbox_inches='tight', pad_inches=0)
    plt.close()
    img_buffer.seek(0)
    return img_buffer.getvalue()