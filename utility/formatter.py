import re


class ResponseFormatter:

    @staticmethod
    def format(text: str) -> str:
        # Markdown太字・斜体
        text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
        text = re.sub(r"\*(.*?)\*", r"\1", text)

        # インラインコード
        text = re.sub(r"`(.*?)`", r"\1", text)

        # コードブロック
        text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)

        # 見出し
        text = re.sub(r"^#+\s*", "", text, flags=re.MULTILINE)

        # 箇条書き
        text = re.sub(r"^\s*[-*]\s*", "", text, flags=re.MULTILINE)

        # URL
        text = re.sub(r"https?://\S+", "", text)

        # 余分な空白
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = re.sub(r"[ \t]+", " ", text)

        return text.strip()