from pydantic import BaseModel
from typing import Optional


class MachineLearningResponse(BaseModel):
    prediction: dict


class HealthResponse(BaseModel):
    status: bool
