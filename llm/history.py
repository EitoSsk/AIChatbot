# 履歴を管理するクラス
# 履歴の保存、読み込み、破棄の機能を提供する
# 履歴は./data/history.jsonに保存される
# 履歴は、ユーザーとアシスタントのメッセージのリストとして管理される
# 履歴の最大トークン数は、config.pyのhistory_max_tokensで設定される
# 履歴の保存は、チャットの応答が生成された後に行われる
# 履歴の破棄は、最大トークン数を超えた場合に行われ、古いメッセージから順に削除される
# history.jsonが存在しない場合は、新規作成される
# history.jsonの内容は、ユーザーとアシスタントのメッセージのリストであり、各メッセージは辞書形式で、'role'と'content'、'timestamp'のキーを持つ
# history.jsonの内容は、以下のような形式で保存される
# [
#     {
#         "role": "user",
#         "content": "こんにちは、元気ですか？",
#         "timestamp": "2023-01-01 00:00:00"
#     },
#     {
#         "role": "assistant",
#         "content": "元気です、ありがとう。あなたは？",
#         "timestamp": "2023-01-01 00:00:01"
#     }
# ]

from datetime import datetime
import os
import json

from exception.file_exception import FileErrorType, HistoryError

class History:
    def __init__(self, config):
        self.config = config
        self.history_file = './data/history.json'
        self.history = self.load_history()

    # 履歴をロードするメソッド
    # history.jsonが存在しない場合は、新規作成される
    # メッセージの取得前に_discard_history()を呼び出して履歴を整理する
    # message_max_tokensの数だけ、直近のメッセージを取得する
    def load_history(self):
        if not os.path.exists(self.history_file):
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=4)
            return []
        
        try:
            self._discard_history()
            with open(self.history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
                return history[-self.config.message_max_tokens:] if self.config.message_max_tokens else history
        except FileNotFoundError as e:
            raise HistoryError(FileErrorType.READ)
        except PermissionError as e:
            raise HistoryError(FileErrorType.READ)

        

    # 履歴にメッセージを追加するメソッド
    # メッセージは辞書形式で、'role'と'content'、'timestamp'のキーを持つ
    # message_max_tokensの数だけ、直近のメッセージを保持する
    # message_max_tokensの数を超えた場合は、古いメッセージから削除される
    def add_message(self, role, content):
        self.history.append({'role': role, 'content': content, 'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        while self.config.message_max_tokens and len(self.history) > self.config.message_max_tokens:
            self.history.pop(0)

        try:
            self._save_history()
        except FileNotFoundError as e:
            raise HistoryError(FileErrorType.SAVE)
        except PermissionError as e:
            raise HistoryError(FileErrorType.SAVE)

    # 履歴を保存するメソッド
    def _save_history(self):
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)

    # 履歴を破棄するメソッド
    # history_max_tokensの数を超えた場合に、古いメッセージから削除される
    def _discard_history(self):
        # jsonファイルをロードして、メッセージの件数を確認する
        with open(self.history_file, 'r', encoding='utf-8') as f:
            history = json.load(f)
        # history_max_tokensの数を超えた場合に、古いメッセージから削除される
        while self.config.history_max_tokens and len(history) > self.config.history_max_tokens:
            history.pop(0)
        # 更新された履歴を保存する
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=4)