# Модуль 4: Подготовка данных

## Цели модуля
- Освоить парсинг документов
- Изучить стратегии chunking
- Понять обработку текста
- Создать data pipeline

## Лекция: Data Preparation for RAG

### 1. Источники данных

**Типы документов:**
- PDF (технические спецификации)
- DOCX (документация)
- HTML (веб-страницы)
- TXT (лог-файлы)
- Markdown (wiki)
- JSON (структурированные данные)

### 2. Парсинг документов

**PDF:**
```python
import PyPDF2

def parse_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text
```

**DOCX:**
```python
import docx

def parse_docx(file_path):
    doc = docx.Document(file_path)
    text = "\n".join([p.text for p in doc.paragraphs])
    return text
```

**HTML:**
```python
from bs4 import BeautifulSoup

def parse_html(content):
    soup = BeautifulSoup(content, 'html.parser')
    # Удалить script, style
    for tag in soup(['script', 'style']):
        tag.decompose()
    return soup.get_text()
```

### 3. Очистка текста

**Проблемы:**
- Лишние пробелы и переносы
- Специальные символы
- Артефакты OCR
- Форматирование

**Решение:**
```python
import re

def clean_text(text):
    # Убрать лишние пробелы
    text = re.sub(r'\s+', ' ', text)
    
    # Убрать спецсимволы (кроме пунктуации)
    text = re.sub(r'[^\w\s\.,!?;:()\-]', '', text)
    
    # Нормализовать кавычки
    text = text.replace('"', '"').replace('"', '"')
    
    return text.strip()
```

### 4. Chunking стратегии

**Почему chunking?**
- LLM имеют лимит контекста
- Лучше precision в поиске
- Оптимизация стоимости

**Фиксированный размер:**
```python
def chunk_by_size(text, size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunk = text[start:end]
        chunks.append(chunk)
        start += size - overlap
    return chunks
```

**По предложениям:**
```python
def chunk_by_sentences(text, target_size=500):
    sentences = re.split(r'[.!?]+', text)
    chunks = []
    current = []
    current_size = 0
    
    for sent in sentences:
        if current_size + len(sent) > target_size:
            chunks.append(' '.join(current))
            current = [sent]
            current_size = len(sent)
        else:
            current.append(sent)
            current_size += len(sent)
    
    if current:
        chunks.append(' '.join(current))
    
    return chunks
```

**Semantic chunking:**
```python
# Разбиение по темам с помощью LLM
def semantic_chunk(text):
    # Определить границы тем
    # Группировать связанные предложения
    pass
```

### 5. Оптимальный размер chunk

**Trade-offs:**

| Размер | Pros | Cons |
|--------|------|------|
| 100-200 | Точный поиск | Мало контекста |
| 500-800 | Баланс | Универсально |
| 1000+ | Много контекста | Шум в поиске |

**Рекомендации:**
- Технические docs: 300-500
- Новости: 500-800
- Книги: 800-1000
- Overlap: 10-20% от размера

### 6. Metadata enrichment

```python
chunk_data = {
    "content": "RAG - это...",
    "metadata": {
        "source": "lecture_2.pdf",
        "page": 5,
        "section": "Архитектура",
        "author": "Иванов И.И.",
        "date": "2024-01-15",
        "course_id": 123,
        "module": 2,
        "difficulty": "beginner"
    }
}
```

**Польза метаданных:**
- Фильтрация результатов
- Ссылки на источники
- Ранжирование
- Аналитика

### 7. Data Pipeline

```python
class DocumentProcessor:
    def __init__(self, chunker, embedder):
        self.chunker = chunker
        self.embedder = embedder
    
    def process(self, file_path):
        # 1. Parse
        text = self.parse_file(file_path)
        
        # 2. Clean
        text = self.clean_text(text)
        
        # 3. Chunk
        chunks = self.chunker.chunk(text)
        
        # 4. Embed
        vectors = self.embedder.embed_batch(chunks)
        
        # 5. Store
        return [(chunk, vector) for chunk, vector in zip(chunks, vectors)]
```

### 8. Обработка специальных форматов

**Таблицы:**
```python
# Конвертировать в текст
"Таблица: Цены на продукты
Яблоки: 100 руб/кг
Груши: 150 руб/кг"
```

**Код:**
```python
# Сохранять с форматированием
"""
Python функция для расчета:
```python
def calculate(x, y):
    return x + y
```
"""
```

**Формулы:**
```python
# LaTeX → текст
"Формула E = mc² описывает эквивалентность массы и энергии"
```

## Практическое задание

1. Создать парсер для 3 форматов (PDF, DOCX, TXT)
2. Реализовать 2 стратегии chunking
3. Протестировать на реальных документах
4. Сравнить результаты поиска
5. Оптимизировать размер chunk

## Тест

1. Зачем нужен chunking?
2. Какой оптимальный размер chunk для техдокументации?
3. Почему важен overlap между chunks?
4. Какие метаданные полезны для RAG?
5. Как обрабатывать таблицы в документах?

