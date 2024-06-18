import uuid
import numpy as np
from typing import Dict
from numpy.typing import NDArray
from fastapi import APIRouter, Body, Response
from loguru import logger
from starlette.responses import JSONResponse
from src.dtos.mnist_sample import MNISTSample
from src.utilities.exceptions import SampleValidationException, LabelValidationException, ModelNotInitializedException
import src.ml_controller as ml_controller 
import src.visualizer as visualizer
import traceback

router = APIRouter()

@router.post('/initialize')
def initialize():
    try:
        ml_controller.initialize()
        return {'message': 'Model initialized successfully'}
    except Exception as e:
        logger.error('[GENERIC ERROR]')
        logger.error(traceback.format_exc())
        return JSONResponse(content={'error': 'Server failed to process request'}, status_code=500)

@router.get('/clusters_image')
def get_clusters(label: int):
    try:
        clusters: Dict[int, np.ndarray] = ml_controller.get_clusters(label)
        clusters_image: bytes = visualizer.get_clusters_image(clusters, label)
        headers_clusters = {'Content-Disposition': 'inline; filename=f"clusters_{image_uuid}.png"'}
        return Response(clusters_image, headers=headers_clusters, media_type='image/png')
    except ModelNotInitializedException as e:
        return JSONResponse(content={'error': e.detail}, status_code=e.status_code)
    except Exception as e:
        logger.error('[GENERIC ERROR]')
        logger.error(traceback.format_exc())
        return JSONResponse(content={'error': 'Server failed to process request'}, status_code=500)

@router.get('/sample_image')
def get_sample(label: int):
    try:
        x: np.ndarray = ml_controller.generate_sample(label)
        image: bytes = visualizer.get_sample_image(x, label)
        headers = {'Content-Disposition': 'inline; filename=f"sample_{image_uuid}.png"'}
        return Response(image, headers=headers, media_type='image/png')
    except ModelNotInitializedException as e:
        return JSONResponse(content={'error': e.detail}, status_code=e.status_code)
    except Exception as e:
        logger.error('[GENERIC ERROR]')
        logger.error(traceback.format_exc())
        return JSONResponse(content={'error': 'Server failed to process request'}, status_code=500)

@router.get('/sample')
def get_sample(label: int):
    try:
        x: np.ndarray = ml_controller.generate_sample(label)
        result = x.flatten().tolist()
        return result
    except ModelNotInitializedException as e:
        return JSONResponse(content={'error': e.detail}, status_code=e.status_code)
    except Exception as e:
        logger.error('[GENERIC ERROR]')
        logger.error(traceback.format_exc())
        return JSONResponse(content={'error': 'Server failed to process request'}, status_code=500)