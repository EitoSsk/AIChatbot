# 起動処理

from logger import Logger
from config import Config
from exception.file_exception import ConfigError, HistoryError, PromptError
from llm.chatbot import Chatbot

if __name__ == "__main__":
    e = None
    try: 
        config = Config()
        logger = Logger(config)
        chatbot = Chatbot(config, logger)
        chatbot.start_chat()
    except (HistoryError, ConfigError, PromptError) as error:
        e = error

    if (not e == None):
        print(e)
