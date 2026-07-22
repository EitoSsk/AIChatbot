# 設定クラス
# このクラスはアプリケーションの設定値を保持します。
# 設定は./data/config.jsonファイルから読み込まれます。
# jsonの要素はこのクラスのメンバと1対1の対応関係を持ちます。
# 読み込まれた設定値を各メンバに格納します。

import json
import os

from core.data.exception.file_exception import ConfigError, FileErrorType

class Config:
    
    def __init__(self, config_file='./data/config.json'):
        config_data = self._load_config(config_file)

        # キーから値を取得し、存在しない場合はデフォルト値を設定
        self.debug_level = config_data.get("debug_level", "debug")
        self.model_id = config_data.get("model_id", "google/gemma-3-1B-it")
        self.user_name = config_data.get("user_name", "ユーザー")
        self.assistant_name = config_data.get("assistant_name", "アシスタント")
        self.chat_max_tokens = config_data.get("chat_max_tokens", 256)
        self.chat_temperature = config_data.get("chat_temperature", 0.7)
        self.chat_top_p = config_data.get("chat_top_p", 0.9)
        self.history_max_tokens = config_data.get("history_max_tokens", 25)
        self.message_max_tokens = config_data.get("message_max_tokens", 30)

    def _load_config(self, config_file):
        try: 
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            return config_data
        except (FileNotFoundError, PermissionError) as e:
            raise ConfigError(FileErrorType.READ.value)
        