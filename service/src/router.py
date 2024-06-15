import uuid
import numpy as np
from typing import Dict
from numpy.typing import NDArray
from fastapi import APIRouter, Body, Response
from loguru import logger
from starlette.responses import JSONResponse
from src.dtos.mnist_sample import MNISTSample
from src.utilities.exceptions import SampleValidationException, LabelValidationException, ModelNotInitializedException
from src.ml_controller import initialize_model, get_clusters_evaluation, generate_sample
from src.visualizer import get_sample_image, get_cluster_image, get_confusion_matrix_image
import traceback

router = APIRouter()

@router.post('/initialize')
def initialize():
    try:
        initialize_model()
        return {'message': 'Model initialized successfully'}
    except Exception as e:
        logger.error('[GENERIC ERROR]')
        logger.error(traceback.format_exc())
        return JSONResponse(content={'error': 'Server failed to process request'}, status_code=500)

@router.get('/confusion_matrix')
def get_confusion_matrix():
    try:
        _, _, accuracy, confusion_matrix = get_clusters_evaluation()
        image_confusion_matrix: bytes = get_confusion_matrix_image(confusion_matrix, accuracy)
        headers_confusion_matrix = {'Content-Disposition': 'inline; filename=f"confusion_matrix_{uuid.uuid4()}.png"'}
        return Response(image_confusion_matrix, headers=headers_confusion_matrix, media_type='image/png')        
    except ModelNotInitializedException as e:
        return JSONResponse(content={'error': e.detail}, status_code=e.status_code)
    except Exception as e:
        logger.error('[GENERIC ERROR]')
        logger.error(traceback.format_exc())
        return JSONResponse(content={'error': 'Server failed to process request'}, status_code=500)

@router.get('/clusters')
def get_clusters():
    try:
        clusters, cluster_to_digit_mapping, _, _ = get_clusters_evaluation()
        image_clusters: bytes = get_cluster_image(clusters, cluster_to_digit_mapping)
        headers_clusters = {'Content-Disposition': 'inline; filename=f"clusters_{image_uuid}.png"'}
        return Response(image_clusters, headers=headers_clusters, media_type='image/png')
    except ModelNotInitializedException as e:
        return JSONResponse(content={'error': e.detail}, status_code=e.status_code)
    except Exception as e:
        logger.error('[GENERIC ERROR]')
        logger.error(traceback.format_exc())
        return JSONResponse(content={'error': 'Server failed to process request'}, status_code=500)

@router.get('/sample')
def get_sample(label: int):
    try:
        xs: np.ndarray = generate_sample(label)
        image: bytes = get_sample_image(xs)
        headers = {'Content-Disposition': 'inline; filename=f"sample_{image_uuid}.png"'}
        return Response(image, headers=headers, media_type='image/png')
    except ModelNotInitializedException as e:
        return JSONResponse(content={'error': e.detail}, status_code=e.status_code)
    except Exception as e:
        logger.error('[GENERIC ERROR]')
        logger.error(traceback.format_exc())
        return JSONResponse(content={'error': 'Server failed to process request'}, status_code=500)


# @router.post('/predict')
# def predict(sample: MNISTSample = Body(..., example=[0]*784)):
#     try:
#         pred = get_prediction(sample)
#         return {'prediction': pred}
#     except SampleValidationException as e:
#         return JSONResponse(content={'error': e.detail}, status_code=e.status_code)
#     except Exception as e:
#         logger.error('[GENERIC ERROR]')
#         logger.error(traceback.format_exc())
#         return JSONResponse(content={'error': 'Server failed to process request'}, status_code=500)

# @router.get('/sample')
# def sample(label: int):
#     try: 
#         sample: MNISTSample = get_sample(label)
#         image: bytes = get_image(sample)
#         headers = {'Content-Disposition': 'inline; filename=f"{uuid.uuid4()}.png"'}
#         return Response(image, headers=headers, media_type='image/png')
#     except LabelValidationException as e:
#         return JSONResponse(content={'error': e.detail}, status_code=e.status_code)
#     except SampleValidationException as e:
#         return JSONResponse(content={'error': e.detail}, status_code=e.status_code)
#     except Exception as e:
#         logger.error('[GENERIC ERROR]')
#         logger.error(traceback.format_exc())
#         return JSONResponse(content={'error': 'Server failed to process request'}, status_code=500)

# @router.get('/sample_mean')
# def sample(label: int):
#     try: 
#         sample: MNISTSample = get_sample_mean(label)
#         image: bytes = get_image(sample)
#         headers = {'Content-Disposition': 'inline; filename=f"{uuid.uuid4()}.png"'}
#         return Response(image, headers=headers, media_type='image/png')
#     except LabelValidationException as e:
#         return JSONResponse(content={'error': e.detail}, status_code=e.status_code)
#     except SampleValidationException as e:
#         return JSONResponse(content={'error': e.detail}, status_code=e.status_code)
#     except Exception as e:
#         logger.error('[GENERIC ERROR]')
#         logger.error(traceback.format_exc())
#         return JSONResponse(content={'error': 'Server failed to process request'}, status_code=500)

# @router.post('/visualize')
# def save(sample: MNISTSample = Body(..., example=[0]*784)):
#     try:
#         image: bytes = get_image(sample)
#         headers = {'Content-Disposition': 'inline; filename=f"{uuid.uuid4()}.png"'}
#         return Response(image, headers=headers, media_type='image/png')
#     except SampleValidationException as e:
#         return JSONResponse(content={'error': e.detail}, status_code=e.status_code)
#     except Exception as e:
#         logger.error('[GENERIC ERROR]')
#         logger.error(traceback.format_exc())
#         return JSONResponse(content={'error': 'Server failed to process request'}, status_code=500)