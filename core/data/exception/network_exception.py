from enum import Enum

from core.data.exception.application_exception import ApplicationException


class NetworkError(ApplicationException):

    status_code: int = 200
    is_timeout: bool = False

    def __init__(
        self, 
        arg="",
        status_code=200,
        is_timeout=False
    ):
        super().__init__(arg)
        self.status_code = status_code
        self.is_timeout = is_timeout

    def __str__(self):
        return (
            f"通信に失敗しました。"
        )
