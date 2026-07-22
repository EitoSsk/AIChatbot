# Test_To_Speech機能

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

    def play(self, message: Response):
        voice_setting = self._character_repository.get_voice()
        data = self._voice_repository.queryVoice(message, voice_setting)
        audio.play(data)

    def wait(self):
        audio.wait()