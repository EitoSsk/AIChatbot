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
        except VoiceEngineNotRunningError:
            self._voice_enabled = False
            self._logger.debug("VOICEVOXエンジンを起動されていないか、接続できない状況です。")
        except VoiceTimeoutError:
            self._logger.debug("VOICEVOXエンジンとの通信がタイムアウトしました。")
        except (VoicePlaybackError, VoiceNetworkError):
            self._voice_enabled = False
            self._logger.debug("音声が再生できませんでした。")
        except:
            self._voice_enabled = False
            self._logger.debug("音声が再生できませんでした。")

    def wait(self):
        if not self._voice_enabled:
            return

        try:
            audio.wait()
        except:
            self._logger.debug("音声の停止に失敗しました。")
        