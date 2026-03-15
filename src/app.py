from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import math

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
# 手势输出映射
# 你后面改这里就行
# ------------------------
GESTURE_TEXT_MAP = {
    "ok_sign": "你好",
    "v_sign": "谢谢",
    "thumbs_up": "同意",
    "point_up": "请看这里",
    "rock_sign": "启动模式",
}


# ------------------------
# 工具函数
# ------------------------
def dist(a: Landmark, b: Landmark) -> float:
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2 + (a.z - b.z) ** 2)


def finger_up(lm: List[Landmark], tip_id: int, pip_id: int) -> bool:
    return lm[tip_id].y < lm[pip_id].y


def finger_down(lm: List[Landmark], tip_id: int, pip_id: int) -> bool:
    return lm[tip_id].y > lm[pip_id].y


# ------------------------
# 手势判断
# ------------------------

# 1. OK 手势：拇指食指相碰，中无小三指伸直
def is_ok_sign(lm: List[Landmark]) -> bool:
    thumb_index_close = dist(lm[4], lm[8]) < 0.06
    middle_up = finger_up(lm, 12, 10)
    ring_up = finger_up(lm, 16, 14)
    pinky_up = finger_up(lm, 20, 18)
    return thumb_index_close and middle_up and ring_up and pinky_up


# 2. V 手势：食指中指伸直并分开，无名指小指弯曲
def is_v_sign(lm: List[Landmark]) -> bool:
    index_up = finger_up(lm, 8, 6)
    middle_up = finger_up(lm, 12, 10)
    ring_down = finger_down(lm, 16, 14)
    pinky_down = finger_down(lm, 20, 18)
    finger_gap = abs(lm[8].x - lm[12].x) > 0.04
    return index_up and middle_up and ring_down and pinky_down and finger_gap


# 3. 点赞：拇指伸直，其余四指弯曲
def is_thumbs_up(lm: List[Landmark]) -> bool:
    index_down = finger_down(lm, 8, 6)
    middle_down = finger_down(lm, 12, 10)
    ring_down = finger_down(lm, 16, 14)
    pinky_down = finger_down(lm, 20, 18)

    # 拇指竖起：thumb_tip 比 thumb_ip 更高
    thumb_up = lm[4].y < lm[3].y

    return thumb_up and index_down and middle_down and ring_down and pinky_down


# 4. 食指指天：食指伸直，其余弯曲
def is_point_up(lm: List[Landmark]) -> bool:
    index_up = finger_up(lm, 8, 6)
    middle_down = finger_down(lm, 12, 10)
    ring_down = finger_down(lm, 16, 14)
    pinky_down = finger_down(lm, 20, 18)

    # 拇指放松，避免误判成枪手势
    thumb_not_wide = abs(lm[4].x - lm[3].x) < 0.08

    return index_up and middle_down and ring_down and pinky_down and thumb_not_wide


# 5. Rock 手势：食指、小指伸直，中指无名指弯曲
def is_rock_sign(lm: List[Landmark]) -> bool:
    index_up = finger_up(lm, 8, 6)
    middle_down = finger_down(lm, 12, 10)
    ring_down = finger_down(lm, 16, 14)
    pinky_up = finger_up(lm, 20, 18)
    return index_up and middle_down and ring_down and pinky_up


# ------------------------
# 手势识别总入口
# 返回的是手势名，不是文本
# ------------------------
def detect_gesture(lm: List[Landmark]) -> Optional[str]:
    if len(lm) != 21:
        return None

    # 注意顺序：越特殊的手势越先判
    if is_ok_sign(lm):
        return "ok_sign"
    if is_v_sign(lm):
        return "v_sign"
    if is_thumbs_up(lm):
        return "thumbs_up"
    if is_point_up(lm):
        return "point_up"
    if is_rock_sign(lm):
        return "rock_sign"

    return None


# ------------------------
# 旧接口：直接返回文字
# ------------------------
@app.post("/predict")
def predict(payload: HandPayload):
    gesture = detect_gesture(payload.landmarks)
    text = GESTURE_TEXT_MAP.get(gesture, "未识别")
    return {
        "gesture": gesture,
        "text": text
    }


# ------------------------
# 新接口1：查看当前支持哪些手势
# ------------------------
@app.get("/gestures")
def get_gestures():
    return {
        "supported_gestures": list(GESTURE_TEXT_MAP.keys()),
        "mapping": GESTURE_TEXT_MAP
    }


# ------------------------
# 新接口2：按手势名取默认话术
# 方便你前端或别的地方单独调用
# ------------------------
@app.get("/gesture-text/{gesture_name}")
def get_gesture_text(gesture_name: str):
    text = GESTURE_TEXT_MAP.get(gesture_name)
    if text is None:
        return {"gesture": gesture_name, "text": None, "found": False}
    return {"gesture": gesture_name, "text": text, "found": True}


# 静态页面
app.mount("/", StaticFiles(directory="static", html=True), name="static")