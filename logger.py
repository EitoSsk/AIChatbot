# ロガークラス

class Logger:

    def __init__(self, config):
        self._debug_level = config.debug_level

    def debug(self, message: str):
        if not self._debug_level == "debug": return
        print(f"[DEBUG] {message}")

    def info(self, message: str):
        print(f"[INFO] {message}")

    def warning(self, message: str):
        print(f"[WARNING] {message}")

    def error(self, message: str):
        print(f"[ERROR] {message}")

    def error(self, e: Exception):
        print(f"[ERROR] {e}")
