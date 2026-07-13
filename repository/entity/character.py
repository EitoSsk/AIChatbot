# キャラクタークラス
# キャラクター情報を保持する
# キャラクター情報は./character.jsonに保存されている
# キャラクター情報からシステムプロンプトを構成する情報を作成する

import json
from exception.file_exception import CharacterError, FileErrorType

class Character:

    # コンストラクタ
    def __init__(self, config, logger):
        self._config = config
        self._logger = logger
        self._character_file = "./data/character.json"
        self._character_data = self._load()
        self._name = self._character_data["name"]
        self._sections = self._character_data["sections"]

    # 読み込み
    # character.jsonからキャラクターデータを読み込む
    def _load(self):
        try:
            with open(self._character_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, PermissionError) as e:
            raise CharacterError(FileErrorType.READ.value)
        