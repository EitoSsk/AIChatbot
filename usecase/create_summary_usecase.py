# サマリ作成ユースケース
# サマリを作成するために必要な機能を呼び出す
# 前回のサマリ作成から履歴のトークン数が一定数増えた場合、サマリを作成する
# 月替わりで新規ファイルが生成されたかをBoolで返す

from datetime import datetime
from dateutil.relativedelta import relativedelta
from config import Config
from llm.history import History
from logger import Logger
from repository.summary_repository import SummaryRepository

class CreateSummaryUseCase:

    # コンストラクタ
    def __init__(self, summaryRepository: SummaryRepository, history: History, config: Config, logger: Logger):
        self._config = config
        self._logger = logger
        self._summaryRepository = summaryRepository
        self._history = history

    def execute(self, model, tokenizer):
        # サマリ作成の実行判定
        history_tokens = self._history.getAllHistoryTokens()
        prev_tokens = self._summaryRepository.getLastHistoryTokens()

        diff = history_tokens - prev_tokens
        self._logger.debug(f"""[CreateSummary]
history_tokens: {history_tokens}
prev_tokens: {prev_tokens}
diff: {diff}
""")
        if diff > self._config.message_max_tokens:
            self._logger.info("サマリを作成しています。しばらくお待ちください。")
            self._summaryRepository.createSummary(model, tokenizer, self._history.history.copy(), history_tokens)
            return False
        elif diff < 0:
            self._logger.info("サマリを作成しています。しばらくお待ちください。")
            prev_datetime = datetime.now() - relativedelta(months=1)
            prev_month_history = self._history.getHistoryFromDate(prev_datetime, canTrim=True)
            self._summaryRepository.createSummary(model, tokenizer, prev_month_history, 0)
            return True
        else:
            return False