# Модуль 5: Retrieval на практике

## Цели модуля
- Освоить создание эмбеддингов
- Реализовать семантический поиск
- Изучить ре-ранжирование
- Оптимизировать retrieval

## Лекция: Advanced Retrieval

### 1. Модели эмбеддингов

**sentence-transformers:**
```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('intfloat/multilingual-e5-large')

# Один текст
embedding = model.encode("Что такое RAG?")
print(embedding.shape)  # (1024,)

# Batch
texts = ["RAG", "LLM", "Vector DB"]
embeddings = model.encode(texts)
print(embeddings.shape)  # (3, 1024)
```

**Популярные модели:**
- `all-MiniLM-L6-v2` - быстрая, 384 dim
- `multilingual-e5-large` - мультиязычная, 1024 dim
- `e5-mistral-7b-instruct` - лучшее качество

### 2. Semantic Search

```python
class SemanticSearcher:
    def __init__(self, embedder, vector_db):
        self.embedder = embedder
        self.db = vector_db
    
    def search(self, query, top_k=5):
        # 1. Embed query
        query_vector = self.embedder.encode(query)
        
        # 2. Search
        results = self.db.search(
            query_vector=query_vector,
            limit=top_k
        )
        
        # 3. Format results
        return [
            {
                "text": r.payload["content"],
                "score": r.score,
                "metadata": r.payload.get("metadata", {})
            }
            for r in results
        ]
```

### 3. Гибридный поиск

**Semantic + Keyword:**
```python
def hybrid_search(query, top_k=10):
    # Semantic search
    semantic_results = semantic_search(query, k=top_k)
    
    # Keyword search (BM25)
    keyword_results = bm25_search(query, k=top_k)
    
    # Fusion
    combined = reciprocal_rank_fusion(
        semantic_results,
        keyword_results
    )
    
    return combined[:top_k]
```

**Reciprocal Rank Fusion:**
```python
def rrf(results_lists, k=60):
    scores = defaultdict(float)
    
    for results in results_lists:
        for rank, doc in enumerate(results):
            scores[doc.id] += 1 / (k + rank + 1)
    
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)
```

### 4. Ре-ранжирование

**Cross-encoder:**
```python
from sentence_transformers import CrossEncoder

reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-12-v2')

def rerank(query, documents, top_k=5):
    # Создать пары (query, doc)
    pairs = [[query, doc["text"]] for doc in documents]
    
    # Предсказать релевантность
    scores = reranker.predict(pairs)
    
    # Пересортировать
    for doc, score in zip(documents, scores):
        doc["rerank_score"] = score
    
    documents.sort(key=lambda x: x["rerank_score"], reverse=True)
    return documents[:top_k]
```

### 5. Фильтрация результатов

```python
def filtered_search(query, filters, top_k=5):
    query_vector = embedder.encode(query)
    
    # Построить фильтр
    qdrant_filter = Filter(
        must=[
            FieldCondition(
                key="course_id",
                match=MatchValue(value=filters["course_id"])
            )
        ]
    )
    
    if "module" in filters:
        qdrant_filter.must.append(
            FieldCondition(
                key="module",
                match=MatchValue(value=filters["module"])
            )
        )
    
    results = qdrant_client.search(
        collection_name="docs",
        query_vector=query_vector,
        query_filter=qdrant_filter,
        limit=top_k
    )
    
    return results
```

### 6. Query expansion

```python
async def expand_query(query, llm):
    prompt = f"""Перефразируй вопрос 3 разными способами:
    
Исходный: {query}

1.
2.
3."""
    
    expansions = await llm.generate(prompt)
    return [query] + expansions.split('\n')

# Поиск по всем вариантам
async def expanded_search(query, top_k=5):
    queries = await expand_query(query)
    
    all_results = []
    for q in queries:
        results = search(q, top_k)
        all_results.append(results)
    
    # Deduplicate и merge
    return merge_results(all_results)
```

### 7. Оптимизация производительности

**Кэширование эмбеддингов:**
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_embed(text):
    return embedder.encode(text)
```

**Batch processing:**
```python
def index_documents_batch(documents, batch_size=32):
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i+batch_size]
        
        # Batch embed
        embeddings = embedder.encode([d["text"] for d in batch])
        
        # Batch upsert
        points = [
            PointStruct(
                id=str(uuid.uuid4()),
                vector=emb.tolist(),
                payload=doc
            )
            for emb, doc in zip(embeddings, batch)
        ]
        
        qdrant_client.upsert(
            collection_name="docs",
            points=points
        )
```

### 8. Метрики качества

```python
def evaluate_retrieval(queries, relevant_docs):
    precisions = []
    recalls = []
    
    for query, relevant in zip(queries, relevant_docs):
        results = search(query, top_k=10)
        retrieved_ids = [r["id"] for r in results]
        
        # Precision@10
        relevant_count = sum(1 for id in retrieved_ids if id in relevant)
        precision = relevant_count / len(retrieved_ids)
        precisions.append(precision)
        
        # Recall
        recall = relevant_count / len(relevant)
        recalls.append(recall)
    
    return {
        "precision": np.mean(precisions),
        "recall": np.mean(recalls),
        "f1": 2 * (np.mean(precisions) * np.mean(recalls)) / 
              (np.mean(precisions) + np.mean(recalls))
    }
```

## Практическое задание

1. Реализовать semantic search с sentence-transformers
2. Добавить фильтрацию по метаданным
3. Протестировать гибридный поиск
4. Сравнить качество с/без ре-ранжирования
5. Измерить метрики (precision, recall)

## Тест

1. В чем разница между bi-encoder и cross-encoder?
2. Что такое гибридный поиск?
3. Зачем нужно ре-ранжирование?
4. Как работает query expansion?
5. Какие метрики используются для оценки retrieval?

