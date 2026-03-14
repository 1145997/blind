from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Sign Language Demo")

# ------------------------
# 数据结构
# ------------------------
class Landmark(BaseModel):
    x: float
    y: float
    z: float = 0.0

class HandPayload(BaseModel):
    landmarks: List[Landmark]


# ------------------------
# 简单规则识别
# MediaPipe Hands 21点:
# 4 thumb_tip
# 8 index_tip
# 12 middle_tip
# 16 ring_tip
# 20 pinky_tip
# 6/10/14/18 对应各指PIP关节
# ------------------------
def is_open_palm(lm: List[Landmark]) -> bool:
    # 对于除拇指外的四指，tip 在 pip 上方（图像坐标 y 更小）判定为伸直
    fingers_up = 0
    for tip_id, pip_id in [(8, 6), (12, 10), (16, 14), (20, 18)]:
        if lm[tip_id].y < lm[pip_id].y:
            fingers_up += 1

    # 拇指简单判定：thumb_tip 与 thumb_ip/关节有明显横向展开
    thumb_open = abs(lm[4].x - lm[3].x) > 0.03

    return fingers_up >= 4 and thumb_open


def is_fist(lm: List[Landmark]) -> bool:
    # 四指 tip 在 pip 下方（y 更大）近似判定为握拳
    fingers_down = 0
    for tip_id, pip_id in [(8, 6), (12, 10), (16, 14), (20, 18)]:
        if lm[tip_id].y > lm[pip_id].y:
            fingers_down += 1

    return fingers_down >= 4


def translate_sign(lm: List[Landmark]) -> str:
    if len(lm) != 21:
        return "未检测到完整手部关键点"

    if is_open_palm(lm):
        return "你好"
    elif is_fist(lm):
        return "谢谢"
    else:
        return "未识别"


@app.post("/predict")
def predict(payload: HandPayload):
    result = translate_sign(payload.landmarks)
    return {"text": result}


# 静态页面
app.mount("/", StaticFiles(directory="static", html=True), name="static")