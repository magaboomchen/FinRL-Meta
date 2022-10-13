from typing import List
from meta.local.base.type_define import T


def get_common_length_list(a: List[T], b: List[T]) -> List[T]:
    a_len = len(a)
    b_len = len(b)
    min_len = min(a_len, b_len)
    return (a[:min_len], b[:min_len])
