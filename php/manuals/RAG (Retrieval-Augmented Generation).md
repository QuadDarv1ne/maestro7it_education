# 🔍 Полный мануал по RAG (Retrieval-Augmented Generation): Архитектура, Реализация и Применение

## 📋 Содержание

1. [Введение в RAG](#введение-в-rag)
2. [Архитектура RAG систем](#архитектура-rag-систем)
3. [Векторные базы данных](#векторные-базы-данных)
4. [Эмбеддинги и кодирование текста](#эмбеддинги-и-кодирование-текста)
5. [Поиск и ретривал](#поиск-и-ретривал)
6. [Генерация ответов](#генерация-ответов)
7. [Практические примеры](#практические-примеры)
8. [Оптимизация и настройка](#оптимизация-и-настройка)
9. [Лучшие практики](#лучшие-практики)

## Введение в RAG

**RAG (Retrieval-Augmented Generation)** — это архитектура, сочетающая поиск релевантной информации из внешних источников с генерацией ответов с помощью языковых моделей.

Эта система позволяет `LLM` получать доступ к актуальным знаниям и специфическим данным, не включенным в их предварительное обучение.

**Основные преимущества RAG:**

- Доступ к актуальной информации
- Возможность работы с частными данными
- Снижение эффекта "галлюцинаций"
- Гибкость и расширяемость

## Архитектура RAG систем

### Базовая архитектура RAG:

```python
import torch
from transformers import RagTokenizer, RagRetriever, RagSequenceForGeneration

class RAGSystem:
    def __init__(self, model_name="facebook/rag-sequence-nq"):
        self.tokenizer = RagTokenizer.from_pretrained(model_name)
        self.retriever = RagRetriever.from_pretrained(
            model_name, 
            index_name="exact", 
            use_dummy_dataset=True
        )
        self.model = RagSequenceForGeneration.from_pretrained(
            model_name, 
            retriever=self.retriever
        )
    
    def generate_answer(self, question, context_docs=None):
        # Кодирование вопроса
        input_dict = self.tokenizer.prepare_seq2seq_batch(
            question, 
            return_tensors="pt"
        )
        
        # Генерация ответа
        with torch.no_grad():
            generated = self.model.generate(
                input_ids=input_dict["input_ids"],
                attention_mask=input_dict["attention_mask"],
                max_length=100
            )
        
        answer = self.tokenizer.batch_decode(
            generated, 
            skip_special_tokens=True
        )[0]
        
        return answer

# Использование
rag_system = RAGSystem()
answer = rag_system.generate_answer("Что такое машинное обучение?")
```

### Расширенная архитектура с пользовательскими данными:

```python
class CustomRAGSystem:
    def __init__(self, llm_model, embedding_model, vector_store):
        self.llm = llm_model
        self.embedding_model = embedding_model
        self.vector_store = vector_store
        self.prompt_template = """
        Используйте следующие фрагменты контекста, чтобы ответить на вопрос в конце.
        Если вы не знаете ответа, просто скажите, что не знаете, не пытайтесь придумать ответ.
        
        Контекст: {context}
        
        Вопрос: {question}
        
        Полезный ответ:
        """
    
    def retrieve_documents(self, query, k=5):
        """Поиск релевантных документов"""
        query_embedding = self.embedding_model.encode([query])
        results = self.vector_store.search(query_embedding[0], k=k)
        return [doc['text'] for doc in results]
    
    def generate_answer(self, question):
        """Генерация ответа с использованием ретривала"""
        # Поиск релевантных документов
        docs = self.retrieve_documents(question)
        context = "\n\n".join(docs)
        
        # Формирование промпта
        prompt = self.prompt_template.format(
            context=context,
            question=question
        )
        
        # Генерация ответа
        response = self.llm.generate(prompt, max_tokens=200)
        return response.strip()

# Компоненты системы
class VectorStore:
    def __init__(self):
        self.documents = []
        self.embeddings = []
    
    def add_document(self, text, embedding):
        self.documents.append({"text": text, "embedding": embedding})
        self.embeddings.append(embedding)
    
    def search(self, query_embedding, k=5):
        """Поиск по косинусному сходству"""
        similarities = []
        for i, doc_embedding in enumerate(self.embeddings):
            similarity = self.cosine_similarity(query_embedding, doc_embedding)
            similarities.append((similarity, i))
        
        # Сортировка по убыванию сходства
        similarities.sort(reverse=True)
        
        # Возвращение топ-k результатов
        results = []
        for similarity, idx in similarities[:k]:
            results.append({
                "text": self.documents[idx]["text"],
                "similarity": similarity
            })
        
        return results
    
    def cosine_similarity(self, a, b):
        """Вычисление косинусного сходства"""
        dot_product = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        return dot_product / (norm_a * norm_b)
```

## Векторные базы данных

### FAISS (Facebook AI Similarity Search):

```python
import faiss
import numpy as np

class FaissVectorStore:
    def __init__(self, dimension, index_type="Flat"):
        self.dimension = dimension
        self.index = self._create_index(index_type)
        self.documents = []
        
    def _create_index(self, index_type):
        if index_type == "Flat":
            return faiss.IndexFlatL2(self.dimension)
        elif index_type == "IVF":
            quantizer = faiss.IndexFlatL2(self.dimension)
            return faiss.IndexIVFFlat(quantizer, self.dimension, 100)
        elif index_type == "HNSW":
            return faiss.IndexHNSWFlat(self.dimension, 32)
    
    def add_documents(self, texts, embeddings):
        """Добавление документов в индекс"""
        self.documents.extend(texts)
        embeddings_array = np.array(embeddings).astype('float32')
        
        if isinstance(self.index, faiss.IndexIVFFlat):
            self.index.train(embeddings_array)
        
        self.index.add(embeddings_array)
    
    def search(self, query_embedding, k=5):
        """Поиск ближайших соседей"""
        query_vector = np.array([query_embedding]).astype('float32')
        distances, indices = self.index.search(query_vector, k)
        
        results = []
        for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
            if idx < len(self.documents):  # Проверка границ
                results.append({
                    "text": self.documents[idx],
                    "distance": distance,
                    "similarity": 1 / (1 + distance)  # Преобразование расстояния в сходство
                })
        
        return results

# Использование FAISS
dimension = 768  # Размерность эмбеддингов
vector_store = FaissVectorStore(dimension, index_type="IVF")

# Добавление документов
texts = ["Документ 1", "Документ 2", "Документ 3"]
embeddings = [[0.1, 0.2, ...], [0.3, 0.4, ...], [0.5, 0.6, ...]]  # Эмбеддинги
vector_store.add_documents(texts, embeddings)
```

### ChromaDB:

```python
import chromadb
from chromadb.config import Settings

class ChromaVectorStore:
    def __init__(self, persist_directory="./chroma_db"):
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=persist_directory
        ))
        self.collection = self.client.create_collection("documents")
    
    def add_documents(self, texts, metadatas=None, ids=None):
        """Добавление документов"""
        if ids is None:
            ids = [f"doc_{i}" for i in range(len(texts))]
        
        self.collection.add(
            documents=texts,
            metadatas=metadatas or [{} for _ in texts],
            ids=ids
        )
    
    def search(self, query_text, n_results=5):
        """Поиск документов"""
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        
        return [
            {
                "text": doc,
                "metadata": meta,
                "distance": dist
            }
            for doc, meta, dist in zip(
                results['documents'][0],
                results['metadatas'][0],
                results['distances'][0]
            )
        ]
    
    def delete_documents(self, ids):
        """Удаление документов"""
        self.collection.delete(ids=ids)

# Использование ChromaDB
chroma_store = ChromaVectorStore("./my_chroma_db")
chroma_store.add_documents(
    texts=["Первый документ", "Второй документ"],
    metadatas=[{"source": "book1"}, {"source": "book2"}]
)
```

### Pinecone:

```python
import pinecone

class PineconeVectorStore:
    def __init__(self, api_key, environment, index_name):
        pinecone.init(api_key=api_key, environment=environment)
        self.index_name = index_name
        
        # Создание индекса если он не существует
        if index_name not in pinecone.list_indexes():
            pinecone.create_index(
                name=index_name,
                dimension=768,
                metric="cosine"
            )
        
        self.index = pinecone.Index(index_name)
    
    def add_documents(self, vectors, metadata=None, ids=None):
        """Добавление документов"""
        if ids is None:
            ids = [f"vec_{i}" for i in range(len(vectors))]
        
        # Форматирование данных для Pinecone
        vectors_to_upsert = [
            (id_, vector, meta) 
            for id_, vector, meta in zip(ids, vectors, metadata or [{}] * len(vectors))
        ]
        
        self.index.upsert(vectors=vectors_to_upsert)
    
    def search(self, query_vector, top_k=5, filter_metadata=None):
        """Поиск похожих векторов"""
        query_response = self.index.query(
            vector=query_vector,
            top_k=top_k,
            include_metadata=True,
            filter=filter_metadata
        )
        
        results = []
        for match in query_response['matches']:
            results.append({
                "id": match['id'],
                "text": match['metadata'].get('text', ''),
                "score": match['score'],
                "metadata": match['metadata']
            })
        
        return results

# Использование Pinecone
pinecone_store = PineconeVectorStore(
    api_key="your-api-key",
    environment="us-west1-gcp",
    index_name="my-rag-index"
)
```

## Эмбеддинги и кодирование текста

### Sentence Transformers:

```python
from sentence_transformers import SentenceTransformer

class EmbeddingModel:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
    
    def encode(self, texts):
        """Кодирование текстов в векторы"""
        if isinstance(texts, str):
            texts = [texts]
        
        embeddings = self.model.encode(
            texts,
            convert_to_tensor=True,
            normalize_embeddings=True
        )
        
        return embeddings.cpu().numpy()
    
    def encode_batch(self, texts, batch_size=32):
        """Пакетное кодирование для больших объемов данных"""
        embeddings = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            batch_embeddings = self.encode(batch)
            embeddings.extend(batch_embeddings)
        return embeddings

# Использование
embedding_model = EmbeddingModel("all-MiniLM-L6-v2")
vectors = embedding_model.encode(["Пример текста для кодирования"])
```

### OpenAI Embeddings:

```python
import openai

class OpenAIEmbeddingModel:
    def __init__(self, api_key, model="text-embedding-ada-002"):
        openai.api_key = api_key
        self.model = model
    
    def encode(self, texts):
        """Кодирование текстов с помощью OpenAI"""
        if isinstance(texts, str):
            texts = [texts]
        
        response = openai.Embedding.create(
            input=texts,
            model=self.model
        )
        
        embeddings = [item['embedding'] for item in response['data']]
        return embeddings

# Использование
openai_model = OpenAIEmbeddingModel("your-api-key")
embeddings = openai_model.encode(["Текст для кодирования"])
```

### Предобработка текста:

```python
import re
from typing import List

class TextProcessor:
    def __init__(self):
        self.chunk_size = 500
        self.chunk_overlap = 100
    
    def clean_text(self, text: str) -> str:
        """Очистка текста"""
        # Удаление лишних пробелов
        text = re.sub(r'\s+', ' ', text)
        # Удаление специальных символов
        text = re.sub(r'[^\w\s.,!?;:()-]', '', text)
        return text.strip()
    
    def split_text(self, text: str) -> List[str]:
        """Разделение текста на чанки"""
        sentences = re.split(r'[.!?]+', text)
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            # Проверка размера чанка
            if len(current_chunk) + len(sentence) <= self.chunk_size:
                current_chunk += sentence + ". "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "
        
        # Добавление последнего чанка
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def process_document(self, text: str) -> List[str]:
        """Полная обработка документа"""
        cleaned_text = self.clean_text(text)
        chunks = self.split_text(cleaned_text)
        return chunks

# Использование
processor = TextProcessor()
chunks = processor.process_document(large_document_text)
```

## Поиск и ретривал

### Многоуровневый ретривал:

```python
class MultiStageRetriever:
    def __init__(self, vector_store, embedding_model, keyword_retriever=None):
        self.vector_store = vector_store
        self.embedding_model = embedding_model
        self.keyword_retriever = keyword_retriever
    
    def hybrid_search(self, query, k=10, alpha=0.7):
        """
        Гибридный поиск: комбинация векторного и ключевого поиска
        alpha: вес векторного поиска (0-1)
        """
        # Векторный поиск
        query_embedding = self.embedding_model.encode([query])[0]
        vector_results = self.vector_store.search(query_embedding, k=k*2)
        
        # Ключевой поиск (если доступен)
        if self.keyword_retriever:
            keyword_results = self.keyword_retriever.search(query, k=k*2)
        else:
            keyword_results = []
        
        # Объединение и переранжирование результатов
        combined_results = self._combine_results(
            vector_results, 
            keyword_results, 
            alpha
        )
        
        return combined_results[:k]
    
    def _combine_results(self, vector_results, keyword_results, alpha):
        """Комбинирование результатов с весами"""
        # Нормализация оценок
        vector_scores = [(result['text'], result['similarity']) 
                        for result in vector_results]
        keyword_scores = [(result['text'], result['score']) 
                         for result in keyword_results]
        
        # Создание словарей для быстрого доступа
        vector_dict = dict(vector_scores)
        keyword_dict = dict(keyword_scores)
        
        # Объединение всех уникальных текстов
        all_texts = set(vector_dict.keys()) | set(keyword_dict.keys())
        
        # Вычисление комбинированной оценки
        combined_scores = []
        for text in all_texts:
            vector_score = vector_dict.get(text, 0)
            keyword_score = keyword_dict.get(text, 0)
            
            # Комбинированная оценка
            combined_score = alpha * vector_score + (1 - alpha) * keyword_score
            combined_scores.append((text, combined_score))
        
        # Сортировка по убыванию
        combined_scores.sort(key=lambda x: x[1], reverse=True)
        
        return [{'text': text, 'score': score} for text, score in combined_scores]

# Использование
retriever = MultiStageRetriever(vector_store, embedding_model)
results = retriever.hybrid_search("Вопрос о машинном обучении", k=5)
```

### Реранжирование с помощью LLM:

```python
class LLMReranker:
    def __init__(self, llm_model):
        self.llm = llm_model
    
    def rerank(self, query, documents, k=5):
        """Переранжирование документов с помощью LLM"""
        reranked_docs = []
        
        for doc in documents:
            # Создание промпта для оценки релевантности
            prompt = f"""
            Оцените релевантность следующего документа для ответа на вопрос.
            Оцените по шкале от 1 до 10, где 10 - максимально релевантно.
            
            Вопрос: {query}
            
            Документ: {doc['text']}
            
            Ответьте только числом от 1 до 10:
            """
            
            # Получение оценки от LLM
            response = self.llm.generate(prompt, max_tokens=10)
            try:
                relevance_score = float(response.strip())
            except ValueError:
                relevance_score = 0.0
            
            doc['rerank_score'] = relevance_score
            reranked_docs.append(doc)
        
        # Сортировка по новой оценке
        reranked_docs.sort(key=lambda x: x['rerank_score'], reverse=True)
        
        return reranked_docs[:k]

# Использование
reranker = LLMReranker(llm_model)
final_results = reranker.rerank(query, retrieved_docs, k=5)
```

## Генерация ответов

### Prompt Engineering для RAG:

```python
class RAGPromptBuilder:
    def __init__(self):
        self.templates = {
            'qa': """
            Используйте следующие фрагменты контекста, чтобы ответить на вопрос.
            Если ответа нет в контексте, скажите "Я не могу найти ответ на этот вопрос в предоставленных материалах".
            
            Контекст:
            {context}
            
            Вопрос: {question}
            
            Ответ:
            """,
            
            'summarization': """
            Создайте краткое резюме следующих документов:
            
            Документы:
            {context}
            
            Резюме:
            """,
            
            'comparison': """
            Сравните информацию из следующих документов:
            
            Документы:
            {context}
            
            Сравнение:
            """
        }
    
    def build_prompt(self, template_name, context, question=None):
        """Создание промпта по шаблону"""
        if template_name not in self.templates:
            raise ValueError(f"Unknown template: {template_name}")
        
        template = self.templates[template_name]
        
        if template_name == 'qa':
            return template.format(context=context, question=question)
        else:
            return template.format(context=context)

# Использование
prompt_builder = RAGPromptBuilder()
qa_prompt = prompt_builder.build_prompt(
    'qa', 
    context='\n\n'.join([doc['text'] for doc in relevant_docs]),
    question=user_question
)
```

### Генерация с цитированием источников:

```python
class CitationAwareGenerator:
    def __init__(self, llm_model):
        self.llm = llm_model
    
    def generate_with_citations(self, question, documents):
        """Генерация ответа с цитированием источников"""
        # Формирование контекста с номерами источников
        context_parts = []
        for i, doc in enumerate(documents, 1):
            context_parts.append(f"[{i}] {doc['text']}")
        
        context = '\n\n'.join(context_parts)
        
        prompt = f"""
        Используйте следующие документы для ответа на вопрос. 
        Цитируйте источники в квадратных скобках [1], [2], и т.д.
        Если информация берется из нескольких источников, укажите все соответствующие номера.
        
        Документы:
        {context}
        
        Вопрос: {question}
        
        Ответ с цитированием:
        """
        
        response = self.llm.generate(prompt, max_tokens=300)
        
        # Извлечение цитирований
        citations = self._extract_citations(response, documents)
        
        return {
            'answer': response,
            'citations': citations
        }
    
    def _extract_citations(self, response, documents):
        """Извлечение и форматирование цитирований"""
        import re
        
        # Поиск ссылок в квадратных скобках
        citation_pattern = r'\[(\d+(?:,\s*\d+)*)\]'
        matches = re.findall(citation_pattern, response)
        
        citations = []
        for match in matches:
            # Разбор номеров источников
            source_numbers = [int(x.strip()) for x in match.split(',')]
            
            for num in source_numbers:
                if 1 <= num <= len(documents):
                    citations.append({
                        'source_number': num,
                        'text': documents[num-1]['text'][:200] + "...",
                        'metadata': documents[num-1].get('metadata', {})
                    })
        
        return citations

# Использование
generator = CitationAwareGenerator(llm_model)
result = generator.generate_with_citations(question, retrieved_docs)
print(f"Ответ: {result['answer']}")
print("Цитирования:")
for citation in result['citations']:
    print(f"[{citation['source_number']}] {citation['text']}")
```

## Практические примеры

### Пример №1: Чат-бот с RAG для документации

```python
class DocumentationChatbot:
    def __init__(self, docs_path, llm_model, embedding_model):
        self.vector_store = self._build_vector_store(docs_path, embedding_model)
        self.llm = llm_model
        self.embedding_model = embedding_model
    
    def _build_vector_store(self, docs_path, embedding_model):
        """Создание векторного хранилища из документов"""
        vector_store = FaissVectorStore(dimension=embedding_model.dimension)
        
        # Загрузка и обработка документов
        for filename in os.listdir(docs_path):
            if filename.endswith('.txt'):
                with open(os.path.join(docs_path, filename), 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Разделение на чанки
                chunks = self._split_text(content)
                
                # Создание эмбеддингов
                embeddings = embedding_model.encode(chunks)
                
                # Добавление в векторное хранилище
                vector_store.add_documents(chunks, embeddings)
        
        return vector_store
    
    def _split_text(self, text, chunk_size=500):
        """Разделение текста на чанки"""
        sentences = text.split('.')
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) < chunk_size:
                current_chunk += sentence + "."
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + "."
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def chat(self, question):
        """Обработка вопроса пользователя"""
        # Поиск релевантных документов
        query_embedding = self.embedding_model.encode([question])[0]
        docs = self.vector_store.search(query_embedding, k=3)
        
        # Формирование контекста
        context = '\n\n'.join([doc['text'] for doc in docs])
        
        # Генерация ответа
        prompt = f"""
        Используйте следующую документацию для ответа на вопрос:
        
        Документация:
        {context}
        
        Вопрос: {question}
        
        Ответ:
        """
        
        response = self.llm.generate(prompt, max_tokens=200)
        return response.strip()

# Использование
chatbot = DocumentationChatbot('./docs', llm_model, embedding_model)
answer = chatbot.chat("Как установить этот пакет?")
```

### Пример №2: Система вопросов-ответов для исследований

```python
class ResearchQA:
    def __init__(self, papers_directory):
        self.vector_store = ChromaVectorStore("./research_papers")
        self.embedding_model = EmbeddingModel("all-MiniLM-L6-v2")
        self.llm = self._load_llm()
        self._index_papers(papers_directory)
    
    def _load_llm(self):
        """Загрузка языковой модели"""
        from transformers import AutoModelForCausalLM, AutoTokenizer
        model = AutoModelForCausalLM.from_pretrained("gpt2")
        tokenizer = AutoTokenizer.from_pretrained("gpt2")
        return {"model": model, "tokenizer": tokenizer}
    
    def _index_papers(self, papers_dir):
        """Индексация научных статей"""
        import json
        
        for filename in os.listdir(papers_dir):
            if filename.endswith('.json'):
                with open(os.path.join(papers_dir, filename), 'r') as f:
                    paper = json.load(f)
                
                # Извлечение секций статьи
                sections = [
                    f"Заголовок: {paper.get('title', '')}",
                    f"Аннотация: {paper.get('abstract', '')}",
                    f"Введение: {paper.get('introduction', '')}",
                    f"Методы: {paper.get('methods', '')}",
                    f"Результаты: {paper.get('results', '')}",
                    f"Заключение: {paper.get('conclusion', '')}"
                ]
                
                # Создание эмбеддингов для каждой секции
                for i, section in enumerate(sections):
                    if section.split(': ', 1)[1].strip():  # Проверка на пустоту
                        embedding = self.embedding_model.encode([section])[0]
                        self.vector_store.add_documents(
                            [section],
                            [{"paper_id": paper.get('id'), "section": i}],
                            [f"{paper.get('id')}_{i}"]
                        )
    
    def answer_question(self, question, paper_filter=None):
        """Ответ на исследовательский вопрос"""
        # Поиск релевантных секций
        query_embedding = self.embedding_model.encode([question])[0]
        
        # Фильтрация по статьям если указано
        filter_dict = {"paper_id": paper_filter} if paper_filter else None
        relevant_sections = self.vector_store.search(
            question, 
            n_results=10,
            filter_metadata=filter_dict
        )
        
        # Формирование контекста
        context = '\n\n'.join([sec['text'] for sec in relevant_sections])
        
        # Генерация ответа
        prompt = f"""
        На основе следующих научных материалов ответьте на вопрос.
        Цитируйте источники в формате [номер_статьи].
        
        Материалы:
        {context}
        
        Вопрос: {question}
        
        Ответ:
        """
        
        # Генерация с помощью LLM
        response = self._generate_with_llm(prompt)
        return self._format_response(response, relevant_sections)
    
    def _generate_with_llm(self, prompt):
        """Генерация текста с помощью LLM"""
        tokenizer = self.llm["tokenizer"]
        model = self.llm["model"]
        
        inputs = tokenizer.encode(prompt, return_tensors="pt")
        with torch.no_grad():
            outputs = model.generate(
                inputs,
                max_length=inputs.shape[1] + 200,
                temperature=0.7,
                pad_token_id=tokenizer.eos_token_id
            )
        
        return tokenizer.decode(outputs[0], skip_special_tokens=True)[len(prompt):]
    
    def _format_response(self, response, sections):
        """Форматирование ответа с цитированием"""
        # Извлечение цитирований и форматирование
        return {
            "answer": response,
            "sources": [
                {
                    "paper_id": sec['metadata']['paper_id'],
                    "section": sec['metadata']['section'],
                    "text": sec['text'][:100] + "..."
                } for sec in sections
            ]
        }

# Использование
research_qa = ResearchQA("./papers")
result = research_qa.answer_question(
    "Каковы последние достижения в области трансформеров?",
    paper_filter="transformer_survey_2023"
)
```

## Оптимизация и настройка

### Оптимизация поиска:

```python
class OptimizedRetriever:
    def __init__(self, vector_store, embedding_model):
        self.vector_store = vector_store
        self.embedding_model = embedding_model
        self.cache = {}  # Кэш для частых запросов
    
    def optimized_search(self, query, k=5, use_cache=True):
        """Оптимизированный поиск с кэшированием"""
        # Проверка кэша
        if use_cache and query in self.cache:
            return self.cache[query]
        
        # Предобработка запроса
        processed_query = self._preprocess_query(query)
        
        # Создание эмбеддинга
        query_embedding = self.embedding_model.encode([processed_query])[0]
        
        # Поиск с оптимизированными параметрами
        results = self.vector_store.search(
            query_embedding, 
            k=k,
            search_params={"ef_search": 100}  # Для HNSW индексов
        )
        
        # Постобработка результатов
        filtered_results = self._filter_results(results)
        
        # Сохранение в кэш
        if use_cache:
            self.cache[query] = filtered_results
        
        return filtered_results
    
    def _preprocess_query(self, query):
        """Предобработка запроса пользователя"""
        # Удаление стоп-слов, нормализация и т.д.
        import re
        query = re.sub(r'[^\w\s]', '', query.lower())
        return ' '.join(query.split())  # Нормализация пробелов
    
    def _filter_results(self, results):
        """Фильтрация результатов по качеству"""
        # Удаление дубликатов
        seen_texts = set()
        filtered = []
        
        for result in results:
            text = result['text'].strip()
            if text and text not in seen_texts:
                seen_texts.add(text)
                filtered.append(result)
        
        return filtered

# Использование
optimized_retriever = OptimizedRetriever(vector_store, embedding_model)
results = optimized_retriever.optimized_search("сложный технический вопрос")
```

### Адаптивная настройка параметров:

```python
class AdaptiveRAG:
    def __init__(self, base_retriever, llm):
        self.base_retriever = base_retriever
        self.llm = llm
        self.performance_history = []
    
    def adaptive_search(self, query, target_recall=0.8):
        """Адаптивный поиск с настройкой параметров"""
        k_values = [3, 5, 10, 15, 20]
        best_k = 5
        best_score = 0
        
        # Поиск оптимального k
        for k in k_values:
            results = self.base_retriever.search(query, k=k)
            score = self._evaluate_results(query, results)
            
            if score > best_score:
                best_score = score
                best_k = k
            
            # Ранний выход если достигнута цель
            if score >= target_recall:
                break
        
        # Использование оптимального k
        final_results = self.base_retriever.search(query, k=best_k)
        return final_results, best_k
    
    def _evaluate_results(self, query, results):
        """Оценка качества результатов"""
        # Использование LLM для оценки релевантности
        context = '\n\n'.join([r['text'] for r in results[:3]])
        
        prompt = f"""
        Оцените релевантность следующих документов для ответа на вопрос.
        Оцените по шкале от 0 до 1, где 1 - максимально релевантно.
        
        Вопрос: {query}
        
        Документы:
        {context}
        
        Ответьте только числом от 0 до 1:
        """
        
        response = self.llm.generate(prompt, max_tokens=10)
        try:
            return float(response.strip())
        except ValueError:
            return 0.0
    
    def update_performance_history(self, query, actual_k, user_feedback):
        """Обновление истории производительности"""
        self.performance_history.append({
            'query': query,
            'k_used': actual_k,
            'feedback': user_feedback,
            'timestamp': datetime.now()
        })

# Использование
adaptive_rag = AdaptiveRAG(base_retriever, llm)
results, optimal_k = adaptive_rag.adaptive_search("технический вопрос")
```

## Лучшие практики

### 1. Управление качеством данных:

```python
class DataQualityManager:
    def __init__(self):
        self.quality_threshold = 0.7
    
    def assess_document_quality(self, text):
        """Оценка качества документа"""
        metrics = {
            'length_score': self._length_score(text),
            'coherence_score': self._coherence_score(text),
            'diversity_score': self._diversity_score(text)
        }
        
        overall_score = sum(metrics.values()) / len(metrics)
        return overall_score, metrics
    
    def _length_score(self, text):
        """Оценка по длине текста"""
        word_count = len(text.split())
        if word_count < 50:
            return 0.3
        elif word_count < 200:
            return 0.7
        elif word_count < 1000:
            return 1.0
        else:
            return 0.8  # Слишком длинные тексты могут быть менее полезны
    
    def _coherence_score(self, text):
        """Оценка связности текста"""
        # Простая оценка на основе плотности уникальных слов
        words = text.lower().split()
        if len(words) == 0:
            return 0
        
        unique_ratio = len(set(words)) / len(words)
        return 1 - abs(unique_ratio - 0.5)  # Оптимально около 0.5
    
    def _diversity_score(self, text):
        """Оценка разнообразия содержания"""
        # Оценка на основе разнообразия частей речи
        import nltk
        try:
            tokens = nltk.word_tokenize(text)
            pos_tags = nltk.pos_tag(tokens)
            tag_types = set([tag for word, tag in pos_tags])
            return min(len(tag_types) / 10, 1.0)  # Нормализация
        except:
            return 0.5  # Значение по умолчанию

# Использование
quality_manager = DataQualityManager()
score, metrics = quality_manager.assess_document_quality(document_text)
if score >= quality_manager.quality_threshold:
    # Добавить документ в индекс
    pass
```

### 2. Мониторинг производительности:

```python
class RAGMonitor:
    def __init__(self):
        self.metrics = {
            'query_count': 0,
            'avg_response_time': 0,
            'retrieval_accuracy': 0,
            'generation_quality': 0
        }
        self.query_log = []
    
    def log_query(self, query, response_time, retrieval_results, final_answer):
        """Логирование запроса и метрик"""
        self.metrics['query_count'] += 1
        
        # Обновление среднего времени ответа
        old_avg = self.metrics['avg_response_time']
        new_avg = (old_avg * (self.metrics['query_count'] - 1) + response_time) / self.metrics['query_count']
        self.metrics['avg_response_time'] = new_avg
        
        # Логирование деталей
        self.query_log.append({
            'query': query,
            'response_time': response_time,
            'retrieved_docs_count': len(retrieval_results),
            'answer_length': len(final_answer),
            'timestamp': datetime.now()
        })
    
    def calculate_metrics(self, ground_truth_data):
        """Расчет метрик качества"""
        if not ground_truth_data:
            return
        
        retrieval_correct = 0
        total_queries = len(ground_truth_data)
        
        for query_data in ground_truth_data:
            query = query_data['query']
            expected_docs = set(query_data['relevant_docs'])
            
            # Получение фактических результатов
            actual_results = self._get_actual_results(query)
            actual_docs = set([r['id'] for r in actual_results])
            
            # Расчет точности ретривала
            if expected_docs & actual_docs:  # Есть пересечение
                retrieval_correct += 1
        
        self.metrics['retrieval_accuracy'] = retrieval_correct / total_queries
    
    def generate_report(self):
        """Генерация отчета о производительности"""
        report = f"""
        RAG System Performance Report
        ============================
        
        Total Queries: {self.metrics['query_count']}
        Average Response Time: {self.metrics['avg_response_time']:.2f}s
        Retrieval Accuracy: {self.metrics['retrieval_accuracy']:.2%}
        Generation Quality Score: {self.metrics['generation_quality']:.2f}/1.0
        
        Recent Performance Trends:
        """
        
        # Анализ последних запросов
        recent_queries = self.query_log[-10:]  # Последние 10 запросов
        avg_recent_time = sum(q['response_time'] for q in recent_queries) / len(recent_queries)
        
        report += f"Average time for recent queries: {avg_recent_time:.2f}s\n"
        
        return report

# Использование
monitor = RAGMonitor()
# Во время обработки запросов
monitor.log_query(query, response_time, retrieved_docs, final_answer)
# Периодически
performance_report = monitor.generate_report()
```

### 3. Обработка ошибок и отказоустойчивость:

```python
class RobustRAG:
    def __init__(self, retriever, generator, fallback_responses=None):
        self.retriever = retriever
        self.generator = generator
        self.fallback_responses = fallback_responses or self._default_fallbacks()
        self.error_count = 0
        self.max_errors = 5
    
    def _default_fallbacks(self):
        return {
            'no_results': "Извините, я не смог найти релевантную информацию по вашему запросу.",
            'generation_failed': "Извините, возникла техническая проблема при генерации ответа.",
            'retrieval_failed': "Извините, система поиска временно недоступна."
        }
    
    def robust_query(self, question):
        """Отказоустойчивая обработка запросов"""
        try:
            # Этап 1: Поиск документов
            try:
                docs = self.retriever.search(question, k=5)
                if not docs:
                    return self.fallback_responses['no_results']
            except Exception as e:
                self._handle_error("retrieval", e)
                return self.fallback_responses['retrieval_failed']
            
            # Этап 2: Генерация ответа
            try:
                answer = self.generator.generate(question, docs)
                if not answer or len(answer.strip()) < 5:
                    return self.fallback_responses['generation_failed']
            except Exception as e:
                self._handle_error("generation", e)
                return self.fallback_responses['generation_failed']
            
            return answer
            
        except Exception as e:
            self._handle_error("general", e)
            return "Извините, произошла непредвиденная ошибка. Пожалуйста, попробуйте позже."
    
    def _handle_error(self, error_type, exception):
        """Обработка ошибок"""
        self.error_count += 1
        print(f"Error in {error_type}: {str(exception)}")
        
        # Реакция на превышение лимита ошибок
        if self.error_count >= self.max_errors:
            self._trigger_failover()
    
    def _trigger_failover(self):
        """Активация резервной системы"""
        print("Triggering failover mechanism...")
        # Здесь может быть логика переключения на резервную систему
        self.error_count = 0  # Сброс счетчика после failover

# Использование
robust_rag = RobustRAG(retriever, generator)
answer = robust_rag.robust_query("сложный вопрос")
```

---

#### 💼 Автор: Дуплей Максим Игоревич

### 📲 Контакты:

- **Telegram №1:** [@quadd4rv1n7](https://t.me/quadd4rv1n7)
- **Telegram №2:** [@dupley_maxim_1999](https://t.me/dupley_maxim_1999)

📅 **Дата:** 26.01.2026

▶️ Версия 1.0

---
> 📧 **Предложения по сотрудничеству:** maksimqwe42@mail.ru

---

### 💼 Профиль на Profi.ru
[![Profi.ru Profile](https://img.shields.io/badge/Profi.ru-Дуплей%20М.И.-FF6B35?style=for-the-badge)](https://profi.ru/profile/DupleyMI)

> Консультации и услуги программирования на платформе Profi.ru

---

### 📚 Услуги обучения
[![Обучение технологиям и языкам программирования на Kwork](https://img.shields.io/badge/Kwork-Обучение%20Программированию-blue?style=for-the-badge&logo=kwork)](https://kwork.ru/usability-testing/42465951/обучение-технологиям-и-языкам-программирования)

> Профессиональное обучение технологиям и языкам программирования. Персональные консультации и курсы от опытного преподавателя.

---

### 🏫 О школе
[![Website](https://img.shields.io/badge/Maestro7IT-school--maestro7it.ru-darkgreen?style=for-the-badge)](https://school-maestro7it.ru/)

> Инновационная школа программирования, специализирующаяся на подготовке специалистов в области современных технологий и языков программирования.