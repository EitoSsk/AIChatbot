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

    def __init__(self, config, tokenizer, logger):
        self._config = config
        self._tokenizer = tokenizer
        self._logger = logger

    def build_prompt(self, history, user_message):
        # promptに履歴を追加
        prompt = []
        for message in history:
            prompt.append(message)
    
        # システムプロンプトを構築
        prompt = self._build_system_prompt(prompt, user_message)
        return prompt

    # 履歴とシステムプロンプトの合計からトークン数を計算し、
    # 上限のトークン数に収めるため、履歴の数を調整して返却する
    # 履歴の読み込み時はユーザーメッセージ不要
    def trim_history_by_tokens(self, history, message=""):
        trimed_history = history.copy()
        # プロンプトを作成する
        if not message == "":
            prompt = self.build_prompt(history, message)
        else:
            prompt = history

        if len(prompt) == 0: return []

        while True:
            if len(prompt) < 2: break

            # トークナイズ
            tokens = self._tokenizer.apply_chat_template(
                prompt,
                tokenize=True,
                return_tensors="pt",
                add_generation_prompt=True,
            )
            # message_max_tokensの上限を超えなくなるまで履歴を破棄する
            if tokens["input_ids"].shape[-1] > self._config.message_max_tokens:
                del prompt[:2]
                del trimed_history[:2]
            else:
                break

        return trimed_history

    def _build_system_prompt(self, prompt, user_message):
        # システムプロンプトの構築ロジックをここに実装
        message = f"{self.SYSTEM_PROMPT}\n{user_message}"
        prompt.append({'role': 'user', 'content': message, 'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        return prompt
