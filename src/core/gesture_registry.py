from typing import Callable, List, Optional, Tuple
from core.models import Landmark
from core.gesture_rules import (
    is_ok_sign,
    is_v_sign,
    is_rock_sign,
    is_thumbs_up,
    is_call_sign,
    is_three_sign,
    is_point_up_sign,
)

GestureRule = Tuple[str, Callable[[List[Landmark]], bool]]

GESTURE_RULES: List[GestureRule] = [
    ("ok_sign", is_ok_sign),
    ("v_sign", is_v_sign),
    ("rock_sign", is_rock_sign),
    ("call_sign", is_call_sign),
    ("three_sign", is_three_sign),
    ("thumbs_up", is_thumbs_up),
    ("point_up_sign", is_point_up_sign),
]

GESTURE_LIBRARY = {
    "ok_sign": "进入输入",
    "v_sign": "我画的",
    "rock_sign": "这个角色",
    "thumbs_up": "怎么样",
    "call_sign": "还需要",
    "three_sign": "修改吗",
    "point_up_sign": "请看看",
}


def detect_gesture(landmarks: List[Landmark]) -> Optional[str]:
    if len(landmarks) != 21:
        return None

    for gesture_name, rule_func in GESTURE_RULES:
        if rule_func(landmarks):
            return gesture_name
    return None


def get_gesture_label(gesture_name: Optional[str]) -> Optional[str]:
    if gesture_name is None:
        return None
    return GESTURE_LIBRARY.get(gesture_name)