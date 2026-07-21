# Test_To_Speech機能

from repository.voice_repository import VoiceRepository
from logger import Logger
from config import Config
import speech.audio as audio


class TTS:

    def __init__(self, config: Config, logger: Logger):
        self._config = config
        self._logger = logger
        self._repos = VoiceRepository(config, logger)

    def play(self, text: str):
        data = self._repos.queryVoice(text)
        audio.play(data)

    def wait(self):
        audio.wait()