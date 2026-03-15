from typing import List
from core.models import Landmark
from core.geometry import dist, finger_up, finger_down
from core.settings import (
    OK_DISTANCE_THRESHOLD,
    V_FINGER_GAP_THRESHOLD,
    CALL_THUMB_OPEN_THRESHOLD,
)


def is_ok_sign(lm: List[Landmark]) -> bool:
    thumb_index_close = dist(lm[4], lm[8]) < OK_DISTANCE_THRESHOLD
    middle_up = finger_up(lm, 12, 10)
    ring_up = finger_up(lm, 16, 14)
    pinky_up = finger_up(lm, 20, 18)
    return thumb_index_close and middle_up and ring_up and pinky_up


def is_v_sign(lm: List[Landmark]) -> bool:
    index_up = finger_up(lm, 8, 6)
    middle_up = finger_up(lm, 12, 10)
    ring_down = finger_down(lm, 16, 14)
    pinky_down = finger_down(lm, 20, 18)
    finger_gap = abs(lm[8].x - lm[12].x) > V_FINGER_GAP_THRESHOLD
    return index_up and middle_up and ring_down and pinky_down and finger_gap


def is_rock_sign(lm: List[Landmark]) -> bool:
    index_up = finger_up(lm, 8, 6)
    middle_down = finger_down(lm, 12, 10)
    ring_down = finger_down(lm, 16, 14)
    pinky_up = finger_up(lm, 20, 18)
    return index_up and middle_down and ring_down and pinky_up


def is_thumbs_up(lm: List[Landmark]) -> bool:
    index_down = finger_down(lm, 8, 6)
    middle_down = finger_down(lm, 12, 10)
    ring_down = finger_down(lm, 16, 14)
    pinky_down = finger_down(lm, 20, 18)
    thumb_up = lm[4].y < lm[3].y
    return thumb_up and index_down and middle_down and ring_down and pinky_down


def is_call_sign(lm: List[Landmark]) -> bool:
    thumb_open = abs(lm[4].x - lm[3].x) > CALL_THUMB_OPEN_THRESHOLD or lm[4].y < lm[3].y
    index_down = finger_down(lm, 8, 6)
    middle_down = finger_down(lm, 12, 10)
    ring_down = finger_down(lm, 16, 14)
    pinky_up = finger_up(lm, 20, 18)
    return thumb_open and index_down and middle_down and ring_down and pinky_up


def is_three_sign(lm: List[Landmark]) -> bool:
    index_up = finger_up(lm, 8, 6)
    middle_up = finger_up(lm, 12, 10)
    ring_up = finger_up(lm, 16, 14)
    pinky_down = finger_down(lm, 20, 18)
    return index_up and middle_up and ring_up and pinky_down


def is_point_up_sign(lm: List[Landmark]) -> bool:
    index_up = finger_up(lm, 8, 6)
    middle_down = finger_down(lm, 12, 10)
    ring_down = finger_down(lm, 16, 14)
    pinky_down = finger_down(lm, 20, 18)
    return index_up and middle_down and ring_down and pinky_down