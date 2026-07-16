# メモリリポジトリクラス
# 長期記憶を作成、取得する機能を提供します。
# TODO:メモリ情報をシステムプロンプトを構築するために整理して提供します。

from repository.entity.memory import Memory

class MemoryRepository:

    _SYSTEM_PROMPT = """以下は、これまでの会話から長期間保持すべきと判断された情報です。

内容には、
・ユーザーの性格
・価値観
・好み
・重要な思い出
・ユーザーとの約束
・長期的な目標
などが含まれています。

会話では必要に応じて自然に参考にしてください。
内容を無理に話題へ出す必要はありません。
新しい情報によって矛盾が生じた場合は、現在の会話を優先してください。

[長期記憶]
"""

    # コンストラクタ
    def __init__(self, config, logger):
        self._config = config
        self._logger = logger
        self._memory = Memory(config, logger)

    def createMemory(self, model, tokenizer, summary):
        self._memory.create(model, tokenizer, summary)

    def build_prompt(self):
        memory = self._memory.getMemory()
        if memory == "":
            memory = "なし"
        prompt = [
            "=========================================================",
            self._SYSTEM_PROMPT,
            memory,
        ]

        return "\n".join(prompt)