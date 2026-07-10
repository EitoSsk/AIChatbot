# モデルクラス
# このクラスはモデルの起動と管理、チャットのアウトプットのみ担当します。
# チャットはループで行われ、ユーザーの入力を受け取り、モデルに渡して応答を生成します。
# チャット機能自体はllm/chat.pyが担当します。

from llm.chat import Chat
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class Chatbot:

    # コンストラクタ
    # モデルとトークナイザーを生成し、Chatクラスのインスタンスを作成します。
    def __init__(self, config, logger):
        self._config = config
        self._logger = logger
        model_id = self._config.model_id
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        self._chat = Chat(model, tokenizer, self._config, self._logger)

    # チャットループを開始するメソッド
    def start_chat(self):
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
                response = self._chat.send_message(user_input)
                print(f"{self._config.assistant_name}: {response}")

    # チャットの終了処理
    def _close_chat(self):
        print("チャットを終了します。")