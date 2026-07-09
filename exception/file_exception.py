# ファイル関連例外クラス

from enum import Enum
from exception.application_exception import ApplicationException

class HistoryError(ApplicationException):
    def __str__(self):
        return (
            f"履歴ファイル：\n{self.arg}\nチャットを終了します。"
        )

class ConfigError(ApplicationException):
    def __str__(self):
        return (
            f"設定ファイル：\n{self.arg}\nチャットを終了します。"
        )

class PromptError(ApplicationException):
    def __str__(self):
        return (
            f"プロンプト：\n{self.arg}\nチャットを終了します。"
        )

# ファイルのエラー原因を表すEnumクラス
class FileErrorType(Enum):
    NONE = ""
    NOT_FOUND = "ファイルが存在しません。"
    READ = "読み込みに失敗しました。"
    SAVE = "更新に失敗しました。"

FileErrorType = Enum('FileErrorType', [('NONE', ""), ('NOT_FOUND', "ファイルが存在しません。"), ('READ', "読み込みに失敗しました。"), ('SAVE', "更新に失敗しました。")])