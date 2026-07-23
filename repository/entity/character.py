# キャラクタークラス
# キャラクター情報を保持する
# キャラクター情報は./character.jsonに保存されている
# キャラクター情報からシステムプロンプトを構成する情報を作成する

import json
from core.data.exception.file_exception import CharacterError, FileErrorType
from core.data.exception.validation_exception import JsonKeysValidationError, JsonTypesValidationError
from logger import Logger
from utility.validation import Validation

class Character:

    _CHARACTER_KEYS = ["name", "sections"]
    _CHARACTER_SECTIONS_KEYS = ["title", "items"]
    _VOICE_KEYS = ["neutral", "shy", "sad", "angry", "happy", "surprised", "excited"]
    _VOICE_DEFAULT = {
       "voice": { "neutral": 20, "shy": 66, "sad": 77, "angry": 78, "happy": 79, "surprised": 20, "excited": 20 },
    }

    # コンストラクタ
    def __init__(self, config, logger: Logger):
        self._config = config
        self._logger = logger
        self._character_file = "./data/character.json"
        self._voice_file = "./data/voice.json"
        self._character_data = self._load(self._character_file)
        self._voice_data = self._load(self._voice_file)

        self._validate()

        self._name = self._character_data["name"]
        self._sections: dict = self._character_data["sections"]
        self._voice: dict = self._voice_data["voice"]

    # 読み込み
    def _load(self, file_path: str):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, PermissionError) as e:
            raise CharacterError(FileErrorType.READ.value)
        
    def _validate(self):
        # characterのバリデーション
        # キーチェック
        for key in self._CHARACTER_KEYS:
            try:
                Validation.key(self._character_data, key)
                for section in self._character_data["sections"]:
                    for key in self._CHARACTER_SECTIONS_KEYS:
                        Validation.key(section, key)
            except JsonKeysValidationError as  e:
                self._logger.error(e)
                raise e
                
        # 型チェック
        try:
            Validation.types(self._character_data["name"], str)
            Validation.types(self._character_data["sections"], list)
            for section in self._character_data["sections"]:
                Validation.types(section["title"], str)
                Validation.types(section["items"], list)
                for item in section["items"]:
                    Validation.types(item, str)
        except JsonTypesValidationError as  e:
            self._logger.error(e)
            raise e

        # voiceのバリデーション
        # キーチェック
        try:
            Validation.key(self._voice_data, "voice")
        except JsonKeysValidationError as  e:
            self._logger.error(e)
            self._logger.warning("ボイス設定をデフォルトで補完して復旧しています。必要があれば手動でファイルを修正してください。")
            self._voice_data = self._VOICE_DEFAULT

        for key in self._VOICE_KEYS:
            try:
                Validation.key(self._voice_data["voice"], key)
            except JsonKeysValidationError as  e:
                self._logger.error(e)
                self._logger.warning("ボイス設定をデフォルトで補完して復旧しています。必要があれば手動でファイルを修正してください。")
                self._voice_data["voice"][key] = self._VOICE_DEFAULT["voice"][key]

        # 型チェック
        for key in self._VOICE_KEYS:
            try:
                Validation.types(self._voice_data["voice"][key], int)
            except JsonTypesValidationError as e:
                self._logger.error(e)
                self._logger.warning("ボイス設定をデフォルトで補完して復旧しています。必要があればアプリを終了してから手動でファイルを修正してください。")
                self._voice_data["voice"][key] = self._VOICE_DEFAULT["voice"][key]
