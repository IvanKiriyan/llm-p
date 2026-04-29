from app.db.models import ChatMessage
from app.repositories.chat_messages import ChatMessageRepository
from app.services.openrouter_client import ClientOpenRouter

class UsecaseChat: #бизнес логика общения с llm
    def __init__(self, chat_repo: ChatMessageRepository, 
                 llm: ClientOpenRouter) -> None:
        self._chat_repo = chat_repo
        self._llm = llm

    async def ask( #запрос к модели
            self,
            user_id: int,
            prompt: str,
            system: str | None = None,
            max_history: int = 10,
            temperature: float = 0.7,
    ) -> str:
        messages = []

        if system:
            messages.append({"role": "system", "content": system})
        
        history = await self._chat_repo.get_nlast_message(user_id, max_history)
        for msg in history:
            messages.append({"role": msg.role, "content": msg.content})
        
        messages.append({"role": "user", "content": prompt})

        await self._chat_repo.add(user_id=user_id, role="user", content=prompt)

        answer = await self._llm.complete(messages=messages, 
                                          temperature=temperature)
        
        await self._chat_repo.add(user_id=user_id, role="assistant",
                                  content=answer)
        
        return answer
    
    async def get_history(self, user_id: int) -> list[ChatMessage]: #получение истории
        return await self._chat_repo.get_nlast_message(user_id, n=100)
    
    async def clear_history(self, user_id: int) -> None: #очистка истории
        await self._chat_repo.clear_history(user_id)