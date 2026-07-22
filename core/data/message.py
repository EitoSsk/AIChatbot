# メッセージデータクラス

import dataclasses
from core.data.emotion import Emotion

@dataclasses.dataclass
class Message:
    text: str
    emotion: Emotion
