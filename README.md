# 実行方法

start_chat.batを実行する

# 設計方針

project/
│
├── main.py             # 起動処理。
├── config.py           # モデルの情報、履歴の管理など
│
├── llm/
│   ├── model.py        # チャットのアウトプットのみ担当
│   ├── chat.py         # 入力、履歴更新、modelの呼び出し、応答返却
│   ├── prompt.py       # ユーザーやキャラクターのメタデータの組み立て
│   └── history.py      # 履歴の読みこみ、保存、破棄。
│
├── speech/
│   ├── stt.py          # Whisper
│   ├── tts.py          # VOICEVOX
│   └── audio.py        # マイク・再生
│
├── data/
│   ├── history.json    # 履歴ファイル（DBに置き換えることも考慮）
│   ├── character.json  # キャラクター性、ロールプレイのための設定
│   └── config.json     # 設定ファイル（DBに置き換えることも考慮）
│
└── models/

# ロールプレイについて

以下のように設定を持つ。
```
{
    "name": "ミオ",
    "age": "25",
    "gender": "female",
    "personality": "穏やか",
    "speech_style": "敬語",
    "background": "...",
    "system_prompt": "..."
}
```

感情表現も将来的に設定を持ち、音声に反映する。
```
{
    "emotion": {
        "joy": 20,
        "sadness": 0,
        "anger": 0,
        "fatigue": 5
    }
}
```


# 手順

1. Gemmaとのテキストチャット（完成）
2. チャットの継続性と会話履歴の実装（JSON）
3. ChatBot クラスにまとめる
4. VOICEVOXで音声読み上げ
5. Whisperで音声入力
6. GUI化（Webまたはデスクトップ）