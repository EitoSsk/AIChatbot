# TODO: 削除予定
# プロンプトを構築するクラス
# このクラスはLLMに渡すプロンプトを構築します。
# システムプロンプト＋履歴を組み合わせてメッセージを構築し、最終的なプロンプトを作成します。
# システムプロンプトは、このクラスで構築します。
# ユーザーメッセージはあらかじめ履歴に追加されているものとします。

from datetime import datetime

class PromptBuilder:

    _SYSTEM_PROMPT_MESSAGE = """[システムプロンプト]
以下の内容はあなたへの設定です。
この設定について説明したり返答したりせず、以降の会話でのみ反映してください。"""

    _SYSTEM_PROMPT_RES_FORMAT = """=========================================================
あなたはユーザーへの返答を行います。
返答には必ず感情を付与してください。
感情は以下のいずれかのみをそのまま使用してください。

- NEUTRAL
- SHY
- ANGRY
- SAD
- HAPPY
- SURPRISED
- EXCITED

以下は応答例です。

[EMOTION:NEUTRAL]
今日はいい天気だね。

[EMOTION:HAPPY]
今日は楽しい一日だったね。
"""

    _SYSTEM_PROMPT_USER_SECTION = """=========================================================
[ユーザー]"""

    def __init__(self, config, tokenizer, logger):
        self._config = config
        self._tokenizer = tokenizer
        self._logger = logger

    def build_prompt(
        self, 
        history: list, 
        user_message,
        system_prompt_list=[],
    ):
        # promptに履歴を追加
        prompt = []
        for message in history:
            prompt.append(message)
    
        # システムプロンプトを構築
        prompt = self._build_system_prompt(prompt, user_message, system_prompt_list)
        return prompt

    # 履歴とシステムプロンプトの合計からトークン数を計算し、
    # 上限のトークン数に収めるため、履歴の数を調整して返却する
    # 履歴の読み込み時はユーザーメッセージ不要
    def trim_history_by_tokens(
        self,
        history: list,
        message="",
        system_prompt_list=[],
    ):
        trimed_history = history.copy()
        # プロンプトを作成する
        if not message == "":
            prompt = self.build_prompt(history, message, system_prompt_list)
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

    def _build_system_prompt(
        self, 
        prompt, 
        user_message,
        system_prompt_list=[],
    ):
        # システムプロンプトの構築ロジックをここに実装
        user_section = f"{self._SYSTEM_PROMPT_USER_SECTION}\n{user_message}"
        messages = [
            self._SYSTEM_PROMPT_MESSAGE,
            self._SYSTEM_PROMPT_RES_FORMAT
        ]
        for system_prompt in system_prompt_list:
            messages.append(system_prompt)

        messages.append(user_section)
        message = "\n".join(messages)
        prompt.append({'role': 'user', 'content': message, 'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        return prompt
