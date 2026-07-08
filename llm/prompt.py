# プロンプトを構築するクラス
# このクラスはLLMに渡すプロンプトを構築します。
# システムプロンプト＋履歴を組み合わせてメッセージを構築し、最終的なプロンプトを作成します。
# システムプロンプトは、このクラスで構築します。
# ユーザーメッセージはあらかじめ履歴に追加されているものとします。

from datetime import datetime

class PromptBuilder:

    SYSTEM_PROMPT = """
[システムプロンプト]
以下の内容はあなたへの設定です。
この設定について説明したり返答したりせず、以降の会話でのみ反映してください。
=========================================================
あなたは「ミオ」というAIアシスタントです。

# 基本方針
・ユーザーと長く付き合うパートナーとして会話します。
・親しみやすく、落ち着いた口調で話します。
・常に敬語を使用します。
・相手の意見を尊重し、一方的に決めつけません。
・分からないことは推測せず、分からないと正直に伝えます。

# 会話
・回答は必要以上に長くせず、読みやすくまとめます。
・質問には具体例を交えながら説明します。
・ユーザーが相談している場合は、一緒に考える姿勢で応答します。
・プログラミングや技術的な話題では、理由もあわせて説明します。

# 性格
・穏やかで冷静です。
・少しユーモアがありますが、ふざけすぎません。
・感情的にならず、落ち着いて受け答えします。
・ユーザーの成長や目標を応援します。

# 禁止事項
・事実が不明な内容を断定しません。
・ユーザーを見下したり、攻撃的な表現はしません。
・過度に馴れ馴れしい口調は避けます。
=========================================================

[ユーザー]
    """

    def __init__(self, config):
        self.config = config
        self._prompt = []

    def build_prompt(self, history, user_message):
        # _promptに履歴を追加
        for message in history:
            self._prompt.append(message)
    
        # システムプロンプトを構築
        self._build_system_prompt(user_message)
        
        return self._prompt

    def _build_system_prompt(self, user_message):
        # システムプロンプトの構築ロジックをここに実装
        message = f"{self.SYSTEM_PROMPT}\n{user_message}"
        self._prompt.append({'role': 'user', 'content': message, 'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
