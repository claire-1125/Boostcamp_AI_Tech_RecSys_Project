from typing import Any

import joblib
from core.errors import PredictException
from fastapi import APIRouter, HTTPException
from loguru import logger
from models.prediction import HealthResponse, MachineLearningResponse
from services.predict import MachineLearningModelHandlerScore as model

router = APIRouter()

get_prediction = lambda u_id, r_id: MachineLearningResponse(prediction=
    model.predict(u_id, r_id, load_wrapper=joblib.load, method="predict_proba")
)


@router.get("/predict", response_model=MachineLearningResponse, name="predict:get-data")
async def predict(u_id: Any = None, r_id: Any = None):
    if not u_id:
        raise HTTPException(status_code=404, detail=f"u_id : {u_id} argument invalid!")
    try:
        prediction = get_prediction(u_id, r_id)
        print("pre")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Exception: {e}")
        # raise HTTPException(status_code=500, detail=f"u_id : {u_id}, r_id: {r_id} argument invalid!")

    return prediction
    #return MachineLearningResponse(prediction=prediction)


@router.get(
    "/health", response_model=HealthResponse, name="health:get-data",
)
async def health():
    is_health = False
    try:
        get_prediction("lorem ipsum")
        is_health = True
        return HealthResponse(status=is_health)
    except Exception:
        raise HTTPException(status_code=404, detail="Unhealthy")
