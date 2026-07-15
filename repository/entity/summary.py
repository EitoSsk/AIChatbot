# サマリクラス
# サマリ情報を作成・保持する
# サマリ情報は./data/summary/yyyy-mm.jsonに保存されている
# サマリ情報からシステムプロンプトを構成する情報を作成する

from datetime import datetime
from dateutil.relativedelta import relativedelta
import os
import json
import torch
from exception.file_exception import SummaryError, FileErrorType

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
    def create(self, model, tokenizer, history, history_tokens):
        prompt = history
        prev_summary = "なし"
        if not self._summary_data == {}:
            prev_summary = self._summary_data["summary"]
        
        content = f"""これまでのユーザーとAIの会話の履歴を、今後の会話で利用するための要約にしてください。
前回の要約も参考にしつつ要約を更新してください。
==============================================
要約のルール
- 前回の要約との差分は積極的に取り入れてください。
- 重要な情報を優先して残してください。
- 挨拶や雑談など、今後不要な内容は省略してください。
- ユーザーの好み、目標、計画、継続中の作業は残してください。
- 事実のみを要約し、推測はしないでください。
- 箇条書きを基本とし、簡潔にまとめてください。
- 1000文字以内を目安にしてください。
- 要約のみを出力してください。
- 説明や前置きは不要です。
==============================================
前回の要約
{prev_summary}
==============================================
"""
        message = {'role': "user", 'content': content, 'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        prompt.append(message)

        response = self._createSummary(model, tokenizer, prompt)
        summary = {'summary': response, 'last_history_tokens': history_tokens, 'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        self._createSummaryFile(summary)
        self._summary_data = summary

    # 前回の履歴のトークン数を取得
    def getLastHistoryTokens(self):
        if self._summary_data == {}:
            return 0
        else:
            return self._summary_data["last_history_tokens"]

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
            raise SummaryError(FileErrorType.READ.value)


    def _createSummary(self, model, tokenizer, prompt):
        # トークナイズ
        inputs = tokenizer.apply_chat_template(
            prompt,
            tokenize=True,
            return_dict=True,
            return_tensors="pt",
            add_generation_prompt=True,
        )
        inputs = {k: v.to(model.device) for k, v in inputs.items()}

        # 推論
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=self._config.chat_max_tokens,
                temperature=self._config.chat_temperature,
                top_p=self._config.chat_top_p,
            )

        # 応答をデコード
        response = tokenizer.decode(
            outputs[0][inputs["input_ids"].shape[-1]:],
            skip_special_tokens=True,
        )

        # トークン数をログ出力
        response_tokens = tokenizer(
            response,
            return_tensors="pt",
            add_special_tokens=False
        )
        response_tokens_count = response_tokens["input_ids"].shape[1]
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
            raise SummaryError(FileErrorType.SAVE.value)