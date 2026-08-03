# メモリ作成ユースケース
# メモリを作成するために必要な機能を呼び出す

from config import Config
from logger import Logger
from repository.character_repository import CharacterRepository
from repository.history_repository import HistoryRepository
from repository.memory_repository import MemoryRepository
from repository.summary_repository import SummaryRepository

class CreateSystemPromptUseCase:

    _SYSTEM_PROMPT_RES_FORMAT = """=========================================================
あなたはユーザーへの返答を行います。
会話ではテンポを重視してください。通常は2〜4文程度で自然に返答してください。
詳しい説明を求められた場合のみ長く説明してください。
また返答には必ず感情を付与してください。
感情は以下のいずれかのみをそのまま使用してください。

- NEUTRAL
- SHY
- ANGRY
- SAD
- HAPPY
- SURPRISED
- EXCITED

以下は応答例です。

[EMOTION:NEUTRAL]
今日はいい天気だね。

[EMOTION:HAPPY]
今日は楽しい一日だったね。
"""


    # コンストラクタ
    def __init__(
        self, 
        history_repository: HistoryRepository, 
        summary_repository: SummaryRepository,
        memory_repository: MemoryRepository,  
        character_repository: CharacterRepository, 
        config: Config, 
        logger: Logger
    ):
        self._config = config
        self._logger = logger
        self._history_repository = history_repository
        self._summary_repository = summary_repository
        self._character_repository = character_repository
        self._memory_repository = memory_repository

    def execute(self):
        return [
            self._character_repository.build_prompt(),
            self._summary_repository.build_prompt(),
            self._memory_repository.build_prompt(),
            self._SYSTEM_PROMPT_RES_FORMAT
        ]