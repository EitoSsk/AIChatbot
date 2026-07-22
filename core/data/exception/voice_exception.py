
from core.data.exception.application_exception import ApplicationException


class VoiceEngineNotRunningError(ApplicationException):

    def __str__(self):
        return (
            f"VOICEVOXエンジンが起動していません。"
        )
    
class VoicePlaybackError(ApplicationException):

    def __str__(self):
        return (
            f"音声の再生に失敗しました。"
        )
    
class VoiceTimeoutError(ApplicationException):

    def __str__(self):
        return (
            f"通信にタイムアウトしました。"
        )
    
class VoiceNetworkError(ApplicationException):

    def __str__(self):
        return (
            f"通信に失敗しました。"
        )
