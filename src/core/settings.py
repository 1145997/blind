"""
settings.py

统一管理手势识别系统的所有参数

包括：
- 手势识别阈值
- 识别顺序
- 状态机时间
- 调试配置
"""

# ===============================
# 手势识别阈值
# ===============================

SETTINGS = {
    #
    "STABLE_FRAME_COUNT": 3,
    #防抖
    "GESTURE_DEBOUNCE_TIME": 1.5,
    # OK 手势：拇指食指距离
    "OK_DISTANCE_THRESHOLD": 0.06,

    # V 手势：食指中指横向间距
    "V_FINGER_GAP_THRESHOLD": 0.04,

    # CALL 手势：拇指展开距离
    "CALL_THUMB_OPEN_THRESHOLD": 0.07,

    # 手枪手势拇指张开
    "FINGER_GUN_THUMB_OPEN_THRESHOLD": 0.06,

    # 张开手掌拇指展开
    "OPEN_PALM_THUMB_THRESHOLD": 0.04,


    # ===============================
    # 手势识别顺序
    # ===============================

    # 越前面优先级越高
    "GESTURE_ORDER": [

        "is_thumbs_up",
        "is_thumbs_down",

        "is_v_sign",
        "is_v_down_sign",

        "is_point_up_sign",

        "is_three_sign",
        "is_four_sign",

        "is_open_palm",

        "is_rock_sign",
        "is_call_sign",

        "is_finger_gun",

        "is_fist",

        "is_ok_sign",

    ],


    # ===============================
    # 动作链状态机
    # ===============================

    # 手势输入超时（秒）
    "GESTURE_TIMEOUT": 1.5,

    # 锁定状态超时
    "LOCK_TIMEOUT": 3.0,

    # 连续识别稳定帧数
    "STABLE_FRAME_COUNT": 3,


    # ===============================
    # 识别过滤
    # ===============================

    # 最小手部置信度
    "MIN_HAND_CONFIDENCE": 0.5,

    # 防抖帧
    "DEBOUNCE_FRAMES": 2,


    # ===============================
    # 调试
    # ===============================

    # 打印识别日志
    "DEBUG_LOG": True,

    # 打印 landmark
    "DEBUG_LANDMARK": False,

}