# 履歴リポジトリクラス
# 履歴情報を取得・更新する機能を提供します。

from repository.entity.history import History

class HistoryRepository:

    # コンストラクタ
    def __init__(self, config, logger):
        self._config = config
        self._logger = logger
        self._history = History(config, logger)

    def getHistory(self):
        return self._history.getHistory()
    
    def getAllHistory(self):
        return self._history.getAllHistory()

    def setHistory(self, history: list):
        self._history.setHistory(history)

    def load_history(self):
        return self._history.load_history()

    def fetch_history(self, role, content, tokens, trimed_history: list):
        self._history.fetch_history(role, content, tokens, trimed_history)
        
    def getAllHistoryTokens(self):
        all = self._history.getAllHistory()
        total_tokens = 0
        for h in all:
            total_tokens += h["tokens"]
        return total_tokens
    
    def getHistoryFromDate(self, datetime):
        return self._history.getHistoryFromDate(datetime)