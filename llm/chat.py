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
from config import Config
from logger import Logger
from repository.history_repository import HistoryRepository
from usecase.create_system_prompt_usecase import CreateSystemPromptUseCase
from utility.validation import LLMResponseValidation
from utility.formatter import ResponseFormatter

class Chat:

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
        self._system_prompt_list = CreateSystemPromptUseCase(
            self._history_repository,
            self._summary_repository,
            self._memory_repository,
            self._character_repository,
            self._config,
            self._logger
        ).execute()

    # メッセージを送信するメソッド
    # レスポンスを返却する
    def send_message(self, message):
        # 履歴のトリミング
        trimed_history = self._model.trim_history(
            message, 
            self._history_repository.getHistory(), 
            self._system_prompt_list
        )

        # 応答を生成
        count = 0
        while True:
            count += 1
            try:
                res = self._model.generate_response(
                    message, 
                    trimed_history, 
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
            except ValueError as e:
                if count > 1:
                    self._logger.error(e)
                    raise e
                trimed_history = self._model.trim_history_force(
                    trimed_history.copy()
                )

        # 履歴の更新
        self._history_repository.fetch_history("user", message, self._model.count_tokens(message), trimed_history)
        self._history_repository.fetch_history("assistant", response.plane_text, self._model.count_tokens(response.plane_text), self._history_repository.getHistory())
        return response
    
    def _extract_message(self, text: str) -> Response:
        EMOTION_PATTERN = re.compile(r"^\[\s*EMOTION\s*:\s*([A-Za-z_]+)\s*\]\s*", re.MULTILINE)
        match = EMOTION_PATTERN.match(text)

        if match is None:
            # 感情が取得できなかった場合はNEUTRAL扱い
            return Response(text, text.strip(), Emotion.NEUTRAL)

        emotion = Emotion.from_string(match.group(1))
        message = EMOTION_PATTERN.sub("", text, count=1).strip()
        message = ResponseFormatter.format(message)
        plane_text = f"[EMOTION:{emotion.name}]\n{message}"

        return Response(plane_text, message, emotion)
