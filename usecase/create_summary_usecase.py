# サマリ作成ユースケース
# サマリを作成するために必要な機能を呼び出す
# 前回のサマリ作成から履歴のトークン数が一定数増えた場合、サマリを作成する
# 月替わりで新規ファイルが生成されたかをBoolで返す

from datetime import datetime
from dateutil.relativedelta import relativedelta
from config import Config
from llm.prompt import PromptBuilder
from repository.history_repository import HistoryRepository
from logger import Logger
from repository.summary_repository import SummaryRepository

class CreateSummaryUseCase:

    # コンストラクタ
    def __init__(self, summary_repository: SummaryRepository, history_repository: HistoryRepository, config: Config, logger: Logger):
        self._config = config
        self._logger = logger
        self._summary_repository = summary_repository
        self._history_repository = history_repository

    def execute(self, model, tokenizer):
        # サマリ作成の実行判定
        history_tokens = self._history_repository.getAllHistoryTokens()
        prev_tokens = self._summary_repository.getLastHistoryTokens()

        diff = history_tokens - prev_tokens
        self._logger.debug(f"""[CreateSummary]
history_tokens: {history_tokens}
prev_tokens: {prev_tokens}
diff: {diff}
""")
        if diff > self._config.message_max_tokens:
            self._logger.info("サマリを作成しています。しばらくお待ちください。")
            self._summary_repository.createSummary(model, tokenizer, self._history_repository.getHistory(), history_tokens)
            return False
        elif diff < 0:
            self._logger.info("サマリを作成しています。しばらくお待ちください。")
            prev_datetime = datetime.now() - relativedelta(months=1)
            prev_month_history = self._getHistoryFromDate(tokenizer, prev_datetime)
            self._summary_repository.createSummary(model, tokenizer, prev_month_history, 0)
            return True
        else:
            return False
        
    def _getHistoryFromDate(self, tokenizer, date):
        history = self._history_repository.getHistoryFromDate(date)
        prompt_builder = PromptBuilder(self._config, tokenizer, self._logger)
        return prompt_builder.trim_history_by_tokens(history)