# 履歴の初期ロードユースケース

from logging import Logger

from config import Config
from core.llm.gguf_llm import GGUF_LLM
from usecase.create_system_prompt_usecase import CreateSystemPromptUseCase
from repository.character_repository import CharacterRepository
from repository.history_repository import HistoryRepository
from repository.memory_repository import MemoryRepository
from repository.summary_repository import SummaryRepository

class LoadHistoryUseCase:

    # コンストラクタ
    def __init__(
        self, 
        config: Config, 
        logger: Logger,
        model: GGUF_LLM,
        history_repository: HistoryRepository, 
        summary_repository: SummaryRepository,
        memory_repository: MemoryRepository,  
        character_repository: CharacterRepository, 
    ):
        self._config = config
        self._logger = logger
        self._model = model
        self._history_repository = history_repository
        self._summary_repository = summary_repository
        self._character_repository = character_repository
        self._memory_repository = memory_repository
        self._system_prompt_list = CreateSystemPromptUseCase(
            self._history_repository,
            self._summary_repository,
            self._memory_repository,
            self._character_repository,
            self._config,
            self._logger
        ).execute()

    def execute(self):
        is_new_month = self._history_repository.load_history()
        all_history = self._history_repository.getAllHistory()

        trimed_history = self._model.trim_history(
            "", 
            all_history, 
            self._system_prompt_list
        )

        self._history_repository.setHistory(trimed_history)
        return is_new_month
