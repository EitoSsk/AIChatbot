# 設定クラス
# このクラスはアプリケーションの設定値を保持します。
# 設定は./data/config.jsonファイルから読み込まれます。
# jsonの要素はこのクラスのメンバと1対1の対応関係を持ちます。
# 読み込まれた設定値を各メンバに格納します。

import json
import os

class Config:
    
    def __init__(self, config_file='./data/config.json'):
        config_data = self.load_config(config_file)

        # キーから値を取得し、存在しない場合はデフォルト値を設定
        self.model_id = config_data.get("model_id", "google/gemma-3-1B-it")
        self.user_name = config_data.get("user_name", "ユーザー")
        self.assistant_name = config_data.get("assistant_name", "アシスタント")
        self.chat_max_tokens = config_data.get("chat_max_tokens", 256)
        self.chat_temperature = config_data.get("chat_temperature", 0.7)
        self.chat_top_p = config_data.get("chat_top_p", 0.9)
        self.history_max_tokens = config_data.get("history_max_tokens", 25)

    def load_config(self, config_file):
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Config file '{config_file}' not found.")
        
        with open(config_file, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        
        return config_data