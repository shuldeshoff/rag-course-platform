"""
YandexGPT service for text generation
"""
import httpx
from app.config import settings

class YandexGPTService:
    def __init__(self):
        self.api_key = settings.YANDEX_API_KEY
        self.folder_id = settings.YANDEX_FOLDER_ID
        self.model = settings.YANDEX_MODEL
        self.endpoint = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    
    async def generate(self, prompt: str, context: str = "") -> str:
        """Generate text using YandexGPT"""
        if not self.api_key or not self.folder_id:
            return "YandexGPT не настроен. Установите YANDEX_API_KEY и YANDEX_FOLDER_ID."
        
        full_prompt = f"{context}\n\n{prompt}" if context else prompt
        
        payload = {
            "modelUri": f"gpt://{self.folder_id}/{self.model}",
            "completionOptions": {
                "stream": False,
                "temperature": 0.6,
                "maxTokens": 1000
            },
            "messages": [
                {
                    "role": "system",
                    "text": "Ты - помощник курса по RAG и YandexGPT. Отвечай на вопросы студентов."
                },
                {
                    "role": "user",
                    "text": full_prompt
                }
            ]
        }
        
        headers = {
            "Authorization": f"Api-Key {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.endpoint,
                    json=payload,
                    headers=headers
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result["result"]["alternatives"][0]["message"]["text"]
                else:
                    return f"Ошибка YandexGPT API: {response.status_code}"
        except Exception as e:
            return f"Ошибка подключения к YandexGPT: {str(e)}"
    
    async def check_health(self) -> bool:
        """Check if YandexGPT is accessible"""
        try:
            result = await self.generate("test")
            return "Ошибка" not in result
        except:
            return False

yandex_service = YandexGPTService()

