from enum import Enum

from core.data.exception.application_exception import ApplicationException


class NewWorkError(ApplicationException):
    def __str__(self):
        return (
            f"通信に失敗しました。"
        )
