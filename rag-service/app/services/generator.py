"""
Generator service with RAG-optimized prompts
"""
import httpx
from typing import List
from app.config import settings
from app.models.response import Chunk

class GeneratorService:
    def __init__(self):
        self.api_key = settings.YANDEX_API_KEY
        self.folder_id = settings.YANDEX_FOLDER_ID
        self.model = settings.YANDEX_MODEL
        self.endpoint = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    
    async def generate_with_context(
        self, 
        question: str, 
        chunks: List[Chunk]
    ) -> str:
        """Generate answer using RAG context"""
        
        if not self.api_key or not self.folder_id:
            return "YandexGPT не настроен. Установите YANDEX_API_KEY и YANDEX_FOLDER_ID."
        
        # Build RAG prompt
        prompt = self._build_rag_prompt(question, chunks)
        
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
                    "text": "Ты - помощник курса по RAG и YandexGPT. Отвечай на вопросы студентов на основе предоставленных материалов курса. Используй только информацию из материалов. Если информации недостаточно - так и скажи."
                },
                {
                    "role": "user",
                    "text": prompt
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
    
    def _build_rag_prompt(self, question: str, chunks: List[Chunk]) -> str:
        """Build RAG prompt with context chunks"""
        
        if not chunks:
            return f"""У меня нет материалов курса по этому вопросу.

ВОПРОС: {question}

Ответь на основе общих знаний о RAG и машинном обучении."""
        
        # Build context from chunks
        context_parts = []
        for i, chunk in enumerate(chunks, 1):
            context_parts.append(
                f"[Материал {i}] (релевантность: {chunk.score:.2f}, источник: {chunk.source})\n{chunk.content}"
            )
        
        context = "\n\n".join(context_parts)
        
        prompt = f"""На основе следующих материалов курса ответь на вопрос студента.

МАТЕРИАЛЫ КУРСА:
{context}

ВОПРОС СТУДЕНТА:
{question}

ИНСТРУКЦИИ:
- Используй только информацию из предоставленных материалов
- Отвечай четко и по существу
- Если информации недостаточно, так и скажи
- Используй примеры из материалов курса
- Структурируй ответ для удобного чтения

ОТВЕТ:"""
        
        return prompt
    
    async def check_health(self) -> bool:
        """Check if YandexGPT is accessible"""
        try:
            result = await self.generate_with_context("test", [])
            return "Ошибка" not in result
        except:
            return False

generator_service = GeneratorService()

