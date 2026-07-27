# バリデーション機能

import re
from typing import Any
from core.data.exception.validation_exception import JsonKeysValidationError, JsonTypesValidationError, RangeValidationError, RequiredValidationError, ResponseEmptyError, ValidationOtherError

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
    def range(name: str, value: Any, range: tuple):
        if isinstance(value, str):
            r = len(value)
        elif isinstance(value, int) or isinstance(value, float):
            r = value
        else:
            raise ValidationOtherError(f"「{name}」の型が対象外です。")
        
        if not range[0] <= r <= range[1]:
            raise RangeValidationError(f"「{name}」が範囲外です。[start={range[0]} end={range[1]}]")
    
    @staticmethod
    def required(name: str, value: Any):
        if value == None:
            raise RequiredValidationError(f"「{name}」は必須です。")
        elif isinstance(value, str) and value == "":
            raise RequiredValidationError(f"「{name}」は必須です。")
        elif isinstance(value, int) and not value > 0:
            raise RequiredValidationError(f"「{name}」は必須です。")

class LLMResponseValidation:

    @staticmethod
    def validate(response: str | None) -> tuple:

        if response is None:
            raise ResponseEmptyError("応答メッセージがありません。")

        response = response.strip()

        if response == "":
            raise ResponseEmptyError("応答メッセージがありません。")

        EMOTION_PATTERN = re.compile(r"^\[\s*EMOTION\s*:\s*([A-Za-z_]+)\s*\]\s*", re.MULTILINE)
        match = EMOTION_PATTERN.search(response)
        has_emotion = match is not None

        if has_emotion:
            message = response[match.end():].strip()
        else:
            message = response.strip()

        if not len(message) > 0:
            raise ResponseEmptyError("応答メッセージがありません。")

        return has_emotion, message
        