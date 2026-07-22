# 感情クラス

from enum import Enum


class Emotion(Enum):

    NEUTRAL = "NEUTRAL"
    SHY = "SHY"
    ANGRY = "ANGRY"
    SAD = "SAD"
    HAPPY = "HAPPY"
    SURPRISED = "SURPRISED"
    EXCITED = "EXCITED"

    @classmethod
    def from_string(cls, value: str) -> "Emotion":
        try:
            return cls[value.upper()]
        except KeyError:
            return cls.NEUTRAL

    