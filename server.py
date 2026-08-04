from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from contextlib import asynccontextmanager
from core.llm.gguf_llm import GGUF_LLM
from llm.chat import Chat
from repository.character_repository import CharacterRepository
from repository.history_repository import HistoryRepository
from repository.memory_repository import MemoryRepository
from repository.summary_repository import SummaryRepository
from usecase.create_memory_usecase import CreateMemoryUseCase
from usecase.create_summary_usecase import CreateSummaryUseCase
from usecase.load_history_usecase import LoadHistoryUseCase
from logger import Logger
from config import Config

class ChatRequest(BaseModel):
    message: str

config = None
logger = None
model_id = None
model = None
history_repository = None
summary_repository = None
memory_repository = None
character_repository = None
load_history_usecase = None
create_summary_usecase = None
create_memory_usecase = None
chat_api = None

@asynccontextmanager
async def lifespan(app: FastAPI):

    global config
    global logger
    global model_id
    global model
    global history_repository
    global summary_repository
    global memory_repository
    global character_repository
    global load_history_usecase
    global create_summary_usecase
    global create_memory_usecase
    global chat_api

    print("Loading model...")

    config = Config()
    logger = Logger(config)
    model_id = config.model_id
    model = GGUF_LLM(model_id, config, logger)
    history_repository = HistoryRepository(config, logger)
    summary_repository = SummaryRepository(config, logger)
    memory_repository = MemoryRepository(config, logger)
    character_repository = CharacterRepository(config, logger)
    load_history_usecase = LoadHistoryUseCase(
        config,
        logger,
        model,
        history_repository, 
        summary_repository, 
        memory_repository,
        character_repository,
    )
    create_summary_usecase = CreateSummaryUseCase(
        summary_repository,
        history_repository,
        config,
        logger
    )
    create_memory_usecase = CreateMemoryUseCase(
        summary_repository,
        memory_repository,
        config,
        logger
    )
    chat_api = Chat(
        model, 
        history_repository, 
        summary_repository, 
        memory_repository,
        character_repository,
        config, 
        logger
    )
    # 履歴のロード
    is_new_month = load_history_usecase.execute()
    # 要約・長期記憶を作成する
    canCreateMemory = create_summary_usecase.execute(model, is_new_month)
    if canCreateMemory:
        create_memory_usecase.execute(model)
        
    print("Model loaded")

    yield

    print("Shutdown")

app = FastAPI(lifespan=lifespan)

@app.on_event("startup")
async def startup():
    print("CHAT API LOADED")

@app.post("/chat")
async def chat(request: ChatRequest):

    response = chat_api.send_message(request.message)

    return {
        "reply": response.message
    }

@app.get("/get_history")
async def get_history():
    history = history_repository.getHistory()
    return history

app.mount("/", StaticFiles(directory="static", html=True), name="static")
