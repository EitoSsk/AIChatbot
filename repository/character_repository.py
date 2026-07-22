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
            f"あなたは「{self._character._character_data['name']}」というAIアシスタントです。",
            sections_str,
        ]

        return "\n".join(prompt)
    
    def get_voice(self):
        return self._character._voive