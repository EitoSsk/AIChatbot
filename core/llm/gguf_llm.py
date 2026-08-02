
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
            n_ctx=self._config.message_max_tokens,
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
            top_k=self._config.chat_top_k,
            max_tokens=self._config.chat_max_tokens,
        )
        return response["choices"][-1]["message"]["content"]
            
    def trim_history(self, message: str, history: list, system_prompt_list: list):
        if not len(history) > 0:
            return history.copy()

        total_tokens = 0
        system_message = "\n".join(system_prompt_list)
        total_tokens += len(self._model.tokenize(message.encode("utf-8")))
        total_tokens += len(self._model.tokenize(system_message.encode("utf-8")))
        total_tokens += self._config.chat_template_overhead
        for h in history:
            total_tokens += h["tokens"]

        if total_tokens <= self._config.message_max_tokens:
            return history.copy()

        trimed_history = history.copy()
        while total_tokens > self._config.message_max_tokens and len(history) > 0:
            removed = trimed_history[:2]
            for r in removed:
                total_tokens -= r["tokens"]
            
            del trimed_history[:2]

        return trimed_history

    def count_tokens(self, message: str):
        return len(self._model.tokenize(message.encode("utf-8")))