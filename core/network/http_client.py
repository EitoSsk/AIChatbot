# HTTPクライアントクラス

from core.data.exception.network_exception import NewWorkError
from logger import Logger
import requests
from config import Config


API_AUDIO_QUERY = "http://localhost:50021/audio_query"
API_SYNTHESIS = "http://localhost:50021/synthesis"

class HttpClient:

    _DEFAULT_TIMEOUT: tuple[int, int] = (5, 30)

    def __init__(self, config: Config, logger: Logger):
        self._config = config
        self._logger = logger

    def request(self,
        api: str,
        params: dict = None,
        json: dict = None,
        timeout: tuple[int, int] = _DEFAULT_TIMEOUT,
    ):
        response = requests.post(
            url = api,
            params = params,
            json = json,
            timeout = timeout,
        )
        try:
            response.raise_for_status()
            return response
        except:
            raise NewWorkError()
