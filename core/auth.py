import os
from huggingface_hub import login

hf_token = os.getenv("HF_TOKEN")

if hf_token is None:
    print("HF_TOKEN が設定されていません。")
else:
    login(os.environ["HF_TOKEN"])
    print("Hugging Face にログインしました。")