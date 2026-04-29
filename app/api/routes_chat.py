from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_chat_usecase, get_current_user_id
from app.core.errors import ServerMistake
from app.schemas.chat import ChatRequest, ChatResponse
from app.usecases.chat import UsecaseChat

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("", response_model=ChatResponse) #эндпоинт чата
async def chat(
    body: ChatRequest,
    user_id: int = Depends(get_current_user_id),
    usecase: UsecaseChat = Depends(get_chat_usecase),
):
    try:
        answer = await usecase.ask(
            user_id=user_id,
            prompt=body.prompt,
            system=body.system,
            max_history=body.max_history,
            temperature=body.temperature,
        )
        return ChatResponse(answer=answer)
    except ServerMistake as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(e))

@router.get("/history") #эндпоинт истории
async def get_history(
    user_id: int = Depends(get_current_user_id),
    usecase: UsecaseChat = Depends(get_chat_usecase),
):
    messages = await usecase.get_history(user_id)
    return [
        {
            "id": m.id,
            "role": m.role,
            "content": m.content,
            "created_at": m.created.at,
        }
        for m in messages
    ]

@router.delete("/history", status_code=status.HTTP_204_NO_CONTENT) #эндпоинт удаления истории
async def delete_history(
    user_id: int = Depends(get_current_user_id),
    usecase: UsecaseChat = Depends(get_chat_usecase),
):
    await usecase.clear_history(user_id)