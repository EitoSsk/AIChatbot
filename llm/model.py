# モデルクラス
# このクラスはモデルの起動と管理、チャットのアウトプットのみ担当します。
# チャットはループで行われ、ユーザーの入力を受け取り、モデルに渡して応答を生成します。
# チャット機能自体はllm/chat.pyが担当します。


from config import Config
from llm.chat import Chat
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class Model:

    # コンストラクタ
    # モデルとトークナイザーを生成し、Chatクラスのインスタンスを作成します。
    def __init__(self):
        self.config = Config()
        model_id = self.config.model_id
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        self.chat = Chat(model, tokenizer, self.config)

    # チャットループを開始するメソッド
    def start_chat(self):
        self.chat_loop()

    # チャットループの実装
    # ユーザーの入力を受け取り、モデルに渡して応答を生成し、出力します。
    # チャットはCUI上で行われ、ユーザーが 'exit' と入力するまで続きます。
    # 空のメッセージを入力した場合は、再度入力を促します。
    def chat_loop(self):
        print("チャットを開始します。終了するには 'exit' と入力してください。")
        while True:
            user_input = input(f"{self.config.user_name}: ")
            if user_input.lower() == "exit":
                print("チャットを終了します。")
                break
            if not user_input.strip():
                continue
            response = self.chat.send_message(user_input)
            print(f"{self.config.assistant_name}: {response}")