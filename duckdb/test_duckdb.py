'''
Проверка Python установки:
~ %LOCALAPPDATA%\Programs\Python

Добавление в PATH:
~ C:\Users\maksi\AppData\Local\Programs\Python\Python313
~ C:\Users\maksi\AppData\Local\Programs\Python\Python313\Scripts

Установка venv окружения:
~ python -m venv duckdb_venv
~ duckdb_venv\bin\Activate.ps1
~ pip install duckdb

Установка DuckDB:
~ pip install duckdb

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

import duckdb
print(duckdb.sql("SELECT 'DuckDB работает :D' AS message;"))