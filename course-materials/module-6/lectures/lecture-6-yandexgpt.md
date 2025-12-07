# Модуль 6: Генерация на YandexGPT

## Цели модуля
- Освоить YandexGPT API
- Изучить параметры генерации
- Создать эффективные RAG-промпты
- Обработать ошибки и лимиты

## Лекция: YandexGPT Integration

### 1. YandexGPT API Setup

**Получение API ключа:**
1. Зарегистрироваться в Yandex Cloud
2. Создать сервисный аккаунт
3. Назначить роль `ai.languageModels.user`
4. Создать API ключ

**Основные параметры:**
```python
YANDEX_API_KEY = "AQVNx..."
YANDEX_FOLDER_ID = "b1g..."
```

### 2. Базовый запрос

```python
import httpx

async def call_yandex_gpt(prompt, temperature=0.6):
    endpoint = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    
    payload = {
        "modelUri": f"gpt://{YANDEX_FOLDER_ID}/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": temperature,
            "maxTokens": 1000
        },
        "messages": [
            {
                "role": "system",
                "text": "Ты - помощник по курсу машинного обучения"
            },
            {
                "role": "user",
                "text": prompt
            }
        ]
    }
    
    headers = {
        "Authorization": f"Api-Key {YANDEX_API_KEY}",
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(endpoint, json=payload, headers=headers)
        result = response.json()
        
    return result["result"]["alternatives"][0]["message"]["text"]
```

### 3. Параметры генерации

**temperature (0.0 - 1.0):**
```python
# 0.0-0.3: Детерминированный, точный
answer = await call_yandex_gpt("2+2=?", temperature=0.1)
# → "4"

# 0.6-0.7: Сбалансированный
answer = await call_yandex_gpt("Расскажи про RAG", temperature=0.6)
# → Информативный, но креативный

# 0.8-1.0: Креативный, разнообразный
answer = await call_yandex_gpt("Придумай историю", temperature=0.9)
# → Очень креативный ответ
```

**maxTokens:**
```python
# Короткий ответ
response = call_gpt(prompt, maxTokens=100)

# Развернутый
response = call_gpt(prompt, maxTokens=2000)
```

### 4. RAG-промпты

**Базовый RAG промпт:**
```python
def build_rag_prompt(question, chunks):
    context = "\n\n".join([
        f"[Источник {i+1}]: {chunk['text']}"
        for i, chunk in enumerate(chunks)
    ])
    
    prompt = f"""На основе следующего контекста ответь на вопрос.

КОНТЕКСТ:
{context}

ВОПРОС: {question}

ИНСТРУКЦИИ:
- Используй только информацию из контекста
- Если информации недостаточно, так и скажи
- Укажи номера источников в ответе
- Отвечай на русском языке

ОТВЕТ:"""
    
    return prompt
```

**Продвинутый промпт:**
```python
def advanced_rag_prompt(question, chunks):
    # Добавить metadata
    context_parts = []
    for i, chunk in enumerate(chunks):
        source = chunk.get("source", "unknown")
        score = chunk.get("score", 0)
        
        context_parts.append(f"""
[Материал {i+1}] (релевантность: {score:.2f})
Источник: {source}
Текст: {chunk['text']}
""")
    
    context = "\n".join(context_parts)
    
    prompt = f"""Ты - AI ассистент курса по RAG и машинному обучению.
Твоя задача - помочь студенту понять материал курса.

МАТЕРИАЛЫ КУРСА:
{context}

ВОПРОС СТУДЕНТА:
{question}

ПРАВИЛА ОТВЕТА:
1. Используй только информацию из предоставленных материалов
2. Если в материалах нет ответа, честно скажи об этом
3. Структурируй ответ с заголовками и списками
4. Приводи примеры из материалов
5. Будь дружелюбным и понятным
6. Укажи источники в конце ответа

ОТВЕТ:"""
    
    return prompt
```

### 5. Streaming ответов

```python
async def stream_yandex_gpt(prompt):
    payload = {
        "modelUri": f"gpt://{YANDEX_FOLDER_ID}/yandexgpt-lite",
        "completionOptions": {
            "stream": True,  # Включаем streaming
            "temperature": 0.6,
            "maxTokens": 1000
        },
        "messages": [
            {"role": "user", "text": prompt}
        ]
    }
    
    async with httpx.AsyncClient() as client:
        async with client.stream(
            "POST",
            endpoint,
            json=payload,
            headers=headers,
            timeout=30.0
        ) as response:
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = json.loads(line[6:])
                    if "alternatives" in data.get("result", {}):
                        text = data["result"]["alternatives"][0]["message"]["text"]
                        yield text
```

### 6. Обработка ошибок

```python
class YandexGPTError(Exception):
    pass

async def safe_call_gpt(prompt, retries=3):
    for attempt in range(retries):
        try:
            response = await call_yandex_gpt(prompt)
            return response
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                # Rate limit
                wait_time = 2 ** attempt
                await asyncio.sleep(wait_time)
                continue
                
            elif e.response.status_code == 401:
                raise YandexGPTError("Invalid API key")
                
            elif e.response.status_code >= 500:
                # Server error
                if attempt < retries - 1:
                    await asyncio.sleep(1)
                    continue
                raise YandexGPTError("Service unavailable")
                
            else:
                raise YandexGPTError(f"API error: {e.response.status_code}")
                
        except httpx.TimeoutException:
            if attempt < retries - 1:
                continue
            raise YandexGPTError("Request timeout")
    
    raise YandexGPTError("Max retries exceeded")
```

### 7. Квоты и лимиты

**Лимиты YandexGPT:**
- Requests per minute: 20
- Tokens per request: 8000 (input + output)
- Max concurrent requests: 5

**Управление квотами:**
```python
from asyncio import Semaphore

class YandexGPTClient:
    def __init__(self, max_concurrent=5):
        self.semaphore = Semaphore(max_concurrent)
        self.request_times = []
    
    async def call(self, prompt):
        # Rate limiting
        await self._check_rate_limit()
        
        async with self.semaphore:
            response = await call_yandex_gpt(prompt)
            self.request_times.append(time.time())
            return response
    
    async def _check_rate_limit(self):
        now = time.time()
        # Убрать старые запросы (>1 минуты)
        self.request_times = [
            t for t in self.request_times 
            if now - t < 60
        ]
        
        if len(self.request_times) >= 20:
            # Подождать до освобождения квоты
            wait_time = 60 - (now - self.request_times[0])
            await asyncio.sleep(wait_time)
```

### 8. Оптимизация стоимости

**Сократить промпт:**
```python
def optimize_prompt(question, chunks, max_tokens=3000):
    prompt = build_rag_prompt(question, chunks)
    
    # Подсчитать токены (примерно)
    token_count = len(prompt.split()) * 1.3  # Коэффициент для русского
    
    if token_count > max_tokens:
        # Уменьшить количество chunks
        reduced_chunks = chunks[:3]
        prompt = build_rag_prompt(question, reduced_chunks)
    
    return prompt
```

**Кэширование:**
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_call_gpt(prompt_hash):
    return call_yandex_gpt(prompt)
```

## Практическое задание

1. Получить API ключ YandexGPT
2. Реализовать RAG-промпты
3. Протестировать разные temperature
4. Добавить обработку ошибок
5. Измерить качество ответов

## Тест

1. Какие версии YandexGPT существуют?
2. Что делает параметр temperature?
3. Как обработать ошибку 429?
4. Какие лимиты у YandexGPT API?
5. Как оптимизировать стоимость запросов?

