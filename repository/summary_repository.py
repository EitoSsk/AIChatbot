# サマリリポジトリクラス
# 要約を作成、取得する機能を提供します。
# TODO:サマリ情報をシステムプロンプトを構築するために整理して提供します。

from repository.entity.summary import Summary

class SummaryRepository:

    # コンストラクタ
    def __init__(self, config, logger):
        self._config = config
        self._logger = logger
        self._summary = Summary(config, logger)

    def createSummary(self, model, tokenizer, history, history_tokens):
        self._summary.create(model, tokenizer, history, history_tokens)

    def getLastHistoryTokens(self):
        return self._summary.getLastHistoryTokens()