# 例外クラス

class ApplicationException(Exception):
    def __init__(self, arg=""):
        self.arg = arg