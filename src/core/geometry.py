import math
from typing import List
from core.models import Landmark


def dist(a: Landmark, b: Landmark) -> float:
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2 + (a.z - b.z) ** 2)


def finger_up(lm: List[Landmark], tip_id: int, pip_id: int) -> bool:
    return lm[tip_id].y < lm[pip_id].y


def finger_down(lm: List[Landmark], tip_id: int, pip_id: int) -> bool:
    return lm[tip_id].y > lm[pip_id].y