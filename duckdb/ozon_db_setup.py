'''
Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

# ozon_db_setup.py
# Полный скрипт для создания и заполнения базы данных товаров Ozon с использованием DuckDB

import duckdb
import json
from datetime import datetime

# === ШАГ №1: Подключение к базе данных (файл на диске) ===
# Если файла нет — он создастся автоматически
con = duckdb.connect('ozon_products.duckdb')

# === ШАГ №2: Создание таблицы товаров ===
con.execute("""
CREATE TABLE IF NOT EXISTS ozon_products (
    product_id      BIGINT PRIMARY KEY,
    name            VARCHAR,
    brand           VARCHAR,
    category        VARCHAR,
    price           DOUBLE,
    old_price       DOUBLE,
    rating          DOUBLE,
    review_count    INTEGER,
    is_in_stock     BOOLEAN,
    url             VARCHAR,
    description     VARCHAR,
    characteristics VARCHAR,  -- хранится как JSON-строка
    scraped_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

print("✅ Таблица 'ozon_products' создана или уже существует.")

# === ШАГ №3: Пример добавления данных (в реальности — из парсера или API) ===
# Пример товара (реальные данные можно получать через скрапинг или API)
# Добавление 15 реалистичных записей
products = [
    {
        "product_id": 100000001,
        "name": "Смартфон Apple iPhone 15 128GB",
        "brand": "Apple",
        "category": "Электроника > Смартфоны",
        "price": 79990.0,
        "old_price": 84990.0,
        "rating": 4.9,
        "review_count": 3210,
        "is_in_stock": True,
        "url": "https://www.ozon.ru/product/100000001/",
        "description": "Новейший флагманский смартфон от Apple с чипом A17.",
        "characteristics": json.dumps({
            "Цвет": "Чёрный",
            "Память": "128 ГБ",
            "Экран": "6.1 дюйма",
            "ОС": "iOS 17"
        }, ensure_ascii=False)
    },
    {
        "product_id": 100000002,
        "name": "Наушники Sony WH-1000XM5",
        "brand": "Sony",
        "category": "Электроника > Аудиотехника",
        "price": 24990.0,
        "old_price": 29990.0,
        "rating": 4.8,
        "review_count": 1247,
        "is_in_stock": True,
        "url": "https://www.ozon.ru/product/100000002/",
        "description": "Беспроводные наушники с активным шумоподавлением.",
        "characteristics": json.dumps({
            "Тип": "Накладные",
            "Bluetooth": "5.2",
            "Время работы": "30 ч"
        }, ensure_ascii=False)
    },
    {
        "product_id": 100000003,
        "name": "Книга 'Атомные привычки' Джеймс Клир",
        "brand": "Альпина Паблишер",
        "category": "Книги > Саморазвитие",
        "price": 699.0,
        "old_price": 899.0,
        "rating": 4.7,
        "review_count": 8920,
        "is_in_stock": True,
        "url": "https://www.ozon.ru/product/100000003/",
        "description": "Бестселлер о том, как строить полезные привычки.",
        "characteristics": json.dumps({
            "Формат": "Твёрдый переплёт",
            "Страниц": "368",
            "Язык": "Русский"
        }, ensure_ascii=False)
    },
    {
        "product_id": 100000004,
        "name": "Пылесос Xiaomi Mi Vacuum-Mop 2 Pro",
        "brand": "Xiaomi",
        "category": "Бытовая техника > Уборка",
        "price": 18990.0,
        "old_price": 22990.0,
        "rating": 4.6,
        "review_count": 2105,
        "is_in_stock": False,
        "url": "https://www.ozon.ru/product/100000004/",
        "description": "Робот-пылесос с функцией влажной уборки.",
        "characteristics": json.dumps({
            "Мощность": "3000 Па",
            "Ёмкость бака": "200 мл",
            "Время работы": "150 мин"
        }, ensure_ascii=False)
    },
    {
        "product_id": 100000005,
        "name": "Крем для лица La Roche-Posay Hydreane",
        "brand": "La Roche-Posay",
        "category": "Красота > Уход за кожей",
        "price": 1299.0,
        "old_price": 1499.0,
        "rating": 4.8,
        "review_count": 4320,
        "is_in_stock": True,
        "url": "https://www.ozon.ru/product/100000005/",
        "description": "Увлажняющий крем для чувствительной кожи.",
        "characteristics": json.dumps({
            "Объём": "50 мл",
            "Тип кожи": "Чувствительная",
            "Без отдушек": "Да"
        }, ensure_ascii=False)
    },
    {
        "product_id": 100000006,
        "name": "Ноутбук Lenovo IdeaPad 3 15ADA6",
        "brand": "Lenovo",
        "category": "Электроника > Ноутбуки",
        "price": 39990.0,
        "old_price": 44990.0,
        "rating": 4.5,
        "review_count": 876,
        "is_in_stock": True,
        "url": "https://www.ozon.ru/product/100000006/",
        "description": "Бюджетный ноутбук для учёбы и работы.",
        "characteristics": json.dumps({
            "Процессор": "AMD Ryzen 5",
            "ОЗУ": "8 ГБ",
            "SSD": "512 ГБ",
            "Экран": "15.6 дюймов"
        }, ensure_ascii=False)
    },
    {
        "product_id": 100000007,
        "name": "Чайник электрический Redmond RK-G212S",
        "brand": "Redmond",
        "category": "Бытовая техника > Кухонная техника",
        "price": 2490.0,
        "old_price": 2990.0,
        "rating": 4.4,
        "review_count": 3421,
        "is_in_stock": True,
        "url": "https://www.ozon.ru/product/100000007/",
        "description": "Стеклянный чайник с терморегулятором.",
        "characteristics": json.dumps({
            "Объём": "1.7 л",
            "Мощность": "2200 Вт",
            "Подсветка": "Синяя"
        }, ensure_ascii=False)
    },
    {
        "product_id": 100000008,
        "name": "Фитнес-браслет Huawei Band 8",
        "brand": "Huawei",
        "category": "Электроника > Гаджеты",
        "price": 3990.0,
        "old_price": 4990.0,
        "rating": 4.7,
        "review_count": 1543,
        "is_in_stock": True,
        "url": "https://www.ozon.ru/product/100000008/",
        "description": "Лёгкий и стильный фитнес-трекер с ЭКГ.",
        "characteristics": json.dumps({
            "Вес": "14 г",
            "Водонепроницаемость": "5 ATM",
            "Автономность": "14 дней"
        }, ensure_ascii=False)
    },
    {
        "product_id": 100000009,
        "name": "Кофе молотый Lavazza Qualità Rossa",
        "brand": "Lavazza",
        "category": "Продукты > Кофе",
        "price": 599.0,
        "old_price": 699.0,
        "rating": 4.6,
        "review_count": 2876,
        "is_in_stock": True,
        "url": "https://www.ozon.ru/product/100000009/",
        "description": "Ароматный итальянский кофе для эспрессо.",
        "characteristics": json.dumps({
            "Вес": "250 г",
            "Обжарка": "Средняя",
            "Тип": "Молотый"
        }, ensure_ascii=False)
    },
    {
        "product_id": 100000010,
        "name": "Рюкзак городской Xiaomi 20L",
        "brand": "Xiaomi",
        "category": "Мода > Сумки и рюкзаки",
        "price": 2990.0,
        "old_price": 3490.0,
        "rating": 4.5,
        "review_count": 987,
        "is_in_stock": True,
        "url": "https://www.ozon.ru/product/100000010/",
        "description": "Водонепроницаемый рюкзак с отделением для ноутбука.",
        "characteristics": json.dumps({
            "Объём": "20 л",
            "Материал": "Нейлон",
            "Цвет": "Серый"
        }, ensure_ascii=False)
    },
    {
        "product_id": 100000011,
        "name": "Планшет Samsung Galaxy Tab A9",
        "brand": "Samsung",
        "category": "Электроника > Планшеты",
        "price": 14990.0,
        "old_price": 16990.0,
        "rating": 4.6,
        "review_count": 654,
        "is_in_stock": True,
        "url": "https://www.ozon.ru/product/100000011/",
        "description": "Лёгкий и мощный планшет для развлечений.",
        "characteristics": json.dumps({
            "Экран": "8.7 дюймов",
            "Память": "64 ГБ",
            "Аккумулятор": "5100 мА·ч"
        }, ensure_ascii=False)
    },
    {
        "product_id": 100000012,
        "name": "Шампунь против перхоти Head & Shoulders",
        "brand": "Head & Shoulders",
        "category": "Красота > Уход за волосами",
        "price": 349.0,
        "old_price": 399.0,
        "rating": 4.3,
        "review_count": 5432,
        "is_in_stock": True,
        "url": "https://www.ozon.ru/product/100000012/",
        "description": "Эффективный шампунь для борьбы с перхотью.",
        "characteristics": json.dumps({
            "Объём": "400 мл",
            "Тип волос": "Все типы",
            "Эффект": "Против перхоти"
        }, ensure_ascii=False)
    },
    {
        "product_id": 100000013,
        "name": "Микроволновая печь Panasonic NN-ST27JW",
        "brand": "Panasonic",
        "category": "Бытовая техника > Кухонная техника",
        "price": 8990.0,
        "old_price": 9990.0,
        "rating": 4.7,
        "review_count": 1234,
        "is_in_stock": False,
        "url": "https://www.ozon.ru/product/100000013/",
        "description": "Компактная микроволновка с грилем.",
        "characteristics": json.dumps({
            "Объём": "27 л",
            "Мощность": "1000 Вт",
            "Гриль": "Да"
        }, ensure_ascii=False)
    },
    {
        "product_id": 100000014,
        "name": "Кроссовки Nike Air Max 270",
        "brand": "Nike",
        "category": "Мода > Обувь",
        "price": 12990.0,
        "old_price": 14990.0,
        "rating": 4.8,
        "review_count": 3210,
        "is_in_stock": True,
        "url": "https://www.ozon.ru/product/100000014/",
        "description": "Стильные кроссовки с амортизацией Air Max.",
        "characteristics": json.dumps({
            "Размер": "42",
            "Цвет": "Белый/Чёрный",
            "Материал": "Текстиль + кожа"
        }, ensure_ascii=False)
    },
    {
        "product_id": 100000015,
        "name": "Набор кистей для макияжа Morphe",
        "brand": "Morphe",
        "category": "Красота > Макияж",
        "price": 1990.0,
        "old_price": 2490.0,
        "rating": 4.5,
        "review_count": 876,
        "is_in_stock": True,
        "url": "https://www.ozon.ru/product/100000015/",
        "description": "Профессиональный набор из 12 кистей.",
        "characteristics": json.dumps({
            "Количество": "12 шт",
            "Щетина": "Синтетика",
            "Чехол": "Да"
        }, ensure_ascii=False)
    }
]

# === ШАГ №4: Вставка всех 15 записей ===
for p in products:
    con.execute("""
    INSERT INTO ozon_products (
        product_id, name, brand, category, price, old_price,
        rating, review_count, is_in_stock, url, description, characteristics
    ) VALUES (
        ?, ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?, ?
    )
    ON CONFLICT (product_id) DO UPDATE SET
        price = EXCLUDED.price,
        old_price = EXCLUDED.old_price,
        rating = EXCLUDED.rating,
        review_count = EXCLUDED.review_count,
        is_in_stock = EXCLUDED.is_in_stock,
        scraped_at = CURRENT_TIMESTAMP;
    """, list(p.values()))

print(f"✅ Добавлено {len(products)} товаров в базу.")

# === ШАГ №5: Проверка данных ===
result = con.execute("SELECT * FROM ozon_products LIMIT 1;").fetchdf()
print("\n🔍 Пример записи из базы:")
print(result)

# === ШАГ №6: Полезные аналитические запросы ===
print("\n📊 Топ-3 самых дорогих товаров:")
top_expensive = con.execute("""
    SELECT name, brand, price
    FROM ozon_products
    ORDER BY price DESC
    LIMIT 3;
""").fetchdf()
print(top_expensive)

print("\n📈 Средний рейтинг по брендам:")
avg_rating = con.execute("""
    SELECT brand, AVG(rating) AS avg_rating, COUNT(*) AS products
    FROM ozon_products
    WHERE rating IS NOT NULL
    GROUP BY brand
    ORDER BY avg_rating DESC;
""").fetchdf()
print(avg_rating)

print("\n📊 Топ-5 самых дорогих товаров:")
print(con.execute("""
    SELECT name, brand, price FROM ozon_products
    ORDER BY price DESC LIMIT 5;
""").fetchdf())

print("\n📈 Товары с рейтингом выше 4.7:")
print(con.execute("""
    SELECT name, rating, review_count
    FROM ozon_products
    WHERE rating > 4.7
    ORDER BY review_count DESC;
""").fetchdf())

# Закрытие соединения и правильная утилизация данных
con.close()
print("\n💾 База сохранена в 'ozon_products.duckdb'")