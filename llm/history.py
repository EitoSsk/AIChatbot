# 履歴を管理するクラス
# 履歴の保存、読み込み、破棄の機能を提供する
# 履歴は./data/history.jsonに保存される
# 履歴は、ユーザーとアシスタントのメッセージのリストとして管理される
# 履歴の最大トークン数は、config.pyのhistory_max_tokensで設定される
# 履歴の保存は、チャットの応答が生成された後に行われる
# 履歴の破棄は、最大トークン数を超えた場合に行われ、古いメッセージから順に削除される
# history.jsonが存在しない場合は、新規作成される

import os
import json

class History:
    def __init__(self, config):
        self.config = config
        self.history_file = './data/history.json'
        self.history = self.load_history()

    # 履歴をロードするメソッド
    # history.jsonが存在しない場合は、新規作成される
    def load_history(self):
        if not os.path.exists(self.history_file):
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=4)
            return []

        with open(self.history_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    # 履歴にメッセージを追加するメソッド
    # メッセージは辞書形式で、'role'と'content'のキーを持つ
    def add_message(self, role, content):
        self.history.append({'role': role, 'content': content})
        self._trim_history()
        self._save_history()

    # 履歴を保存するメソッド
    def _save_history(self):
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)

    # 履歴の最大数を超えた場合に古いメッセージから削除するメソッド
    def _trim_history(self):
        while len(self.history) > self.config.history_max_tokens:
            self.history.pop(0)