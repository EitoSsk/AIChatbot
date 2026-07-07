#チャット機能を持つクラス
#このクラスは以下の機能を持つ
#テキストの送信
#チャット履歴の更新
#応答返却

import torch

class Chat:

    # コンストラクタ
    def __init__(self, model, tokenizer):
        self.chat_history = []
        self.model = model
        self.tokenizer = tokenizer

    # メッセージを送信するメソッド
    # レスポンスを返却する
    def send_message(self, message):
        # メッセージをチャット履歴に追加
        self.chat_history.append({"role": "user", "content": message})
        # 応答を生成
        response = self.generate_response(self.chat_history)
        # 応答をチャット履歴に追加
        self.chat_history.append({"role": "assistant", "content": response})
        return response

    # インプットから応答を生成するメソッド
    # ここでは、モデルを使用して応答を生成するロジックを実装する
    # tokenizer と model を使用して、入力メッセージに基づいて応答を生成する
    def generate_response(self, history):
        # トークナイズ
        inputs = self.tokenizer.apply_chat_template(
            history,
            tokenize=True,
            return_dict=True,
            return_tensors="pt",
            add_generation_prompt=True,
        )
        inputs = {k: v.to(self.model.device) for k, v in inputs.items()}

        # 推論
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=256,
                temperature=0.7,
            )

        # 応答をデコード
        response = self.tokenizer.decode(
            outputs[0][inputs["input_ids"].shape[-1]:],
            skip_special_tokens=True,
        )

        return response

    # TODO: history.pyからチャット履歴を取得するメソッドを追加する
    def get_chat_history(self):
        return self.chat_history
    