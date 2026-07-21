from enum import Enum

from exception.application_exception import ApplicationException


class NewWorkError(ApplicationException):
    def __str__(self):
        return (
            f"通信に失敗しました。"
        )
