# Полный мануал по большим языковым моделям (LLM): Архитектура, Реализация и Применение

## 📋 Содержание

1. [Введение в большие языковые модели](#введение-в-большие-языковые-модели)
2. [Архитектуры LLM](#архитектуры-llm)
3. [Трансформеры и механизмы внимания](#трансформеры-и-механизмы-внимания)
4. [Предварительное обучение](#предварительное-обучение)
5. [Тонкая настройка (Fine-tuning)](#тонкая-настройка-fine-tuning)
6. [Извлечение параметров (LoRA и PEFT)](#извлечение-параметров-lora-и-peft)
7. [Инференс и оптимизация](#инференс-и-оптимизация)
8. [Практические примеры](#практические-примеры)
9. [Лучшие практики](#лучшие-практики)

## Введение в большие языковые модели

**Большие языковые модели (Large Language Models, LLM)** — это нейронные сети с огромным количеством параметров (миллиарды и триллионы), обученные на массивных корпусах текста для понимания и генерации естественного языка.

**Основные характеристики LLM:**

- Масштабируемость параметров
- `Few-shot` и `zero-shot` обучение
- Многоязычность
- Многофункциональность (текст, код, рассуждения)

## Архитектуры LLM

### Основные архитектуры:

#### 1. GPT (Generative Pre-trained Transformer)

```python
# Пример архитектуры GPT-like модели
import torch
import torch.nn as nn
from transformers import GPT2LMHeadModel, GPT2Tokenizer

class CustomGPT(nn.Module):
    def __init__(self, vocab_size, d_model=768, n_heads=12, n_layers=12):
        super().__init__()
        self.token_embedding = nn.Embedding(vocab_size, d_model)
        self.position_embedding = nn.Embedding(1024, d_model)
        self.layers = nn.ModuleList([
            nn.TransformerDecoderLayer(
                d_model=d_model,
                nhead=n_heads,
                dim_feedforward=d_model * 4,
                batch_first=True
            ) for _ in range(n_layers)
        ])
        self.lm_head = nn.Linear(d_model, vocab_size)
        
    def forward(self, input_ids, attention_mask=None):
        seq_len = input_ids.size(1)
        positions = torch.arange(seq_len, device=input_ids.device).unsqueeze(0)
        
        x = self.token_embedding(input_ids) + self.position_embedding(positions)
        
        for layer in self.layers:
            x = layer(x, x, tgt_mask=self.generate_causal_mask(seq_len))
            
        return self.lm_head(x)
    
    def generate_causal_mask(self, size):
        mask = torch.triu(torch.ones(size, size), diagonal=1).bool()
        return mask
```

#### 2. BERT (Bidirectional Encoder Representations)

```python
# Пример BERT-подобной архитектуры
class BERTModel(nn.Module):
    def __init__(self, vocab_size, d_model=768, n_heads=12, n_layers=12):
        super().__init__()
        self.token_embedding = nn.Embedding(vocab_size, d_model)
        self.segment_embedding = nn.Embedding(2, d_model)
        self.position_embedding = nn.Embedding(512, d_model)
        
        self.encoder_layers = nn.ModuleList([
            nn.TransformerEncoderLayer(
                d_model=d_model,
                nhead=n_heads,
                dim_feedforward=d_model * 4,
                batch_first=True
            ) for _ in range(n_layers)
        ])
        
        self.pooler = nn.Linear(d_model, d_model)
        self.activation = nn.Tanh()
        
    def forward(self, input_ids, token_type_ids=None, attention_mask=None):
        seq_len = input_ids.size(1)
        positions = torch.arange(seq_len, device=input_ids.device).unsqueeze(0)
        
        embeddings = self.token_embedding(input_ids) + self.position_embedding(positions)
        
        if token_type_ids is not None:
            embeddings += self.segment_embedding(token_type_ids)
            
        # Применение маски внимания
        if attention_mask is not None:
            attention_mask = attention_mask.unsqueeze(1).unsqueeze(2)
            attention_mask = (1.0 - attention_mask) * -10000.0
            
        for layer in self.encoder_layers:
            embeddings = layer(embeddings, src_key_padding_mask=attention_mask)
            
        # Pooler для получения представления [CLS] токена
        pooled_output = self.activation(self.pooler(embeddings[:, 0]))
        
        return embeddings, pooled_output
```

#### 3. T5 (Text-to-Text Transfer Transformer)

```python
# Пример T5-подобной архитектуры
class T5Model(nn.Module):
    def __init__(self, vocab_size, d_model=512, n_heads=8, n_layers=6):
        super().__init__()
        self.shared_embedding = nn.Embedding(vocab_size, d_model)
        
        # Encoder
        self.encoder_layers = nn.ModuleList([
            T5EncoderLayer(d_model, n_heads) for _ in range(n_layers)
        ])
        
        # Decoder
        self.decoder_layers = nn.ModuleList([
            T5DecoderLayer(d_model, n_heads) for _ in range(n_layers)
        ])
        
        self.lm_head = nn.Linear(d_model, vocab_size, bias=False)
        
    def forward(self, input_ids, decoder_input_ids, attention_mask=None):
        # Encoder
        encoder_hidden_states = self.shared_embedding(input_ids)
        for layer in self.encoder_layers:
            encoder_hidden_states = layer(encoder_hidden_states, attention_mask)
            
        # Decoder
        decoder_hidden_states = self.shared_embedding(decoder_input_ids)
        for layer in self.decoder_layers:
            decoder_hidden_states = layer(
                decoder_hidden_states, 
                encoder_hidden_states,
                attention_mask
            )
            
        return self.lm_head(decoder_hidden_states)
```

## Трансформеры и механизмы внимания

### Self-Attention механизм:

```python
class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, n_heads):
        super().__init__()
        self.d_model = d_model
        self.n_heads = n_heads
        self.d_k = d_model // n_heads
        
        self.q_linear = nn.Linear(d_model, d_model)
        self.k_linear = nn.Linear(d_model, d_model)
        self.v_linear = nn.Linear(d_model, d_model)
        self.out = nn.Linear(d_model, d_model)
        
    def forward(self, query, key, value, mask=None):
        batch_size = query.size(0)
        
        # Линейные преобразования и разделение на головы
        Q = self.q_linear(query).view(batch_size, -1, self.n_heads, self.d_k).transpose(1, 2)
        K = self.k_linear(key).view(batch_size, -1, self.n_heads, self.d_k).transpose(1, 2)
        V = self.v_linear(value).view(batch_size, -1, self.n_heads, self.d_k).transpose(1, 2)
        
        # Вычисление внимания
        scores = torch.matmul(Q, K.transpose(-2, -1)) / torch.sqrt(torch.tensor(self.d_k, dtype=torch.float32))
        
        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)
            
        attention = torch.softmax(scores, dim=-1)
        context = torch.matmul(attention, V)
        
        # Конкатенация голов и линейное преобразование
        context = context.transpose(1, 2).contiguous().view(batch_size, -1, self.d_model)
        output = self.out(context)
        
        return output, attention
```

### Position-wise Feed-Forward Network:

```python
class PositionwiseFeedForward(nn.Module):
    def __init__(self, d_model, d_ff, dropout=0.1):
        super().__init__()
        self.w_1 = nn.Linear(d_model, d_ff)
        self.w_2 = nn.Linear(d_ff, d_model)
        self.dropout = nn.Dropout(dropout)
        self.activation = nn.GELU()
        
    def forward(self, x):
        return self.w_2(self.dropout(self.activation(self.w_1(x))))
```

## Предварительное обучение

### Маскированное языковое моделирование (MLM):

```python
def mlm_pretraining(model, tokenizer, texts, mlm_probability=0.15):
    """
    Предварительное обучение с маскированным языковым моделированием
    """
    model.train()
    total_loss = 0
    
    for batch in texts:
        # Токенизация
        inputs = tokenizer(batch, return_tensors='pt', padding=True, truncation=True)
        input_ids = inputs['input_ids']
        
        # Создание масок
        labels = input_ids.clone()
        probability_matrix = torch.full(labels.shape, mlm_probability)
        
        # Маскирование токенов
        masked_indices = torch.bernoulli(probability_matrix).bool()
        labels[~masked_indices] = -100  # Игнорировать при вычислении потерь
        
        # Замена маскированных токенов
        indices_replaced = torch.bernoulli(torch.full(labels.shape, 0.8)).bool() & masked_indices
        input_ids[indices_replaced] = tokenizer.mask_token_id
        
        # Замена случайными токенами
        indices_random = torch.bernoulli(torch.full(labels.shape, 0.5)).bool() & masked_indices & ~indices_replaced
        random_words = torch.randint(len(tokenizer), labels.shape, dtype=torch.long)
        input_ids[indices_random] = random_words[indices_random]
        
        # Forward pass
        outputs = model(input_ids, labels=labels)
        loss = outputs.loss
        total_loss += loss.item()
        
        # Backward pass
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        
    return total_loss / len(texts)
```

### Предсказание следующего токена (Causal LM):

```python
def causal_lm_training(model, tokenizer, texts):
    """
    Обучение с предсказанием следующего токена
    """
    model.train()
    total_loss = 0
    
    for batch in texts:
        inputs = tokenizer(batch, return_tensors='pt', padding=True, truncation=True)
        input_ids = inputs['input_ids']
        
        # Сдвиг для создания целевых меток
        labels = input_ids.clone()
        labels[:, :-1] = input_ids[:, 1:]
        labels[:, -1] = -100  # Игнорировать последний токен
        
        outputs = model(input_ids, labels=labels)
        loss = outputs.loss
        total_loss += loss.item()
        
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        
    return total_loss / len(texts)
```

## Тонкая настройка (Fine-tuning)

### Полная тонкая настройка:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer

# Загрузка предобученной модели
model_name = "gpt2"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Подготовка данных
def prepare_dataset(examples):
    texts = examples['text']
    encodings = tokenizer(texts, truncation=True, padding=True, max_length=512)
    return encodings

# Создание датасета
train_dataset = dataset.map(prepare_dataset, batched=True)

# Настройка обучения
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    warmup_steps=100,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,
    save_steps=1000,
    evaluation_strategy="steps",
    eval_steps=1000,
    fp16=True,  # Для ускорения на GPU
)

# Создание тренера
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    tokenizer=tokenizer,
)

# Запуск обучения
trainer.train()
```

### Инструкт-тюнинг:

```python
def format_instruction_prompt(instruction, input_text="", output=""):
    """Форматирование промпта для инструкт-тюнинга"""
    if input_text:
        prompt = f"### Instruction:\n{instruction}\n\n### Input:\n{input_text}\n\n### Response:\n"
    else:
        prompt = f"### Instruction:\n{instruction}\n\n### Response:\n"
    
    if output:
        prompt += f"{output}"
    
    return prompt

# Пример создания датасета для инструкт-тюнинга
instruction_data = [
    {
        "instruction": "Переведи текст с английского на русский",
        "input": "Hello, how are you?",
        "output": "Привет, как дела?"
    },
    {
        "instruction": "Обобщи текст",
        "input": "Машинное обучение - это область искусственного интеллекта...",
        "output": "Машинное обучение позволяет компьютерам учиться без явного программирования."
    }
]

# Форматирование данных
formatted_prompts = [
    format_instruction_prompt(**item) for item in instruction_data
]
```

## Извлечение параметров (LoRA и PEFT)

### LoRA (Low-Rank Adaptation):

```python
from peft import LoraConfig, get_peft_model, TaskType

# Настройка LoRA
lora_config = LoraConfig(
    r=8,  # ранг матриц
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],  # какие веса адаптировать
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)

# Применение LoRA к модели
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()  # Показать количество обучаемых параметров

# Обучение с LoRA
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    tokenizer=tokenizer,
)

trainer.train()
```

### QLoRA (Quantized LoRA):

```python
from peft import prepare_model_for_kbit_training

# Подготовка модели для 4-битного обучения
model = prepare_model_for_kbit_training(model)

# Настройка QLoRA
lora_config = LoraConfig(
    r=64,
    lora_alpha=16,
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
    lora_dropout=0.1,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)

model = get_peft_model(model, lora_config)
```

### Адаптеры (Adapter Tuning):

```python
class AdapterLayer(nn.Module):
    def __init__(self, d_model, bottleneck_size=64):
        super().__init__()
        self.down_proj = nn.Linear(d_model, bottleneck_size)
        self.up_proj = nn.Linear(bottleneck_size, d_model)
        self.activation = nn.ReLU()
        self.layer_norm = nn.LayerNorm(d_model)
        
    def forward(self, x):
        residual = x
        x = self.layer_norm(x)
        x = self.down_proj(x)
        x = self.activation(x)
        x = self.up_proj(x)
        return x + residual

# Добавление адаптеров к трансформерным слоям
def add_adapters_to_model(model, bottleneck_size=64):
    for layer in model.transformer.h:
        # Добавляем адаптеры после каждого attention и FFN слоя
        layer.attn_adapter = AdapterLayer(model.config.n_embd, bottleneck_size)
        layer.mlp_adapter = AdapterLayer(model.config.n_embd, bottleneck_size)
    return model
```

## Инференс и оптимизация

### Генерация текста:

```python
def generate_text(model, tokenizer, prompt, max_length=100, temperature=0.7, top_p=0.9):
    """Генерация текста с различными стратегиями"""
    model.eval()
    
    inputs = tokenizer.encode(prompt, return_tensors='pt')
    
    with torch.no_grad():
        outputs = model.generate(
            inputs,
            max_length=max_length,
            temperature=temperature,
            do_sample=True,
            top_p=top_p,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )
    
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated_text

# Пример использования
prompt = "В науке машинного обучения"
generated = generate_text(model, tokenizer, prompt, max_length=200)
print(generated)
```

### Beam Search генерация:

```python
def beam_search_generation(model, tokenizer, prompt, max_length=100, num_beams=5):
    """Генерация с beam search"""
    model.eval()
    
    inputs = tokenizer.encode(prompt, return_tensors='pt')
    
    with torch.no_grad():
        outputs = model.generate(
            inputs,
            max_length=max_length,
            num_beams=num_beams,
            early_stopping=True,
            pad_token_id=tokenizer.eos_token_id,
        )
    
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
```

### Оптимизация для инференса:

```python
# Квантование модели
from torch.quantization import quantize_dynamic

quantized_model = quantize_dynamic(
    model, {nn.Linear}, dtype=torch.qint8
)

# Использование ONNX для оптимизации
import torch.onnx

dummy_input = torch.randint(0, 1000, (1, 512))
torch.onnx.export(
    model,
    dummy_input,
    "model.onnx",
    export_params=True,
    opset_version=11,
    do_constant_folding=True,
    input_names=['input'],
    output_names=['output'],
    dynamic_axes={
        'input': {0: 'batch_size', 1: 'sequence'},
        'output': {0: 'batch_size', 1: 'sequence'}
    }
)

# Использование TensorRT (для NVIDIA GPU)
# Требует установки tensorrt и onnxruntime-gpu
```

## Практические примеры

### Пример №1: Чат-бот с использованием LLM

```python
class ChatBot:
    def __init__(self, model_name="gpt2"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.chat_history = []
        
    def get_response(self, user_message, max_length=150):
        # Добавление сообщения в историю
        self.chat_history.append(f"User: {user_message}")
        
        # Формирование контекста
        context = "\n".join(self.chat_history[-5:])  # Последние 5 сообщений
        prompt = f"{context}\nAI:"
        
        # Генерация ответа
        inputs = self.tokenizer.encode(prompt, return_tensors='pt')
        
        with torch.no_grad():
            outputs = self.model.generate(
                inputs,
                max_length=len(inputs[0]) + max_length,
                temperature=0.7,
                pad_token_id=self.tokenizer.eos_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
            )
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        ai_response = response[len(prompt):].strip()
        
        # Добавление ответа в историю
        self.chat_history.append(f"AI: {ai_response}")
        
        return ai_response

# Использование
chatbot = ChatBot()
response = chatbot.get_response("Привет! Как дела?")
print(response)
```

### Пример №2: Классификация текста с LLM

```python
def classify_text_with_llm(model, tokenizer, text, labels):
    """Классификация текста с использованием LLM"""
    prompt = f"Классифицируй следующий текст. Возможные категории: {', '.join(labels)}.\n\nТекст: {text}\n\nКатегория:"
    
    inputs = tokenizer.encode(prompt, return_tensors='pt')
    
    with torch.no_grad():
        outputs = model.generate(
            inputs,
            max_length=len(inputs[0]) + 20,
            temperature=0.1,  # Низкая температура для детерминированного ответа
            pad_token_id=tokenizer.eos_token_id,
        )
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    predicted_label = response[len(prompt):].strip()
    
    return predicted_label

# Пример использования
labels = ["спорт", "политика", "технологии", "культура"]
text = "Новый смартфон с революционной камерой был представлен на выставке"
predicted = classify_text_with_llm(model, tokenizer, text, labels)
print(f"Предсказанная категория: {predicted}")
```

### Пример №3: Резюмирование текста

```python
def summarize_text(model, tokenizer, text, max_summary_length=150):
    """Создание резюме текста"""
    prompt = f"Создай краткое резюме следующего текста:\n\n{text}\n\nРезюме:"
    
    inputs = tokenizer.encode(prompt, return_tensors='pt')
    
    with torch.no_grad():
        outputs = model.generate(
            inputs,
            max_length=len(inputs[0]) + max_summary_length,
            temperature=0.7,
            top_p=0.9,
            pad_token_id=tokenizer.eos_token_id,
        )
    
    summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return summary[len(prompt):].strip()

# Пример использования
long_text = """
Машинное обучение - это область искусственного интеллекта, 
которая фокусируется на разработке алгоритмов и статистических моделей, 
позволяющих компьютерным системам выполнять задачи без явного программирования. 
Эта технология находит применение в различных сферах: от медицинской диагностики 
до финансового анализа и автоматического перевода.
"""

summary = summarize_text(model, tokenizer, long_text)
print(f"Резюме: {summary}")
```

## Лучшие практики

### 1. Эффективное управление памятью:

```python
# Использование gradient checkpointing
from transformers import TrainingArguments

training_args = TrainingArguments(
    # ... другие параметры
    gradient_checkpointing=True,  # Уменьшает использование памяти
)

# Очистка кэша GPU
torch.cuda.empty_cache()

# Использование mixed precision training
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()
with autocast():
    outputs = model(inputs)
    loss = outputs.loss
    
scaler.scale(loss).backward()
scaler.step(optimizer)
scaler.update()
```

### 2. Обработка длинных последовательностей:

```python
# Sliding window attention для длинных текстов
def sliding_window_attention(model, tokenizer, long_text, window_size=512, stride=256):
    """Обработка длинных текстов с помощью скользящего окна"""
    tokens = tokenizer.encode(long_text, return_tensors='pt')[0]
    chunks = []
    
    for i in range(0, len(tokens), stride):
        chunk = tokens[i:i + window_size]
        if len(chunk) < window_size:
            chunk = torch.cat([chunk, torch.zeros(window_size - len(chunk), dtype=torch.long)])
        chunks.append(chunk)
    
    # Обработка каждого чанка
    embeddings = []
    for chunk in chunks:
        with torch.no_grad():
            output = model(chunk.unsqueeze(0), output_hidden_states=True)
            embedding = output.hidden_states[-1][:, 0, :]  # [CLS] токен
            embeddings.append(embedding)
    
    # Объединение эмбеддингов
    final_embedding = torch.mean(torch.stack(embeddings), dim=0)
    return final_embedding
```

### 3. Мониторинг и отладка:

```python
# Логирование во время обучения
import wandb
from transformers import TrainerCallback

class LoggingCallback(TrainerCallback):
    def on_log(self, args, state, control, logs=None, **kwargs):
        if state.is_local_process_zero:
            wandb.log(logs)

# Использование
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    callbacks=[LoggingCallback()],
)

# Мониторинг градиентов
def monitor_gradients(model):
    """Мониторинг норм градиентов"""
    total_norm = 0
    for name, param in model.named_parameters():
        if param.grad is not None:
            param_norm = param.grad.data.norm(2)
            total_norm += param_norm.item() ** 2
    total_norm = total_norm ** (1. / 2)
    return total_norm
```

### 4. Оптимизация гиперпараметров:

```python
from ray import tune
from ray.tune.schedulers import ASHAScheduler

def train_model(config):
    """Функция для оптимизации гиперпараметров"""
    model = AutoModelForCausalLM.from_pretrained("gpt2")
    
    training_args = TrainingArguments(
        output_dir="./results",
        num_train_epochs=config["epochs"],
        per_device_train_batch_size=config["batch_size"],
        learning_rate=config["learning_rate"],
        weight_decay=config["weight_decay"],
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
    )
    
    result = trainer.train()
    return {"loss": result.training_loss}

# Поиск оптимальных параметров
config = {
    "epochs": tune.choice([2, 3, 4]),
    "batch_size": tune.choice([2, 4, 8]),
    "learning_rate": tune.loguniform(1e-5, 1e-3),
    "weight_decay": tune.uniform(0.0, 0.3),
}

scheduler = ASHAScheduler(
    metric="loss",
    mode="min",
    max_t=10,
    grace_period=1,
    reduction_factor=2
)

analysis = tune.run(
    train_model,
    resources_per_trial={"cpu": 2, "gpu": 1},
    config=config,
    num_samples=10,
    scheduler=scheduler
)

print("Лучшие гиперпараметры:", analysis.best_config)
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