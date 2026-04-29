from pydantic import BaseModel, Field

class ChatRequest(BaseModel): #реализована схема запроса-ответа
    prompt: str = Field(min_length=1)
    system: str | None = None
    max_history: int = Field(default=10, ge=0, le=50)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)

class ChatResponse(BaseModel):
    answer: str