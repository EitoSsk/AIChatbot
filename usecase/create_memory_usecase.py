# メモリ作成ユースケース
# メモリを作成するために必要な機能を呼び出す

from config import Config
from logger import Logger
from repository.memory_repository import MemoryRepository
from repository.summary_repository import SummaryRepository

class CreateMemoryUseCase:

    # コンストラクタ
    def __init__(self, summaryRepository: SummaryRepository, memoryRepository: MemoryRepository, config: Config, logger: Logger):
        self._config = config
        self._logger = logger
        self._summaryRepository = summaryRepository
        self._memoryRepository = memoryRepository

    def execute(self, model, tokenizer):
        summary = self._summaryRepository.getSummary()
        self._logger.info("メモリを作成しています。しばらくお待ちください。")
        self._memoryRepository.createMemory(model, tokenizer, summary)