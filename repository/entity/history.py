# 履歴を管理するクラス
# 履歴の保存、読み込み、破棄の機能を提供する
# 履歴は./data/history/yyyy-mm.jsonに保存される
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
from core.data.exception.file_exception import FileErrorType, HistoryError
from pathlib import Path
import shutil

class History:

    _HISTORY_DIR = "./data/history/"
    _SEED_FILE = "./data/conversation_seed.json"

    def __init__(self, config, logger):
        self._config = config
        date = datetime.now().strftime("%Y-%m")
        self._history_file = f'{self._HISTORY_DIR}{date}.json'
        self._logger = logger
        self._all_history = []

    def getHistory(self):
        return self._history.copy()
    
    def getAllHistory(self):
        return self._all_history.copy()
    
    def setHistory(self, history: list):
        self._history = history

    # 履歴をロードするメソッド
    # history.jsonが存在しない場合は、新規作成される
    # メッセージの取得前に_discard_history()を呼び出して履歴を整理する
    # message_max_tokensの数だけ、直近のメッセージを取得する
    def load_history(self) -> bool:
        if not os.path.exists(self._history_file):
            is_new_month = self._create_new_history()
        else:
            is_new_month = False

        try:
            self._discard_history()
            with open(self._history_file, 'r', encoding='utf-8') as f:
                self._all_history = json.load(f)
        except (FileNotFoundError, PermissionError) as e:
            self._logger.error(e)
            raise HistoryError(FileErrorType.READ.value)

        return is_new_month

    # 履歴にメッセージを追加し、最新の履歴を反映するメソッド
    # メッセージは辞書形式で、'role'と'content'、'timestamp'のキーを持つ
    def fetch_history(self, role, content, tokens, trimed_history: list):
        self._history = trimed_history.copy()
        new = {'role': role, 'content': content, 'tokens': tokens, 'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        self._history.append(new)
        self._all_history.append(new)

        try:
            self._save_history()
        except (FileNotFoundError, PermissionError) as e:
            self._logger.error(e)
            raise HistoryError(FileErrorType.SAVE.value)
        
        self._logger.debug(
f"""
[History]
Historys: {len(self._history)}
Total Historys: {len(self._all_history)}
History Name: {self._history_file}
"""
        )
    
    # 日付指定で履歴を取得する(yyyy-MM)
    def getHistoryFromDate(self, datetime):
        date = datetime.strftime("%Y-%m")
        file = f'{self._HISTORY_DIR}{date}.json'
        if not os.path.exists(file):
            return []
        
        try:
            with open(file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, PermissionError) as e:
            self._logger.error(e)
            raise HistoryError(FileErrorType.READ.value)

    def _create_new_history(self):
        if not os.path.exists(self._HISTORY_DIR):
            os.makedirs(self._HISTORY_DIR, exist_ok=True)
        
        history_dir = Path(self._HISTORY_DIR)
        history_files = sorted(history_dir.glob("*.json"))

        if len(history_files) > 0:
            file = history_files[-1]
            if not file.exists():
                self._create_new_history_from_seed()
                return False
                    
            try:
                with file.open('r', encoding='utf-8') as f:
                    data = json.load(f)
                with open(self._history_file, 'w', encoding='utf-8') as f:
                    json.dump(data[-20:], f, ensure_ascii=False, indent=4)
                return True
            except:
                self._create_new_history_from_seed()
        else:
            self._create_new_history_from_seed()

        return False

    def _create_new_history_from_seed(self):
        seed_file = Path(self._SEED_FILE)
        history_file = Path(self._history_file)
        history_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(seed_file, history_file)

    # 履歴を保存するメソッド
    def _save_history(self):
        with open(self._history_file, 'w', encoding='utf-8') as f:
            json.dump(self._all_history, f, ensure_ascii=False, indent=4)

    # 履歴を破棄するメソッド
    # history_max_tokensの数を超えた場合に、古いメッセージから削除される
    def _discard_history(self):
        # jsonファイルをロードして、メッセージの件数を確認する
        with open(self._history_file, 'r', encoding='utf-8') as f:
            history = json.load(f)
        # history_max_tokensの数を超えた場合に、古いメッセージから削除される
        while self._config.history_max_tokens and len(history) > self._config.history_max_tokens:
            del history[:2]
        # 更新された履歴を保存する
        with open(self._history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=4)