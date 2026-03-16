from typing import Callable, Dict, List, Optional

from core.models import Landmark
from core.settings import SETTINGS


# =========================
# 基础几何工具
# =========================
def dist(a: Landmark, b: Landmark) -> float:
    dx = a.x - b.x
    dy = a.y - b.y
    dz = a.z - b.z
    return (dx * dx + dy * dy + dz * dz) ** 0.5


def finger_up(lm: List[Landmark], tip_id: int, pip_id: int) -> bool:
    # MediaPipe 图像坐标：越往上 y 越小
    return lm[tip_id].y < lm[pip_id].y


def finger_down(lm: List[Landmark], tip_id: int, pip_id: int) -> bool:
    return lm[tip_id].y > lm[pip_id].y


def valid_landmarks(lm: List[Landmark]) -> bool:
    return isinstance(lm, list) and len(lm) == 21


# =========================
# 手势识别规则
# 对外暴露统一使用 is_xxx_sign 命名
# =========================
def is_thumbs_up(lm: List[Landmark]) -> bool:
    if not valid_landmarks(lm):
        return False

    index_down = finger_down(lm, 8, 6)
    middle_down = finger_down(lm, 12, 10)
    ring_down = finger_down(lm, 16, 14)
    pinky_down = finger_down(lm, 20, 18)
    thumb_up = lm[4].y < lm[3].y

    return (
        thumb_up
        and index_down
        and middle_down
        and ring_down
        and pinky_down
    )


def is_thumbs_down(lm: List[Landmark]) -> bool:
    if not valid_landmarks(lm):
        return False

    index_down = finger_down(lm, 8, 6)
    middle_down = finger_down(lm, 12, 10)
    ring_down = finger_down(lm, 16, 14)
    pinky_down = finger_down(lm, 20, 18)
    thumb_down = lm[4].y > lm[3].y

    return (
        thumb_down
        and index_down
        and middle_down
        and ring_down
        and pinky_down
    )


def is_v_sign(lm: List[Landmark]) -> bool:
    if not valid_landmarks(lm):
        return False

    index_up = finger_up(lm, 8, 6)
    middle_up = finger_up(lm, 12, 10)
    ring_down = finger_down(lm, 16, 14)
    pinky_down = finger_down(lm, 20, 18)

    finger_gap = abs(lm[8].x - lm[12].x) > SETTINGS["V_FINGER_GAP_THRESHOLD"]

    return (
        index_up
        and middle_up
        and ring_down
        and pinky_down
        and finger_gap
    )


def is_v_down_sign(lm: List[Landmark]) -> bool:
    if not valid_landmarks(lm):
        return False

    index_down = finger_down(lm, 8, 6)
    middle_down = finger_down(lm, 12, 10)
    ring_up = finger_up(lm, 16, 14)
    pinky_up = finger_up(lm, 20, 18)

    return index_down and middle_down and ring_up and pinky_up


def is_point_up_sign(lm: List[Landmark]) -> bool:
    if not valid_landmarks(lm):
        return False

    index_up = finger_up(lm, 8, 6)
    middle_down = finger_down(lm, 12, 10)
    ring_down = finger_down(lm, 16, 14)
    pinky_down = finger_down(lm, 20, 18)

    return index_up and middle_down and ring_down and pinky_down


def is_three_sign(lm: List[Landmark]) -> bool:
    if not valid_landmarks(lm):
        return False

    index_up = finger_up(lm, 8, 6)
    middle_up = finger_up(lm, 12, 10)
    ring_up = finger_up(lm, 16, 14)
    pinky_down = finger_down(lm, 20, 18)

    return index_up and middle_up and ring_up and pinky_down


def is_four_sign(lm: List[Landmark]) -> bool:
    if not valid_landmarks(lm):
        return False

    index_up = finger_up(lm, 8, 6)
    middle_up = finger_up(lm, 12, 10)
    ring_up = finger_up(lm, 16, 14)
    pinky_up = finger_up(lm, 20, 18)

    # 拇指尽量收回，避免与 open_palm 混淆
    thumb_down = lm[4].x < lm[3].x or lm[4].y > lm[3].y

    return index_up and middle_up and ring_up and pinky_up and thumb_down


def is_open_palm(lm: List[Landmark]) -> bool:
    if not valid_landmarks(lm):
        return False

    index_up = finger_up(lm, 8, 6)
    middle_up = finger_up(lm, 12, 10)
    ring_up = finger_up(lm, 16, 14)
    pinky_up = finger_up(lm, 20, 18)
    thumb_open = dist(lm[4], lm[3]) > SETTINGS["OPEN_PALM_THUMB_THRESHOLD"]

    return index_up and middle_up and ring_up and pinky_up and thumb_open


def is_rock_sign(lm: List[Landmark]) -> bool:
    if not valid_landmarks(lm):
        return False

    index_up = finger_up(lm, 8, 6)
    middle_down = finger_down(lm, 12, 10)
    ring_down = finger_down(lm, 16, 14)
    pinky_up = finger_up(lm, 20, 18)

    return index_up and middle_down and ring_down and pinky_up


def is_call_sign(lm: List[Landmark]) -> bool:
    if not valid_landmarks(lm):
        return False

    thumb_open = dist(lm[4], lm[3]) > SETTINGS["CALL_THUMB_OPEN_THRESHOLD"]
    index_down = finger_down(lm, 8, 6)
    middle_down = finger_down(lm, 12, 10)
    ring_down = finger_down(lm, 16, 14)
    pinky_up = finger_up(lm, 20, 18)

    return (
        thumb_open
        and index_down
        and middle_down
        and ring_down
        and pinky_up
    )


def is_finger_gun(lm: List[Landmark]) -> bool:
    if not valid_landmarks(lm):
        return False

    index_up = finger_up(lm, 8, 6)
    middle_down = finger_down(lm, 12, 10)
    ring_down = finger_down(lm, 16, 14)
    pinky_down = finger_down(lm, 20, 18)
    thumb_open = dist(lm[4], lm[3]) > SETTINGS["FINGER_GUN_THUMB_OPEN_THRESHOLD"]

    return (
        index_up
        and middle_down
        and ring_down
        and pinky_down
        and thumb_open
    )


def is_fist(lm: List[Landmark]) -> bool:
    if not valid_landmarks(lm):
        return False

    fingers_down = 0
    for tip_id, pip_id in [(8, 6), (12, 10), (16, 14), (20, 18)]:
        if finger_down(lm, tip_id, pip_id):
            fingers_down += 1

    return fingers_down >= 4


def is_ok_sign(lm: List[Landmark]) -> bool:
    if not valid_landmarks(lm):
        return False

    thumb_index_close = dist(lm[4], lm[8]) < SETTINGS["OK_DISTANCE_THRESHOLD"]
    middle_up = finger_up(lm, 12, 10)
    ring_up = finger_up(lm, 16, 14)
    pinky_up = finger_up(lm, 20, 18)

    return thumb_index_close and middle_up and ring_up and pinky_up


# =========================
# 手势注册表
# hand_role.py 后面直接调用这里
# =========================
GestureFunc = Callable[[List[Landmark]], bool]

HAND_GESTURE_REGISTRY: Dict[str, GestureFunc] = {
    "is_thumbs_up": is_thumbs_up,
    "is_thumbs_down": is_thumbs_down,
    "is_v_sign": is_v_sign,
    "is_v_down_sign": is_v_down_sign,
    "is_point_up_sign": is_point_up_sign,
    "is_three_sign": is_three_sign,
    "is_four_sign": is_four_sign,
    "is_open_palm": is_open_palm,
    "is_rock_sign": is_rock_sign,
    "is_call_sign": is_call_sign,
    "is_finger_gun": is_finger_gun,
    "is_fist": is_fist,
    "is_ok_sign": is_ok_sign,
}


# =========================
# 工具接口
# =========================
def list_gesture_tags() -> List[str]:
    return list(HAND_GESTURE_REGISTRY.keys())


def get_gesture_func(tag: str) -> Optional[GestureFunc]:
    return HAND_GESTURE_REGISTRY.get(tag)


def detect_first_match(
    lm: List[Landmark],
    ordered_tags: Optional[List[str]] = None
) -> Optional[str]:
    """
    按顺序返回第一个命中的手势标签。
    如果不传 ordered_tags，则按默认注册顺序检测。
    """
    if not valid_landmarks(lm):
        return None

    tags = ordered_tags or list_gesture_tags()

    for tag in tags:
        func = HAND_GESTURE_REGISTRY.get(tag)
        if func and func(lm):
            return tag
    return None