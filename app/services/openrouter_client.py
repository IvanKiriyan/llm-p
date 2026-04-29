import httpx

from app.core.config import settings
from app.core.errors import ServerMistake

class ClientOpenRouter: #класс клиента для openrouter
    def __init__(self) -> None:
        self._base_url = settings.openrouter_base_url
        self._headers = { #собираем заголовки с настроек
            "Authorization": f"Bearer {settings.openrouter_api_key}",
            "HTTP-Referer": settings.openrouter_site_url,
            "X-Title": settings.openrouter_app_name,
        }
    
    async def complete(self, messages: list[dict], temperature: float = 0.7) -> str: #создание запроса
        payload = {
            "model": settings.openrouter_model,
            "messages": messages,
            "temperature": temperature,
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self._base_url}/chat/completions",
                headers=self._headers,
                json=payload,
                timeout=60.0,
            )
        if response.status_code !=200: #проверка статуса ответа
            raise ServerMistake(
                f"OpenRouter error {response.status_code}: {response.text}"
            )
        data = response.json()
        return data["choices"][0]["message"]["content"]