# メッセージレスポンスデータクラス

import dataclasses
from core.data.emotion import Emotion

@dataclasses.dataclass
class Response:
    plane_text: str
    message: str
    emotion: Emotion
