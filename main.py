# 起動処理

from exception.file_exception import ConfigError, HistoryError, PromptError
from llm.model import Model

if __name__ == "__main__":
    message = ""
    try: 
        model = Model()
        model.start_chat()
    except HistoryError as e:
        message = e
    except ConfigError as e:
        message = e
    except PromptError as e:
        message = e

    if (not message.strip()):
        print(message)
