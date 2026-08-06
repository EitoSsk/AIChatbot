# 起動処理

from core.data.exception.application_exception import ApplicationException
from logger import Logger
from config import Config
from app.chatbot import Chatbot

if __name__ == "__main__":
    e = None
    try: 
        config = Config()
        logger = Logger(config)
        chatbot = Chatbot(config, logger)
        chatbot.start_chat()
    except ApplicationException as error:
        e = error

    if (not e == None):
        print(e)
