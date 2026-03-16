from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from core.models import PredictPayload
from core.hand_role import HandRoleEngine
from core.text_library import TEXT_LIBRARY
from core.settings import SETTINGS

app = FastAPI(title="Gesture Word Input Demo")

# 全局动作引擎
engine = HandRoleEngine()


@app.get("/health")
def health():
    return {
        "ok": True,
        "service": "gesture-word-input-demo"
    }


@app.post("/predict")
def predict(payload: PredictPayload):
    """
    保留主接口：
    输入 landmarks
    输出:
    - gesture: 手势标签，例如 is_v_sign
    - code: 词语编码，例如 chr_a
    - label: 对应文本，例如 我看看
    - locked: 当前是否处于锁定状态
    - state: 当前动作引擎状态
    """
    result = engine.predict(payload.landmarks)

    return {
        "gesture": result.gesture,
        "code": result.code,
        "label": result.label,
        "locked": result.locked,
        "state": result.state,
    }


@app.post("/reset")
def reset_engine():
    """
    重置动作引擎状态
    比如清空锁定链路、退出复杂动作模式
    """
    engine.reset()
    return {
        "ok": True,
        "message": "engine reset"
    }


@app.get("/gesture-library")
def get_gesture_library():
    """
    查看当前动作引擎支持的手势标签与规则入口
    """
    return {
        "gestures": engine.get_gesture_library()
    }


@app.get("/text-library")
def get_text_library():
    """
    查看词语标签库
    例如 chr_a -> 我看看
    """
    return {
        "texts": TEXT_LIBRARY
    }


@app.get("/settings")
def get_settings():
    """
    查看当前阈值配置
    """
    return {
        "settings": SETTINGS
    }


# 静态页面
app.mount("/", StaticFiles(directory="static", html=True), name="static")