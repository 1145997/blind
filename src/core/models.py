from pydantic import BaseModel
from typing import List, Optional


class Landmark(BaseModel):
    x: float
    y: float
    z: float = 0.0


class PredictPayload(BaseModel):
    landmarks: List[Landmark]


class PredictResult(BaseModel):
    gesture: Optional[str] = None
    code: Optional[str] = None
    label: Optional[str] = None
    locked: bool = False
    state: str = "idle"