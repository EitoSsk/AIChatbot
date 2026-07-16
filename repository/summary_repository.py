# サマリリポジトリクラス
# 要約を作成、取得する機能を提供します。
# TODO:サマリ情報をシステムプロンプトを構築するために整理して提供します。

from repository.entity.summary import Summary

class SummaryRepository:

    _SYSTEM_PROMPT = """以下は最近の会話を要約したものです。

現在の状況や継続中の話題を理解するための参考情報です。
直近の会話とのつながりを理解する目的で利用してください。

[要約]
"""

    # コンストラクタ
    def __init__(self, config, logger):
        self._config = config
        self._logger = logger
        self._summary = Summary(config, logger)

    def createSummary(self, model, tokenizer, history, history_tokens):
        self._summary.create(model, tokenizer, history, history_tokens)

    def getLastHistoryTokens(self):
        return self._summary.getLastHistoryTokens()
    
    def getSummary(self):
        return self._summary.getSummary()
    
    def build_prompt(self):
        summary = self._summary.getSummary()
        if summary == "":
            summary = "なし"
        prompt = [
            "=========================================================",
            self._SYSTEM_PROMPT,
            summary,
        ]

        return "\n".join(prompt)