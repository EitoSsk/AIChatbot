
from config import Config
from llama_cpp import Llama

class GGUF_LLM:

    def __init__(self, model_id, config: Config, logger):
        self._config = config
        self._logger = logger
        self.load_model(model_id)

    def load_model(self, model_id: str):
        self._model = Llama(
            model_path=model_id,
            n_ctx=8192,
            # n_gpu_layers=-1,
            verbose=False
        )
        
    def generate_response(self, message: str, prompt: list, system: list):
        system_message = "\n".join(system)
        messages = [
            {
                "role": "system",
                "content": system_message
            }
        ]
        for p in prompt:
            messages.append(p)
        messages.append(
            {
                "role": "user",
                "content": message
            }
        )
        
        response = self._model.create_chat_completion(
            messages=messages,
            temperature=self._config.chat_temperature,
            top_p=self._config.chat_top_p,
            max_tokens=self._config.chat_max_tokens,
        )
        return response["choices"][-1]["message"]["content"]
            
    def trim_prompt(self, prompt: list, history: list):
       pass