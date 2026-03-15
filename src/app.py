from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from core.models import PredictPayload
from core.gesture_registry import detect_gesture, get_gesture_label, GESTURE_LIBRARY

app = FastAPI(title="Gesture Word Input Demo")


@app.post("/predict")
def predict(payload: PredictPayload):
    gesture = detect_gesture(payload.landmarks)
    return {
        "gesture": gesture,
        "label": get_gesture_label(gesture),
    }


@app.get("/gesture-library")
def gesture_library():
    return {
        "library": GESTURE_LIBRARY
    }


app.mount("/", StaticFiles(directory="static", html=True), name="static")