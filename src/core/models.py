from pydantic import BaseModel
from typing import List


class Landmark(BaseModel):
    x: float
    y: float
    z: float = 0.0


class PredictPayload(BaseModel):
    landmarks: List[Landmark]