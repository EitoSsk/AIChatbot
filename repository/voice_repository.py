# 音声リポジトリクラス
# 音声データを作成する機能を提供する

from core.data.exception.network_exception import NetworkError
from core.data.exception.voice_exception import VoiceEngineNotRunningError, VoiceNetworkError, VoiceTimeoutError
from core.data.response import Response
from core.data.emotion import Emotion
from core.network.http_client import API_AUDIO_QUERY, API_SYNTHESIS, HttpClient
from logger import Logger
from config import Config

class VoiceRepository:

    def __init__(self, config: Config, logger: Logger):
        self._config = config
        self._logger = logger

    def queryVoice(self, message: Response, voice_setting: dict):
        client = HttpClient(self._config, self._logger)
        speaker = voice_setting.get(
            message.emotion.name.lower(),
            voice_setting["neutral"]
        )
        # クエリの取得
        try:
            query_res = client.request(
                api = API_AUDIO_QUERY,
                params = {
                    "text": message.message,
                    "speaker": speaker
                }
            )
        except NetworkError as e:
            if e.status_code == 400 or e.status_code == 404 or e.status_code == 422:
                raise VoiceEngineNotRunningError()
            elif e.status_code == 500:
                raise VoiceNetworkError()
            elif e.is_timeout:
                raise VoiceTimeoutError()
            else:
                raise VoiceNetworkError()
        
        # 音声編集
        query_json = query_res.json()
        if message.emotion == Emotion.NEUTRAL:
            query_json["speedScale"] = 1.0
            query_json["pitchScale"] = 0.0
            query_json["intonationScale"] = 1.0
        elif message.emotion == Emotion.SHY:
            query_json["speedScale"] = 1.0
            query_json["pitchScale"] = 0.0
            query_json["intonationScale"] = 1.0
        elif message.emotion == Emotion.SAD:
            query_json["speedScale"] = 1.0
            query_json["pitchScale"] = 0.0
            query_json["intonationScale"] = 1.0
        elif message.emotion == Emotion.ANGRY:
            query_json["speedScale"] = 1.0
            query_json["pitchScale"] = 0.0
            query_json["intonationScale"] = 1.0
        elif message.emotion == Emotion.HAPPY:
            query_json["speedScale"] = 1.0
            query_json["pitchScale"] = 0.0
            query_json["intonationScale"] = 1.0
        elif message.emotion == Emotion.SURPRISED:
            query_json["speedScale"] = 1.20
            query_json["pitchScale"] = 0.10
            query_json["intonationScale"] = 1.40
            query_json["volumeScale"] = 1.05
        elif message.emotion == Emotion.EXCITED:
            query_json["speedScale"] = 1.30
            query_json["pitchScale"] = 0.08
            query_json["intonationScale"] = 1.55
            query_json["volumeScale"] = 1.05

        self._logger.debug(f"""
[VOICE]
speaker={speaker}
emotion={message.emotion.name}""")

        # 音声合成
        try:
            synthesis_res = client.request(
                api = API_SYNTHESIS,
                params = {
                    "speaker": speaker
                },
                json = query_json
            )
        except NetworkError as e:
            if e.status_code == 400 or e.status_code == 404 or e.status_code == 422:
                raise VoiceEngineNotRunningError()
            elif e.status_code == 500:
                raise VoiceNetworkError()
            elif e.is_timeout:
                raise VoiceTimeoutError()
            else:
                raise VoiceNetworkError()
        
        return  synthesis_res.content
