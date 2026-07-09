# 起動処理

from logger import Logger
from config import Config
from exception.file_exception import ConfigError, HistoryError, PromptError
from llm.model import Model

if __name__ == "__main__":
    e = None
    try: 
        config = Config()
        logger = Logger(config)
        model = Model(config, logger)
        model.start_chat()
    except (HistoryError, ConfigError, PromptError) as error:
        e = error

    if (not e == None):
        print(e)
