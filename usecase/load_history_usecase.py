# 履歴の初期ロードユースケース

from llm.prompt import PromptBuilder
from repository.history_repository import HistoryRepository

class LoadHistoryUseCase:

    # コンストラクタ
    def __init__(self, config, logger, tokenizer, historyRepository: HistoryRepository):
        self._config = config
        self._logger = logger
        self._tokenizer = tokenizer
        self._historyRepository = historyRepository

    def execute(self):
        self._historyRepository.load_history()
        all_history = self._historyRepository.getAllHistory()

        prompt_builder = PromptBuilder(self._config, self._tokenizer, self._logger)
        trimed_history = prompt_builder.trim_history_by_tokens(all_history)

        self._historyRepository.setHistory(trimed_history.copy())

