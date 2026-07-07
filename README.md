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

# 履歴について

jsonファイルでやり取りを保存しておく。
直近数十件の履歴を保持して、軽量化を図る。

### 履歴の上限について

メッセージの上限は、推論の高速化のために小さく設定する。
20~30件くらいの想定。

永続化しておく履歴はすべて残しておいても問題ない。
数万件程度は保存しておく。

### 履歴の検索（TODO）

過去に行っていた会話を遡りたいとき、
検索と要約を行って、直近の履歴に追加する。
検索結果をまとめて要約はAIにやらせる。

# ロールプレイについて（TODO）

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