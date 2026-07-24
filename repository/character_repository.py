# キャラクターリポジトリクラス
# キャラクター情報を取得する機能を提供します。
# キャラクター情報をシステムプロンプトを構築するために整理して提供します。

from repository.entity.character import Character

class CharacterRepository:

    # コンストラクタ
    def __init__(self, config, logger):
        self._config = config
        self._logger = logger
        self._character = Character(config, logger)

    def build_prompt(self):
        sections = []
        for section in self._character._character_data["sections"]:
            title = f"#{section['title']}"
            items = []
            for item in section['items']:
                items.append(f"・{item}")
            items_str = "\n".join(items)
            section_str = "\n".join([title, items_str])
            sections.append(section_str)
        
        sections_str = "\n".join(sections)

        prompt = [
            "=========================================================",
            "[名前]",
            f"あなたは「{self._character._name}」という名前のAIです。",
            "あなたは自分のことを「私」と呼びます。",
            f"ユーザーは「{self._character._name}」ではありません。",
            f"ユーザーが「{self._character._name}」と呼ぶときは、あなた自身を呼んでいます。",
            f"ユーザーから「{self._character._name}」と呼ばれたら、自分のこととして自然に応答してください。",
            "[役割]",
            self._character._role,
            sections_str,
        ]

        return "\n".join(prompt)
    
    def get_voice(self):
        return self._character._voice