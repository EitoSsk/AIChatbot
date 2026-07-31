#チャット機能を持つクラス
#このクラスは以下の機能を持つ
#テキストの送信
#チャット履歴の更新
#応答返却

from core.data.exception.validation_exception import ResponseEmptyError
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
from utility.validation import LLMResponseValidation

class Chat:

    _SYSTEM_PROMPT_RES_FORMAT = """=========================================================
あなたはユーザーへの返答を行います。
返答には必ず感情を付与してください。
感情は以下のいずれかのみをそのまま使用してください。

- NEUTRAL
- SHY
- ANGRY
- SAD
- HAPPY
- SURPRISED
- EXCITED

以下は応答例です。

[EMOTION:NEUTRAL]
今日はいい天気だね。

[EMOTION:HAPPY]
今日は楽しい一日だったね。
"""

    # コンストラクタ
    def __init__(
        self, 
        model, 
        history_repository: HistoryRepository, 
        summary_repository: SummaryRepository,
        memory_repository: MemoryRepository,  
        character_repository: CharacterRepository, 
        config: Config, 
        logger: Logger
    ):
        self._model = model
        self._config = config
        self._logger = logger
        self._history_repository = history_repository
        self._summary_repository = summary_repository
        self._memory_repository = memory_repository
        self._character_repository = character_repository
        self._system_prompt_list = [
            self._character_repository.build_prompt(),
            self._summary_repository.build_prompt(),
            self._memory_repository.build_prompt(),
            self._SYSTEM_PROMPT_RES_FORMAT
        ]

    # メッセージを送信するメソッド
    # レスポンスを返却する
    def send_message(self, message):
        # PromptBuilderを使用して、履歴からプロンプトを構築
        # prompt_builder = PromptBuilder(self._config, self._tokenizer, self._logger)
        # trimed_history = prompt_builder.trim_history_by_tokens(
        #     self._history_repository.getHistory(), 
        #     message,
        #     self._system_prompt_list
        # )
        # prompt = prompt_builder.build_prompt(
        #     trimed_history, message,
        #     self._system_prompt_list
        # )

        # 応答を生成
        count = 0
        while True:
            count += 1
            try:
                res = self._model.generate_response(
                    message, 
                    self._history_repository.getHistory(), 
                    self._system_prompt_list
                )
                has_emotion, text = LLMResponseValidation.validate(res)
                if has_emotion:
                    response = self._extract_message(res)
                else:
                    response = self._extract_message(f"[EMOTION:NEUTRAL]\n{text}")
                break
            except ResponseEmptyError as e:
                if count > 1:
                    self._logger.error(e)
                    raise e

        # # 履歴の更新
        # # ユーザーはシステムプロンプトを含めない
        # # 応答は原文を履歴にs追加
        # self._history_repository.fetch_history("user", message, trimed_history)
        # self._history_repository.fetch_history("assistant", response.plane_text, self._history_repository.getHistory())

        self._history_repository.fetch_history("user", message, self._history_repository.getHistory())
        self._history_repository.fetch_history("assistant", response.plane_text, self._history_repository.getHistory())
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

        # 応答のバリデーション
        has_emotion, message = LLMResponseValidation.validate(response)
        if has_emotion:
            # 感情とメッセージに分解  
            return self._extract_message(response)
        else:
            # 本文のみの場合は感情タグを補完する
            return self._extract_message(f"[EMOTION:NEUTRAL]\n{message}")
    
    def _extract_message(self, text: str) -> Response:
        EMOTION_PATTERN = re.compile(r"^\[\s*EMOTION\s*:\s*([A-Za-z_]+)\s*\]\s*", re.MULTILINE)
        match = EMOTION_PATTERN.match(text)

        if match is None:
            # 感情が取得できなかった場合はNEUTRAL扱い
            return Response(text, text.strip(), Emotion.NEUTRAL)

        emotion = Emotion.from_string(match.group(1))
        message = EMOTION_PATTERN.sub("", text, count=1).strip()
        return Response(text, message, emotion)
    
