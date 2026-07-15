#チャット機能を持つクラス
#このクラスは以下の機能を持つ
#テキストの送信
#チャット履歴の更新
#応答返却

import torch
from config import Config
from logger import Logger
from llm.history import History
from llm.prompt import PromptBuilder

class Chat:

    # コンストラクタ
    def __init__(self, model, tokenizer, history: History, config: Config, logger: Logger):
        self._model = model
        self._tokenizer = tokenizer
        self._config = config
        self._logger = logger
        self._history = history

    # メッセージを送信するメソッド
    # レスポンスを返却する
    def send_message(self, message):
        # PromptBuilderを使用して、履歴からプロンプトを構築
        prompt_builder = PromptBuilder(self._config, self._tokenizer, self._logger)
        trimed_history = prompt_builder.trim_history_by_tokens(self._history.history, message)
        prompt = prompt_builder.build_prompt(trimed_history, message)

        # 履歴の更新（システムプロンプトは含めない）
        self._history.fetch_history("user", message, trimed_history)

        # 応答を生成
        response = self._generate_response(prompt)
        # 応答をチャット履歴に追加
        self._history.fetch_history("assistant", response, self._history.history)
        return response

    # インプットから応答を生成するメソッド
    # ここでは、モデルを使用して応答を生成するロジックを実装する
    # tokenizer と model を使用して、入力メッセージに基づいて応答を生成する
    def _generate_response(self, prompt):
        # トークナイズ
        inputs = self._tokenizer.apply_chat_template(
            prompt,
            tokenize=True,
            return_dict=True,
            return_tensors="pt",
            add_generation_prompt=True,
        )
        inputs = {k: v.to(self._model.device) for k, v in inputs.items()}

        # 推論
        with torch.no_grad():
            outputs = self._model.generate(
                **inputs,
                max_new_tokens=self._config.chat_max_tokens,
                temperature=self._config.chat_temperature,
                top_p=self._config.chat_top_p,
            )

        # 応答をデコード
        response = self._tokenizer.decode(
            outputs[0][inputs["input_ids"].shape[-1]:],
            skip_special_tokens=True,
        )

        # トークン数をログ出力
        input_tokens_count = inputs["input_ids"].shape[-1]
        response_tokens = self._tokenizer(
            response,
            return_tensors="pt",
            add_special_tokens=False
        )
        response_tokens_count = response_tokens["input_ids"].shape[1]
        self._logger.debug(
f"""
[Prompt]
Input Tokens: {input_tokens_count}
Response Tokens: {response_tokens_count} 
Total Tokens: {input_tokens_count + response_tokens_count} 
"""
        )

        return response
    