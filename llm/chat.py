#チャット機能を持つクラス
#このクラスは以下の機能を持つ
#テキストの送信
#チャット履歴の更新
#応答返却

from core.data.response import Response
import re
from core.data.emotion import Emotion
from repository.character_repository import CharacterRepository
from repository.memory_repository import MemoryRepository
from repository.summary_repository import SummaryRepository
import torch
from config import Config
from logger import Logger
from repository.history_repository import HistoryRepository
from llm.prompt import PromptBuilder

class Chat:

    # コンストラクタ
    def __init__(
        self, 
        model, 
        tokenizer, 
        history_repository: HistoryRepository, 
        summary_repository: SummaryRepository,
        memory_repository: MemoryRepository,  
        character_repository: CharacterRepository, 
        config: Config, 
        logger: Logger
    ):
        self._model = model
        self._tokenizer = tokenizer
        self._config = config
        self._logger = logger
        self._history_repository = history_repository
        self._summary_repository = summary_repository
        self._memory_repository = memory_repository
        self._character_repository = character_repository
        self._system_prompt_list = [
            self._character_repository.build_prompt(),
            self._summary_repository.build_prompt(),
            self._memory_repository.build_prompt()
        ]

    # メッセージを送信するメソッド
    # レスポンスを返却する
    def send_message(self, message):
        # PromptBuilderを使用して、履歴からプロンプトを構築
        prompt_builder = PromptBuilder(self._config, self._tokenizer, self._logger)
        trimed_history = prompt_builder.trim_history_by_tokens(
            self._history_repository.getHistory(), 
            message,
            self._system_prompt_list
        )
        prompt = prompt_builder.build_prompt(
            trimed_history, message,
            self._system_prompt_list
        )

        # 履歴の更新（システムプロンプトは含めない）
        self._history_repository.fetch_history("user", message, trimed_history)

        # 応答を生成
        response = self._generate_response(prompt)
        # 応答をチャット履歴に追加
        self._history_repository.fetch_history("assistant", response.message, self._history_repository.getHistory())
        return response

    # インプットから応答を生成するメソッド
    # ここでは、モデルを使用して応答を生成するロジックを実装する
    # tokenizer と model を使用して、入力メッセージに基づいて応答を生成する
    def _generate_response(self, prompt) -> Response:
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

        # 感情とメッセージに分解
        return  self._extract_message(response)
    
    def _extract_message(self, text: str) -> Response:
        EMOTION_PATTERN = re.compile(r"^\[EMOTION:([A-Za-z_]+)\]\s*", re.MULTILINE)
        match = EMOTION_PATTERN.match(text)

        if match is None:
            # 感情が取得できなかった場合はNEUTRAL扱い
            return Response(text.strip(), Emotion.NEUTRAL)

        emotion = Emotion.from_string(match.group(1))
        message = EMOTION_PATTERN.sub("", text, count=1).strip()
        return Response(message, emotion)
    
