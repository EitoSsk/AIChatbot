# ロガークラス

class Logger:

    def __init__(self, config):
        self._debug_level = config.debug_level

    def debug(self, message: str):
        if not self._debug_level == "debug": return
        print(message)

    def info(self, message: str):
        print(message)

    def warning(self, message: str):
        print(message)

    def error(self, message: str):
        print(message)
