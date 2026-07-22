# Test_To_Speech機能

from core.data.message import Message
from repository.voice_repository import VoiceRepository
from logger import Logger
from config import Config
import speech.audio as audio


class TTS:

    def __init__(self, config: Config, logger: Logger):
        self._config = config
        self._logger = logger
        self._repos = VoiceRepository(config, logger)

    def play(self, message: Message):
        data = self._repos.queryVoice(message)
        audio.play(data)

    def wait(self):
        audio.wait()