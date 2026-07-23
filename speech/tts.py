# Test_To_Speech機能

from core.data.exception.voice_exception import VoiceEngineNotRunningError, VoiceNetworkError, VoicePlaybackError, VoiceTimeoutError
from core.data.response import Response
from repository.character_repository import CharacterRepository
from repository.voice_repository import VoiceRepository
from logger import Logger
from config import Config
import speech.audio as audio


class TTS:

    def __init__(
        self, config: Config, 
        logger: Logger,
        character_repository: CharacterRepository, 
    ):
        self._config = config
        self._logger = logger
        self._voice_repository = VoiceRepository(config, logger)
        self._character_repository = character_repository
        self._voice_enabled = True

    def play(self, message: Response):
        if not self._voice_enabled:
            return
        
        voice_setting = self._character_repository.get_voice()
        try:
            data = self._voice_repository.queryVoice(message, voice_setting)
            audio.play(data)
        except VoiceEngineNotRunningError as e:
            self._logger.error(e)
            self._logger.warning("VOICEVOXエンジンを起動されていないか、接続できない状況です。")
            self._voice_enabled = False
        except VoiceTimeoutError as e:
            self._logger.error(e)
            self._logger.warning("VOICEVOXエンジンとの通信がタイムアウトしました。")
        except (VoicePlaybackError, VoiceNetworkError) as e:
            self._logger.error(e)
            self._logger.warning("音声が再生できませんでした。")
            self._voice_enabled = False
        except Exception as e:
            self._logger.error(e)
            self._logger.warning("音声が再生できませんでした。")
            self._voice_enabled = False

    def wait(self):
        if not self._voice_enabled:
            return

        try:
            audio.wait()
        except Exception as e:
            self._logger.error(e)
            self._logger.warning("音声の停止に失敗しました。")
        