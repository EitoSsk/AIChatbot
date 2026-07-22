# メッセージレスポンスデータクラス

import dataclasses
from core.data.emotion import Emotion

@dataclasses.dataclass
class Response:
    message: str
    emotion: Emotion
