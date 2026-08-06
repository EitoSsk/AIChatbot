# モデルクラス
# このクラスはモデルの起動と管理、チャットのアウトプットのみ担当します。
# チャットはループで行われ、ユーザーの入力を受け取り、モデルに渡して応答を生成します。
# チャット機能自体はllm/chat.pyが担当します。

from core.data.exception.validation_exception import ResponseEmptyError
from core.llm.gguf_llm import GGUF_LLM
from app.chat import Chat
from repository.character_repository import CharacterRepository
from speech.tts import TTS
from repository.history_repository import HistoryRepository
from repository.memory_repository import MemoryRepository
from repository.summary_repository import SummaryRepository
from usecase.create_memory_usecase import CreateMemoryUseCase
from usecase.create_summary_usecase import CreateSummaryUseCase
from usecase.load_history_usecase import LoadHistoryUseCase

class Chatbot:

    # コンストラクタ
    # モデルとトークナイザーを生成し、Chatクラスのインスタンスを作成します。
    def __init__(self, config, logger):
        self._config = config
        self._logger = logger
        model_id = self._config.model_id
        self._model = GGUF_LLM(model_id, self._config, self._logger)
        self._history_repository = HistoryRepository(config, logger)
        self._summary_repository = SummaryRepository(config, logger)
        self._memory_repository = MemoryRepository(config, logger)
        self._character_repository = CharacterRepository(config, logger)
        self._load_history_usecase = LoadHistoryUseCase(
            self._config,
            self._logger,
            self._model,
            self._history_repository, 
            self._summary_repository, 
            self._memory_repository,
            self._character_repository,
        )
        self._create_summary_usecase = CreateSummaryUseCase(
            self._summary_repository,
            self._history_repository,
            self._config,
            self._logger
        )
        self._create_memory_usecase = CreateMemoryUseCase(
            self._summary_repository,
            self._memory_repository,
            self._config,
            self._logger
        )
        self._chat = Chat(
            self._model, 
            self._history_repository, 
            self._summary_repository, 
            self._memory_repository,
            self._character_repository,
            self._config, 
            self._logger
        )
        self._tts = TTS(
            self._config,
            self._logger,
            self._character_repository
        )

    # チャットループを開始するメソッド
    def start_chat(self):
        # 履歴のロード
        is_new_month = self._load_history_usecase.execute()
        # 要約・長期記憶を作成する
        canCreateMemory = self._create_summary_usecase.execute(self._model, is_new_month)
        if canCreateMemory:
            self._create_memory_usecase.execute(self._model)

        # チャットを開始する
        self._chat_loop()

    # チャットループの実装
    # ユーザーの入力を受け取り、モデルに渡して応答を生成し、出力します。
    # チャットはCUI上で行われ、ユーザーが 'exit' と入力するまで続きます。
    # Ctrl+Cで終了することも可能です。動作は'exit'と同じです。
    # 空のメッセージを入力した場合は、再度入力を促します。
    def _chat_loop(self):
        print("チャットを開始します。終了するには 'exit' か 'Ctrl+C' と入力してください。")
        while True:
            user_input = ""
            can_close = False

            try:
                user_input = input(f"{self._config.user_name}: ")
                if user_input.lower() == "exit":
                    can_close = True
            except KeyboardInterrupt:
                can_close = True

            # 終了判定
            if (can_close):
                self._close_chat()
                break
            if not user_input.strip():
                continue
            else:
                try: 
                    response = self._chat.send_message(user_input)
                    self._tts.play(response)
                    print(f"{self._config.assistant_name}: {response.message}")
                    self._tts.wait()
                except ResponseEmptyError:
                    print("ごめんね。うまく返答を生成できなかったみたい。もう一度試してくれる？")

    # チャットの終了処理
    def _close_chat(self):
        print("チャットを終了します。")