from dataclasses import dataclass
from time import time
from typing import List, Optional

from core.models import Landmark, PredictResult
from core.settings import SETTINGS
from core.hand_library import detect_first_match
from core.text_library import (
    get_code_by_gesture,
    get_code_by_sequence,
    get_text_by_code,
)


@dataclass
class LockContext:
    """
    锁定上下文
    例如：
    识别到 is_four_sign 后进入锁定
    后续只允许识别指定动作
    """
    active: bool = False
    trigger_gesture: Optional[str] = None
    allowed_next_gestures: Optional[List[str]] = None
    started_at: float = 0.0


class HandRoleEngine:
    """
    动作调度引擎

    功能：
    1. 普通手势识别 -> 单动作文本
    2. 锁定动作链识别 -> 多动作组合文本
    3. 超时退出锁定
    """

    def __init__(self) -> None:
        self.state = "idle"
        self.lock_ctx = LockContext()
        self.last_gesture: Optional[str] = None
        self.last_code: Optional[str] = None
        self.last_label: Optional[str] = None

    # =========================
    # 对外接口
    # =========================
    def reset(self) -> None:
        self.state = "idle"
        self.lock_ctx = LockContext()
        self.last_gesture = None
        self.last_code = None
        self.last_label = None

    def get_gesture_library(self) -> List[str]:
        return SETTINGS["GESTURE_ORDER"]

    def predict(self, landmarks: List[Landmark]) -> PredictResult:
        """
        对外统一预测接口
        """
        self._check_lock_timeout()

        gesture = detect_first_match(
            landmarks,
            ordered_tags=SETTINGS["GESTURE_ORDER"]
        )

        if SETTINGS.get("DEBUG_LOG", False):
            print(f"[HandRoleEngine] state={self.state}, gesture={gesture}")

        if gesture is None:
            return PredictResult(
                gesture=None,
                code=None,
                label=None,
                locked=self.lock_ctx.active,
                state=self.state,
            )

        # 先看当前是否处于锁定模式
        if self.lock_ctx.active:
            return self._predict_in_lock(gesture)

        # 普通模式识别
        return self._predict_normal(gesture)

    # =========================
    # 内部逻辑
    # =========================
    def _predict_normal(self, gesture: str) -> PredictResult:
        """
        普通模式：
        - 普通手势直接映射文本
        - 特定手势触发锁定
        """

        # 例：识别到 is_four_sign 进入锁定
        if gesture == "is_four_sign":
            self._enter_lock(
                trigger_gesture=gesture,
                allowed_next_gestures=["is_v_sign"]
            )

            code = get_code_by_gesture(gesture)
            label = get_text_by_code(code)

            self._update_last(gesture, code, label)

            return PredictResult(
                gesture=gesture,
                code=code,
                label=label,
                locked=True,
                state=self.state,
            )

        # 普通单动作识别
        code = get_code_by_gesture(gesture)
        label = get_text_by_code(code)

        self._update_last(gesture, code, label)

        return PredictResult(
            gesture=gesture,
            code=code,
            label=label,
            locked=False,
            state=self.state,
        )

    def _predict_in_lock(self, gesture: str) -> PredictResult:
        """
        锁定模式：
        - 只允许指定后续手势
        - 用 (trigger, current) 查复杂动作链
        - 命中后自动退出锁定
        """

        if not self.lock_ctx.active:
            return PredictResult(
                gesture=gesture,
                code=None,
                label=None,
                locked=False,
                state=self.state,
            )

        # 不在允许列表里，忽略或直接退出
        if (
            self.lock_ctx.allowed_next_gestures
            and gesture not in self.lock_ctx.allowed_next_gestures
        ):
            if SETTINGS.get("DEBUG_LOG", False):
                print(
                    f"[HandRoleEngine] lock active but gesture {gesture} "
                    f"not in allowed {self.lock_ctx.allowed_next_gestures}"
                )

            return PredictResult(
                gesture=gesture,
                code=None,
                label=None,
                locked=True,
                state=self.state,
            )

        # 复杂动作链查表
        seq = (self.lock_ctx.trigger_gesture, gesture)
        code = get_code_by_sequence(seq)
        label = get_text_by_code(code)

        # 命中后退出锁定
        self._exit_lock()

        self._update_last(gesture, code, label)

        return PredictResult(
            gesture=gesture,
            code=code,
            label=label,
            locked=False,
            state=self.state,
        )

    def _enter_lock(
        self,
        trigger_gesture: str,
        allowed_next_gestures: Optional[List[str]] = None
    ) -> None:
        self.lock_ctx = LockContext(
            active=True,
            trigger_gesture=trigger_gesture,
            allowed_next_gestures=allowed_next_gestures or [],
            started_at=time(),
        )
        self.state = "locked"

        if SETTINGS.get("DEBUG_LOG", False):
            print(
                f"[HandRoleEngine] enter lock: trigger={trigger_gesture}, "
                f"allowed={allowed_next_gestures}"
            )

    def _exit_lock(self) -> None:
        if SETTINGS.get("DEBUG_LOG", False):
            print("[HandRoleEngine] exit lock")

        self.lock_ctx = LockContext()
        self.state = "idle"

    def _check_lock_timeout(self) -> None:
        if not self.lock_ctx.active:
            return

        timeout_s = SETTINGS["LOCK_TIMEOUT"]
        now = time()

        if now - self.lock_ctx.started_at > timeout_s:
            if SETTINGS.get("DEBUG_LOG", False):
                print("[HandRoleEngine] lock timeout")
            self._exit_lock()

    def _update_last(
        self,
        gesture: Optional[str],
        code: Optional[str],
        label: Optional[str]
    ) -> None:
        self.last_gesture = gesture
        self.last_code = code
        self.last_label = label