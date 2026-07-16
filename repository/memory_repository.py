# メモリリポジトリクラス
# 長期記憶を作成、取得する機能を提供します。
# TODO:メモリ情報をシステムプロンプトを構築するために整理して提供します。

from repository.entity.memory import Memory

class MemoryRepository:

    # コンストラクタ
    def __init__(self, config, logger):
        self._config = config
        self._logger = logger
        self._Memory = Memory(config, logger)

    def createMemory(self, model, tokenizer, summary):
        self._Memory.create(model, tokenizer, summary)