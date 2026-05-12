from fastapi import FastAPI
from pydantic import BaseModel
from database import get_exhibit_by_id
from prompt_builder import build_prompt
from llm_api import ask_llm
from question_classifier import classify_question   # новый импорт

app = FastAPI()

class MuseumRequest(BaseModel):
    id_exp: int
    text: str

# Сопоставление типа вопроса с максимальным количеством токенов
TYPE_TO_MAX_TOKENS = {
    "short_info": 300,
    "full_info": 2000,
    "history": 1000,
    "author": 700,
    "fact": 500,
}
DEFAULT_MAX_TOKENS = 500

@app.post("/ask")
def ask_museum(request: MuseumRequest):
    exhibit = get_exhibit_by_id(request.id_exp)
    if exhibit is None:
        return {"status": "error", "message": "Экспонат не найден"}

    # Определяем тип вопроса
    question_type = classify_question(request.text)
    
    # Берём подходящий max_tokens
    max_tokens = TYPE_TO_MAX_TOKENS.get(question_type, DEFAULT_MAX_TOKENS)
    
    # Строим промпт
    prompt = build_prompt(exhibit, request.text, question_type)
    
    # Вызываем LLM с возможным ограничением длины
    answer = ask_llm(prompt, max_tokens=max_tokens)
    
    return {
        "status": "success",
        "id_exp": request.id_exp,
        "answer": answer
    }