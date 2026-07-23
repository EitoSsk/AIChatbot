# バリデーション機能

from typing import Any
from core.data.exception.validation_exception import JsonKeysValidationError, JsonTypesValidationError, RangeValidationError, ValidationOtherError

class Validation:

    @staticmethod
    def key(dict: dict, key: Any):
        if key not in dict:
            raise JsonKeysValidationError(f"「{key}」のkeyがありません")
            
    @staticmethod
    def types(value: Any, type: type):
        if not isinstance(value, type):
            raise JsonTypesValidationError(f"「{value}」の型が正しくありません。")
            
    
    # rangeには{start, end}の２つの値を入れること
    @staticmethod
    def range(value: int, range: tuple[int]):
        if not range[0] <= value <= range[1]:
            raise RangeValidationError(f"「{value}」が範囲外です。[start={range[0]} end={range[1]}]")