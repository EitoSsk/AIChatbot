# 音声リポジトリクラス
# 音声データを作成する機能を提供する

from core.network.http_client import API_AUDIO_QUERY, API_SYNTHESIS, HttpClient
from logger import Logger
from config import Config

class VoiceRepository:

    def __init__(self, config: Config, logger: Logger):
        self._config = config
        self._logger = logger

    def queryVoice(self, content: str):
        client = HttpClient(self._config, self._logger)
        query_res = client.request(
            api = API_AUDIO_QUERY,
            params = {
                "text": content,
                "speaker": 16
            }
        )
        synthesis_res = client.request(
            api = API_SYNTHESIS,
            params = {
                "speaker": 16
            },
            json = query_res.json()
        )
        return  synthesis_res.content
