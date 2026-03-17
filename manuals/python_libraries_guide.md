# 📚 Полное руководство по основным библиотекам Python

**Версия:** 3.0
**Последнее обновление:** 2026 г.

## 📋 Содержание

1. [Веб-разработка](#веб-разработка)
2. [Научные вычисления и анализ данных](#научные-вычисления-и-анализ-данных)
3. [Машинное обучение и ИИ](#машинное-обучение-и-ии)
4. [Визуализация данных](#визуализация-данных)
5. [Веб-скрапинг и парсинг](#веб-скрапинг-и-парсинг)
6. [Работа с базами данных](#работа-с-базами-данных)
7. [Автоматизация и скриптинг](#автоматизация-и-скриптинг)
8. [GUI приложения](#gui-приложения)
9. [Тестирование и отладка](#тестирование-и-отладка)
10. [Обработка изображений и видео](#обработка-изображений-и-видео)
11. [Работа с текстом и NLP](#работа-с-текстом-и-nlp)
12. [Полезные команды](#полезные-команды)

---

## 🌐 Веб-разработка

### Django
```python
from django.http import HttpResponse
def hello(request):
    return HttpResponse("Hello, World!")
```
- Установка: `pip install django`

### Flask
```python
from flask import Flask
app = Flask(__name__)
@app.route('/')
def hello():
    return 'Hello, World!'
```
- Установка: `pip install flask`

### FastAPI
```python
from fastapi import FastAPI
app = FastAPI()
@app.get("/")
async def root():
    return {"message": "Hello World"}
```
- Установка: `pip install fastapi[standard]`

### Requests
```python
import requests
response = requests.get('https://api.github.com')
print(response.json())
```
- Установка: `pip install requests`

---

## 📊 Научные вычисления

### NumPy
```python
import numpy as np
arr = np.array([1, 2, 3, 4, 5])
print(arr.mean())
```
- Установка: `pip install numpy`

### Pandas
```python
import pandas as pd
data = {'Имя': ['Анна', 'Борис'], 'Возраст': [25, 30]}
df = pd.DataFrame(data)
print(df.groupby('Возраст').mean())
```
- Установка: `pip install pandas`

### SciPy
```python
from scipy import optimize
def f(x): return x**2 + 10*np.sin(x)
result = optimize.minimize(f, x0=0)
```
- Установка: `pip install scipy`

---

## 🤖 Машинное обучение

### Scikit-learn
```python
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
iris = datasets.load_iris()
model = RandomForestClassifier()
model.fit(iris.data, iris.target)
```
- Установка: `pip install scikit-learn`

### TensorFlow
```python
import tensorflow as tf
from tensorflow import keras
model = keras.Sequential([
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])
```
- Установка: `pip install tensorflow`

### PyTorch
```python
import torch
import torch.nn as nn
class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(784, 10)
```
- Установка: `pip install torch torchvision`

### Transformers (Hugging Face)
```python
from transformers import pipeline
classifier = pipeline("sentiment-analysis")
result = classifier("I love Python!")
```
- Установка: `pip install transformers`

---

## 📈 Визуализация данных

### Matplotlib
```python
import matplotlib.pyplot as plt
import numpy as np
x = np.linspace(0, 10, 100)
plt.plot(x, np.sin(x))
plt.show()
```
- Установка: `pip install matplotlib`

### Seaborn
```python
import seaborn as sns
tips = sns.load_dataset("tips")
sns.boxplot(x='day', y='total_bill', data=tips)
```
- Установка: `pip install seaborn`

### Plotly
```python
import plotly.express as px
df = px.data.iris()
fig = px.scatter(df, x='sepal_width', y='sepal_length')
fig.show()
```
- Установка: `pip install plotly`

---

## 🕷️ Веб-скрапинг

### Beautiful Soup
```python
from bs4 import BeautifulSoup
import requests
soup = BeautifulSoup(response.text, 'html.parser')
links = soup.find_all('a')
```
- Установка: `pip install beautifulsoup4`

### Selenium
```python
from selenium import webdriver
driver = webdriver.Chrome()
driver.get("https://www.google.com")
```
- Установка: `pip install selenium`

### Playwright
```python
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    page = p.chromium.launch().new_page()
    page.goto("https://example.com")
```
- Установка: `pip install playwright`

---

## 🗄️ Базы данных

### SQLAlchemy
```python
from sqlalchemy import create_engine
engine = create_engine('sqlite:///example.db')
```
- Установка: `pip install sqlalchemy`

### PyMongo (MongoDB)
```python
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
collection = client.mydb.users
```
- Установка: `pip install pymongo`

### redis-py
```python
import redis
r = redis.Redis(host='localhost', port=6379, db=0)
r.set('key', 'value')
```
- Установка: `pip install redis`

---

## 🖥️ GUI приложения

### Tkinter (встроенный)
```python
import tkinter as tk
window = tk.Tk()
window.title("My App")
window.mainloop()
```

### PyQt5
```python
import sys
from PyQt5.QtWidgets import QApplication, QWidget
app = QApplication(sys.argv)
window = QWidget()
window.show()
```
- Установка: `pip install PyQt5`

---

## 🎨 Обработка изображений

### Pillow
```python
from PIL import Image
img = Image.open('photo.jpg')
img = img.resize((800, 600))
img.save('output.jpg')
```
- Установка: `pip install Pillow`

### OpenCV
```python
import cv2
img = cv2.imread('photo.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
```
- Установка: `pip install opencv-python`

---

## 🧪 Тестирование

### pytest
```python
def add(a, b): return a + b
def test_add():
    assert add(2, 3) == 5
```
- Установка: `pip install pytest`

### unittest (встроенный)
```python
import unittest
class TestMath(unittest.TestCase):
    def test_sum(self):
        self.assertEqual(sum([1,2,3]), 6)
```

---

## 📝 Работа с текстом

### re (встроенный)
```python
import re
emails = re.findall(r'[\w\.-]+@[\w\.-]+', text)
```

### TextBlob
```python
from textblob import TextBlob
blob = TextBlob("I love Python!")
print(blob.sentiment)
```
- Установка: `pip install textblob`

---

## 🔄 Парсинг данных

### json (встроенный)
```python
import json
data = {"name": "Alice", "age": 30}
json_str = json.dumps(data, indent=2)
```

### PyYAML
```python
import yaml
data = yaml.safe_load("name: Alice\nage: 30")
```
- Установка: `pip install pyyaml`

---

## ⚡ Асинхронность

### asyncio (встроенный)
```python
import asyncio
async def main():
    await asyncio.sleep(1)
    print("Done")
asyncio.run(main())
```

---

## 🎮 Игры

### Pygame
```python
import pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
```
- Установка: `pip install pygame`

---

## 💡 Полезные команды

### Установка пакетов
```bash
pip install package_name
pip install package_name==1.2.3
pip install -r requirements.txt
pip freeze > requirements.txt
```

### Виртуальное окружение
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
deactivate
```

### Poetry
```bash
pip install poetry
poetry new myproject
poetry add requests
poetry shell
```

### Полезные команды Python
```bash
python -m http.server 8000        # HTTP сервер
python -m pdb script.py            # Отладчик
python -m pytest                   # Запуск тестов
python -m unittest discover        # Запуск unittest
```

---

## 📚 Быстрый выбор

| Задача | Рекомендуемые библиотеки |
|--------|-------------------------|
| **Веб-разработка** | Django, Flask, FastAPI |
| **API** | FastAPI, Requests |
| **Анализ данных** | Pandas, NumPy |
| **Машинное обучение** | Scikit-learn, TensorFlow |
| **Визуализация** | Matplotlib, Seaborn |
| **Парсинг сайтов** | BeautifulSoup, Selenium |
| **Базы данных** | SQLAlchemy, PyMongo |
| **GUI** | Tkinter, PyQt5 |
| **Обработка изображений** | Pillow, OpenCV |
| **NLP** | Transformers, TextBlob |

---

## 🔗 Полезные ресурсы

- [PyPI](https://pypi.org/)
- [Awesome Python](https://github.com/vinta/awesome-python)
- [Python Docs](https://docs.python.org/3/)

---

*Happy Coding! 🐍✨*