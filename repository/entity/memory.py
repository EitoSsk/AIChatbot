# メモリクラス
# メモリ情報を作成・保持する
# メモリ情報は./data/memory.jsonに保存されている
# メモリ情報からシステムプロンプトを構成する情報を作成する

from datetime import datetime
import os
import json
import torch
from core.data.exception.file_exception import MemoryError, FileErrorType

class Memory:

    _MEMORY_FILE = "./data/memory.json"

    # コンストラクタ
    def __init__(self, config, logger):
        self._config = config
        self._logger = logger
        self._memory_data = {}
        self._loadMemory()

    # メモリ取得
    def getMemory(self):
        if self._memory_data == {}:
            ""
        else:
            return self._memory_data["memory"]

    # メモリ作成
    # 応答を長期記憶として保存する
    def create(self, model, tokenizer, summary):
        prompt = []
        prev_memory = "なし"
        if not self._memory_data == {}:
            prev_memory = self._memory_data["memory"]
        
        content = f"""あなたは長期記憶を更新するAIです。

以下には、

・現在の長期記憶
・最新の要約

が与えられます。
これらを統合し、新しい長期記憶を作成してください。
==============================================
現在の長期記憶
{prev_memory}
==============================================
最新の要約
{summary}
==============================================
以下は更新のルールです。

# 更新ルール

・以前の長期記憶をできるだけ維持してください。
・最新の要約に新しい重要な情報があれば追加してください。
・既存の情報を削除する場合は、本当に不要になった場合のみとしてください。
・情報量が多少増えても構いません。重要な情報を失わないことを優先してください。
・推測や憶測は記載しないでください。
・会話から確認できる事実のみを記載してください。
・出力は下記フォーマットのみとし、説明や前置きは不要です。

==============================================
以下は長期記憶の優先順位です。
優先順位が高いほど残しておくべき記憶となります

# 優先順位（高 → 低）

1. ユーザーとの約束・ルール
2. ユーザーとAIが共有した重要な出来事（思い出）
3. ユーザーの性格・考え方・価値観
4. 長期間変わらない好み・趣味
5. 長期的な目標・継続している活動

一時的な出来事や短期間しか意味を持たない情報は長期記憶へ残さないでください。
==============================================
フォーマット
下記のように見出しを付けてまとめてください。

# ユーザーについて
ユーザーの性格・価値観・考え方のみを記載してください。
趣味や好みは記載しないでください。

# 好み
ユーザーの趣味・嗜好・好きなもののみを記載してください。

# 思い出
ユーザーとAIが一緒に経験した重要な出来事のみを記載してください。
単なる質問内容は記載しないでください。

# 約束・ルール
ユーザーとAIの間で決まったルールのみを記載してください。

# 長期的な目標
ユーザーが長期間取り組んでいる目標のみを記載してください。
AI自身の目標は記載しないでください。
==============================================
"""
        message = {'role': "user", 'content': content, 'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        prompt.append(message)

        response = self._createMemory(model, tokenizer, prompt)
        memory = {'memory': response, 'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        self._createMemoryFile(memory)
        self._memory_data = memory

    # メモリを取得する
    # 存在しない場合はロードを終了する
    def _loadMemory(self):
        if not os.path.exists(self._MEMORY_FILE):
            return

        try:
            with open(self._MEMORY_FILE, 'r', encoding='utf-8') as f:
                self._memory_data = json.load(f)
        except (FileNotFoundError, PermissionError) as e:
            raise MemoryError(FileErrorType.READ.value)


    def _createMemory(self, model, tokenizer, prompt):
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
        return response
    
    def _createMemoryFile(self, memory):
        try:
            with open(self._MEMORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(memory, f, ensure_ascii=False, indent=4)
        except (FileNotFoundError, PermissionError) as e:
            raise MemoryError(FileErrorType.SAVE.value)