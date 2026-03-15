from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import math

app = FastAPI(title="Gesture Word Input Demo")


class Landmark(BaseModel):
    x: float
    y: float
    z: float = 0.0


class PredictPayload(BaseModel):
    landmarks: List[Landmark]


def dist(a: Landmark, b: Landmark) -> float:
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2 + (a.z - b.z) ** 2)


def finger_up(lm: List[Landmark], tip_id: int, pip_id: int) -> bool:
    return lm[tip_id].y < lm[pip_id].y


def finger_down(lm: List[Landmark], tip_id: int, pip_id: int) -> bool:
    return lm[tip_id].y > lm[pip_id].y


# 1) OK：拇指食指接近，中/无/小指伸直
def is_ok_sign(lm: List[Landmark]) -> bool:
    thumb_index_close = dist(lm[4], lm[8]) < 0.06
    middle_up = finger_up(lm, 12, 10)
    ring_up = finger_up(lm, 16, 14)
    pinky_up = finger_up(lm, 20, 18)
    return thumb_index_close and middle_up and ring_up and pinky_up


# 2) V：食指中指伸直并分开
def is_v_sign(lm: List[Landmark]) -> bool:
    index_up = finger_up(lm, 8, 6)
    middle_up = finger_up(lm, 12, 10)
    ring_down = finger_down(lm, 16, 14)
    pinky_down = finger_down(lm, 20, 18)
    finger_gap = abs(lm[8].x - lm[12].x) > 0.04
    return index_up and middle_up and ring_down and pinky_down and finger_gap


# 3) Rock：食指、小指伸直
def is_rock_sign(lm: List[Landmark]) -> bool:
    index_up = finger_up(lm, 8, 6)
    middle_down = finger_down(lm, 12, 10)
    ring_down = finger_down(lm, 16, 14)
    pinky_up = finger_up(lm, 20, 18)
    return index_up and middle_down and ring_down and pinky_up


# 4) 点赞：拇指竖起，其余弯曲
def is_thumbs_up(lm: List[Landmark]) -> bool:
    index_down = finger_down(lm, 8, 6)
    middle_down = finger_down(lm, 12, 10)
    ring_down = finger_down(lm, 16, 14)
    pinky_down = finger_down(lm, 20, 18)
    thumb_up = lm[4].y < lm[3].y
    return thumb_up and index_down and middle_down and ring_down and pinky_down


# 5) Call：拇指 + 小指伸直
def is_call_sign(lm: List[Landmark]) -> bool:
    thumb_open = abs(lm[4].x - lm[3].x) > 0.05 or lm[4].y < lm[3].y
    index_down = finger_down(lm, 8, 6)
    middle_down = finger_down(lm, 12, 10)
    ring_down = finger_down(lm, 16, 14)
    pinky_up = finger_up(lm, 20, 18)
    return thumb_open and index_down and middle_down and ring_down and pinky_up


# 6) Three：食指、中指、无名指伸直；小指弯曲
def is_three_sign(lm: List[Landmark]) -> bool:
    index_up = finger_up(lm, 8, 6)
    middle_up = finger_up(lm, 12, 10)
    ring_up = finger_up(lm, 16, 14)
    pinky_down = finger_down(lm, 20, 18)
    return index_up and middle_up and ring_up and pinky_down


# 7) Point Up：只有食指伸直
def is_point_up_sign(lm: List[Landmark]) -> bool:
    index_up = finger_up(lm, 8, 6)
    middle_down = finger_down(lm, 12, 10)
    ring_down = finger_down(lm, 16, 14)
    pinky_down = finger_down(lm, 20, 18)
    return index_up and middle_down and ring_down and pinky_down


def detect_gesture(lm: List[Landmark]) -> Optional[str]:
    if len(lm) != 21:
        return None

    if is_ok_sign(lm):
        return "ok_sign"
    if is_v_sign(lm):
        return "v_sign"
    if is_rock_sign(lm):
        return "rock_sign"
    if is_call_sign(lm):
        return "call_sign"
    if is_three_sign(lm):
        return "three_sign"
    if is_thumbs_up(lm):
        return "thumbs_up"
    if is_point_up_sign(lm):
        return "point_up_sign"

    return None


GESTURE_LIBRARY = {
    "ok_sign": "进入输入",
    "v_sign": "我画的",
    "rock_sign": "这个角色",
    "thumbs_up": "怎么样",
    "call_sign": "还需要",
    "three_sign": "修改吗",
    "point_up_sign": "请看看",
}


@app.post("/predict")
def predict(payload: PredictPayload):
    gesture = detect_gesture(payload.landmarks)
    return {
        "gesture": gesture,
        "label": GESTURE_LIBRARY.get(gesture),
    }


@app.get("/gesture-library")
def gesture_library():
    return {
        "library": GESTURE_LIBRARY
    }


app.mount("/", StaticFiles(directory="static", html=True), name="static")