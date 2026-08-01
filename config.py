# 設定クラス
# このクラスはアプリケーションの設定値を保持します。
# 設定は./data/config.jsonファイルから読み込まれます。
# jsonの要素はこのクラスのメンバと1対1の対応関係を持ちます。
# 読み込まれた設定値を各メンバに格納します。

import json
import os

from core.data.exception.file_exception import ConfigError, FileErrorType
from core.data.exception.validation_exception import JsonKeysValidationError, JsonTypesValidationError, RangeValidationError, RequiredValidationError
from utility.validation import Validation

class Config:

    _CONFIG_KEYS = [
        "debug_level", 
        "model_id", 
        "user_name", 
        "assistant_name", 
        "chat_max_tokens", 
        "chat_temperature", 
        "chat_top_p", 
        "history_max_tokens", 
        "chat_template_overhead", 
        "message_max_tokens"
    ]
    _CONFIG_TYPES = [
        str,
        str,
        str,
        str,
        int,
        float,
        float,
        int,
        int,
        int,
    ]
    
    def __init__(self, config_file='./data/config.json'):
        config_data = self._load_config(config_file)
        self._validate(config_data)

        # キーから値を取得し、存在しない場合はデフォルト値を設定
        self.debug_level = config_data.get("debug_level", "debug")
        self.model_id = config_data.get("model_id", "google/gemma-3-1B-it")
        self.user_name = config_data.get("user_name", "ユーザー")
        self.assistant_name = config_data.get("assistant_name", "アシスタント")
        self.chat_max_tokens = config_data.get("chat_max_tokens", 256)
        self.chat_temperature = config_data.get("chat_temperature", 0.7)
        self.chat_top_p = config_data.get("chat_top_p", 0.9)
        self.history_max_tokens = config_data.get("history_max_tokens", 8192)
        self.chat_template_overhead = config_data.get("chat_template_overhead", 520)
        self.message_max_tokens = config_data.get("message_max_tokens", 30)

    def _load_config(self, config_file):
        try: 
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            return config_data
        except (FileNotFoundError, PermissionError) as e:
            self._logger.error(e)
            raise ConfigError(FileErrorType.READ.value)
        
    def _validate(self, config_data: dict):
        # キーチェック
        for key in self._CONFIG_KEYS:
            try:
                Validation.key(config_data, key)
            except JsonKeysValidationError as  e:
                self._logger.error(e)
                raise e
                
        # 型チェック
        try:
            for config, type in zip(config_data.values(), self._CONFIG_TYPES):
                Validation.types(config, type)
        except JsonTypesValidationError as  e:
            self._logger.error(e)
            raise e
        
        # 必須チェック
        try:
            Validation.required("model_id", config_data["model_id"])
            Validation.required("chat_max_tokens", config_data["chat_max_tokens"])
            Validation.required("message_max_tokens", config_data["message_max_tokens"])
            Validation.required("chat_template_overhead", config_data["chat_template_overhead"])
            Validation.required("history_max_tokens", config_data["history_max_tokens"])
        except RequiredValidationError as  e:
            self._logger.error(e)
            raise e

        # 範囲チェック
        try:
            Validation.range("chat_temperature", config_data["chat_temperature"], (0.0, 2.0))
            Validation.range("chat_top_p", config_data["chat_top_p"], (0.0, 1.0))
        except RangeValidationError as  e:
            self._logger.error(e)
            raise e
    