from core.data.exception.application_exception import ApplicationException


class JsonKeysValidationError(ApplicationException):

    def __str__(self):
        return (
            f"バリデーションエラー: {self.args}"
        )
    
class JsonTypesValidationError(ApplicationException):

    def __str__(self):
        return (
            f"バリデーションエラー: {self.args}"
        )

class RangeValidationError(ApplicationException):

    def __str__(self):
        return (
            f"バリデーションエラー: {self.args}"
        )
    
class RequiredValidationError(ApplicationException):

    def __str__(self):
        return (
            f"バリデーションエラー: {self.args}"
        )
    
class ValidationOtherError(ApplicationException):

    def __str__(self):
        return (
            f"バリデーションエラー: {self.args}"
        )
