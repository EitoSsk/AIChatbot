# サマリクラス
# サマリ情報を作成・保持する
# サマリ情報は./data/summary/yyyy-mm.jsonに保存されている
# サマリ情報からシステムプロンプトを構成する情報を作成する

from datetime import datetime
from dateutil.relativedelta import relativedelta
import os
import json
from core.data.exception.file_exception import SummaryError, FileErrorType

class Summary:

    _SUMMARY_DIR = "./data/summary/"

    # コンストラクタ
    def __init__(self, config, logger):
        self._config = config
        self._logger = logger
        date = datetime.now().strftime("%Y-%m")
        self._summary_file = f'{self._SUMMARY_DIR}{date}.json'
        self._summary_data = {}
        self._loadSummary()

    # サマリ作成
    # 応答を要約として保存する
    def create(self, model, history, history_tokens):
        prev_summary = "なし"
        if not self._summary_data == {}:
            prev_summary = self._summary_data["summary"]
        
        system_prompt = f"""これまでのユーザーとAIの会話の履歴を、今後の会話で利用するための要約にしてください。
==============================================
前回の要約
{prev_summary}
==============================================
前回の要約とこれまでの会話を統合し、
以前の要約を書き換えるのではなく、
最新の情報を含んだ新しい要約を一から作成してください。

以下は要約のルールです。
==============================================
要約のルール
- 重要な情報を優先して残してください。
- 挨拶や雑談など、今後不要な内容は省略してください。
- ユーザーの好み、目標、計画、継続中の作業は残してください。
- 事実のみを要約し、推測はしないでください。
- 可能性などの憶測や推測はせず、実際に行った会話の要約のみ行ってください。
- 将来の予測や期待は記載しないでください。
- 箇条書きを基本とし、簡潔にまとめてください。
- 重要な情報を省略せず、十分な情報量で要約してください。
- 要約のみを出力してください。
- 説明や前置きは不要です。
==============================================
フォーマット
下記のように見出しを付けてまとめてください。
「継続中のプロジェクト」は、
複数回の会話で継続して取り組んでいる内容のみを記載し、一度だけ話題に出た内容は記載しないでください。

# ユーザーについて
・性格
・考え方
・会話スタイル
・価値観

# 好み
・好きな食べ物
・趣味
・好きな場所

# 継続中のプロジェクト
・現在取り組んでいること

# 最近決まったこと
・今回追加された新しい情報
==============================================
"""

        response = self._createSummary(model, "履歴の要約をしてください。", history, system_prompt)
        summary = {'summary': response, 'last_history_tokens': history_tokens, 'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        self._createSummaryFile(summary)
        self._summary_data = summary

    # 前回の履歴のトークン数を取得
    def getLastHistoryTokens(self):
        if self._summary_data == {}:
            return 0
        else:
            return self._summary_data["last_history_tokens"]
        
    def getSummary(self):
        if self._summary_data == {}:
            return ""
        else:
            return self._summary_data["summary"]

    # 今月のサマリを取得する
    # 今月のサマリファイルがなければ先月のサマリファイルを取得する
    # どちらもない場合はロードを終了する
    def _loadSummary(self):
        if not os.path.exists(self._SUMMARY_DIR):
            os.makedirs(self._SUMMARY_DIR, exist_ok=True)
            return
        
        file = self._summary_file
        
        if not os.path.exists(self._summary_file):
            prev_datetime = datetime.now() - relativedelta(months=1)
            prev_date = prev_datetime.strftime("%Y-%m")
            prev_file = f'{self._SUMMARY_DIR}{prev_date}.json'
            if not os.path.exists(prev_file):
                return
            else:
                file = prev_file

        try:
            with open(file, 'r', encoding='utf-8') as f:
                self._summary_data = json.load(f)
        except (FileNotFoundError, PermissionError) as e:
            self._logger.error(e)
            raise SummaryError(FileErrorType.READ.value)


    def _createSummary(self, model, message, history, system_prompt):
        # 応答をデコード
        response = model.generate_response(
            message=message,
            prompt=history,
            system=[system_prompt]
        )

        # トークン数をログ出力
        response_tokens_count = model.count_tokens(response)
        self._logger.debug(
f"""
[Summary]
Summary File: {self._summary_file}
Summary Tokens: {response_tokens_count} 
"""
        )

        return response
    
    def _createSummaryFile(self, summary):
        try:
            with open(self._summary_file, 'w', encoding='utf-8') as f:
                json.dump(summary, f, ensure_ascii=False, indent=4)
        except (FileNotFoundError, PermissionError) as e:
            self._logger.error(e)
            raise SummaryError(FileErrorType.SAVE.value)