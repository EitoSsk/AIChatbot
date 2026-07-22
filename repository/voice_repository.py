# 音声リポジトリクラス
# 音声データを作成する機能を提供する

from core.data.response import Response
from core.data.emotion import Emotion
from core.network.http_client import API_AUDIO_QUERY, API_SYNTHESIS, HttpClient
from logger import Logger
from config import Config

class VoiceRepository:

    def __init__(self, config: Config, logger: Logger):
        self._config = config
        self._logger = logger

    def queryVoice(self, message: Response):
        client = HttpClient(self._config, self._logger)
        speaker = 20
        # クエリの取得
        query_res = client.request(
            api = API_AUDIO_QUERY,
            params = {
                "text": message.message,
                "speaker": speaker
            }
        )
        
        # 音声編集
        query_json = query_res.json()
        if message.emotion == Emotion.NEUTRAL:
            speaker = 20
            query_json["speedScale"] = 1.0
            query_json["pitchScale"] = 0.0
            query_json["intonationScale"] = 1.0
        elif message.emotion == Emotion.SHY:
            speaker = 66
            query_json["speedScale"] = 1.0
            query_json["pitchScale"] = 0.0
            query_json["intonationScale"] = 1.0
        elif message.emotion == Emotion.SAD:
            speaker = 77
            query_json["speedScale"] = 1.0
            query_json["pitchScale"] = 0.0
            query_json["intonationScale"] = 1.0
        elif message.emotion == Emotion.ANGRY:
            speaker = 78
            query_json["speedScale"] = 1.0
            query_json["pitchScale"] = 0.0
            query_json["intonationScale"] = 1.0
        elif message.emotion == Emotion.HAPPY:
            speaker = 79
            query_json["speedScale"] = 1.0
            query_json["pitchScale"] = 0.0
            query_json["intonationScale"] = 1.0
        elif message.emotion == Emotion.SURPRISED:
            speaker = 20
            query_json["speedScale"] = 1.20
            query_json["pitchScale"] = 0.10
            query_json["intonationScale"] = 1.40
            query_json["volumeScale"] = 1.05
        elif message.emotion == Emotion.EXCITED:
            speaker = 20
            query_json["speedScale"] = 1.30
            query_json["pitchScale"] = 0.08
            query_json["intonationScale"] = 1.55
            query_json["volumeScale"] = 1.05

        # 音声合成
        synthesis_res = client.request(
            api = API_SYNTHESIS,
            params = {
                "speaker": speaker
            },
            json = query_json
        )
        return  synthesis_res.content
