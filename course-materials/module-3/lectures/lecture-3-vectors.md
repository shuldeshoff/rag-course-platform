# Модуль 3: Векторные хранилища

## Цели модуля
- Понять математику векторов
- Изучить метрики сходства
- Освоить векторные базы данных
- Настроить Qdrant

## Лекция: Vector Databases

### 1. Векторные представления

**Что такое вектор?**
```python
text = "собака"
vector = [0.2, -0.5, 0.8, 0.1, -0.3, ...]  # 1024 измерений
```

Каждая позиция - это "признак" семантического значения.

**Пространство эмбеддингов:**
```
     кот •
          \
   кошка • \ (близко)
            \
             • собака
            /
     пес • / (близко)
```

### 2. Метрики сходства

**Косинусное расстояние (Cosine):**
```python
similarity = cos(angle) = (A · B) / (||A|| ||B||)
# Диапазон: [-1, 1], чем выше - тем похожее
```

**Евклидово расстояние:**
```python
distance = sqrt(Σ(ai - bi)²)
# Чем меньше - тем похожее
```

**Скалярное произведение (Dot Product):**
```python
similarity = Σ(ai * bi)
```

**Когда что использовать:**
- Cosine - для текстов (инвариантна к длине)
- Euclidean - для изображений
- Dot Product - для normalized векторов

### 3. Векторные базы данных

**Зачем нужны:**
- Хранение миллионов векторов
- Быстрый поиск (< 100ms)
- Фильтрация по метаданным
- Масштабирование

**Популярные решения:**
- **Qdrant** - Rust, open-source, быстрый
- **Pinecone** - облачный, managed
- **Milvus** - масштабируемый
- **Chroma** - легковесный
- **Weaviate** - с GraphQL

### 4. Индексы для поиска

**Naive (Linear) Search:**
```python
for vector in database:
    distance = calculate(query, vector)
# O(n) - медленно для больших баз
```

**HNSW (Hierarchical Navigable Small World):**
```
Level 2:  A -------- B
           \        /
Level 1:   C -- D -- E
            \ /  \ /
Level 0:    F-G-H-I-J-K
```
- Быстрый поиск: O(log n)
- Высокое качество
- Используется в Qdrant

**IVF (Inverted File Index):**
- Кластеризация векторов
- Поиск только в близких кластерах
- Trade-off: скорость vs точность

### 5. Qdrant Setup

**Docker:**
```bash
docker run -p 6333:6333 qdrant/qdrant
```

**Python клиент:**
```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

client = QdrantClient("localhost", port=6333)

# Создать коллекцию
client.create_collection(
    collection_name="my_docs",
    vectors_config=VectorParams(
        size=1024,
        distance=Distance.COSINE
    )
)

# Добавить векторы
client.upsert(
    collection_name="my_docs",
    points=[
        {
            "id": 1,
            "vector": [0.1, 0.2, ...],
            "payload": {"text": "...", "source": "doc1"}
        }
    ]
)

# Поиск
results = client.search(
    collection_name="my_docs",
    query_vector=[0.1, 0.2, ...],
    limit=5
)
```

### 6. Оптимизация поиска

**Фильтрация:**
```python
from qdrant_client.models import Filter, FieldCondition

results = client.search(
    collection_name="docs",
    query_vector=vector,
    query_filter=Filter(
        must=[
            FieldCondition(
                key="course_id",
                match={"value": 123}
            )
        ]
    ),
    limit=5
)
```

**Параметры качества:**
```python
# HNSW параметры
{
    "m": 16,  # число соседей (↑ = точнее, медленнее)
    "ef_construct": 100,  # качество индекса
}

# Search параметры
search_params = {
    "hnsw_ef": 128  # точность поиска
}
```

## Практическое задание

1. Установить Qdrant локально
2. Создать коллекцию для курса
3. Загрузить 100 тестовых векторов
4. Протестировать разные метрики
5. Сравнить скорость поиска с/без индекса

## Тест

1. Какая метрика лучше для текстов?
2. Что такое HNSW?
3. В чем разница между Qdrant и обычной БД?
4. Как работает фильтрация в Qdrant?
5. Что влияет на скорость поиска?

