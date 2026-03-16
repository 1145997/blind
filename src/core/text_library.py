from typing import Dict, List, Optional, Tuple


# =====================================
# 1) 词语库
# code -> text
# =====================================
TEXT_LIBRARY: Dict[str, str] = {
    "chr_a": "我看看",
    "chr_b": "好的",
    "chr_c": "请再改一下",
    "chr_d": "这个角色",
    "chr_e": "还需要",
    "chr_f": "修改吗",
    "chr_g": "请看看",
    "chr_h": "我画的",
    "chr_i": "确认",
    "chr_j": "取消",
}


# =====================================
# 2) 单动作映射
# gesture_tag -> code
# 最基础的一层：识别到单个动作直接给词
# =====================================
SINGLE_GESTURE_TEXT_MAP: Dict[str, str] = {
    "is_v_sign": "chr_h",          # 我画的
    "is_rock_sign": "chr_d",       # 这个角色
    "is_call_sign": "chr_e",       # 还需要
    "is_three_sign": "chr_f",      # 修改吗
    "is_point_up_sign": "chr_g",   # 请看看
    "is_ok_sign": "chr_i",         # 确认
    "is_fist": "chr_j",            # 取消
}


# =====================================
# 3) 多动作链映射
# tuple(gesture1, gesture2, ...) -> code
# 用于复杂动作口令
# 例如：
# is_four_sign 进入锁定
# 然后只能识别 is_v_sign
# 最终返回 chr_c
# =====================================
SEQUENCE_TEXT_MAP: Dict[Tuple[str, ...], str] = {
    ("is_v_sign",): "chr_a",                    # 我看看
    ("is_four_sign",): "chr_b",                # 好的（也可以作为进入锁定的触发）
    ("is_four_sign", "is_v_sign"): "chr_c",    # 请再改一下

    ("is_thumbs_up", "is_v_sign"): "chr_h",    # 我画的
    ("is_thumbs_up", "is_rock_sign"): "chr_d", # 这个角色
    ("is_thumbs_up", "is_call_sign"): "chr_e", # 还需要
    ("is_thumbs_up", "is_three_sign"): "chr_f",# 修改吗
    ("is_thumbs_up", "is_point_up_sign"): "chr_g", # 请看看
}


# =====================================
# 4) 常用句模板（可选）
# code sequence -> final text
# 以后可做句子拼接或整句输出
# =====================================
SENTENCE_LIBRARY: Dict[Tuple[str, ...], str] = {
    ("chr_h", "chr_d", "chr_g"): "我画的这个角色请看看",
    ("chr_d", "chr_e", "chr_f"): "这个角色还需要修改吗",
    ("chr_a",): "我看看",
    ("chr_b",): "好的",
    ("chr_c",): "请再改一下",
}


# =====================================
# 5) 工具函数
# =====================================
def get_text_by_code(code: Optional[str]) -> Optional[str]:
    if code is None:
        return None
    return TEXT_LIBRARY.get(code)


def get_code_by_gesture(gesture_tag: Optional[str]) -> Optional[str]:
    if gesture_tag is None:
        return None
    return SINGLE_GESTURE_TEXT_MAP.get(gesture_tag)


def get_code_by_sequence(sequence: Tuple[str, ...]) -> Optional[str]:
    return SEQUENCE_TEXT_MAP.get(sequence)


def get_sentence_by_codes(code_list: List[str]) -> Optional[str]:
    if not code_list:
        return None
    return SENTENCE_LIBRARY.get(tuple(code_list))


def list_text_codes() -> List[str]:
    return list(TEXT_LIBRARY.keys())


def list_text_items() -> Dict[str, str]:
    return dict(TEXT_LIBRARY)


def list_single_gesture_map() -> Dict[str, str]:
    return dict(SINGLE_GESTURE_TEXT_MAP)


def list_sequence_map() -> Dict[str, str]:
    return {
        " -> ".join(k): v
        for k, v in SEQUENCE_TEXT_MAP.items()
    }


def resolve_code(code: Optional[str]) -> Dict[str, Optional[str]]:
    return {
        "code": code,
        "text": get_text_by_code(code),
    }