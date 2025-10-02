'''
Установка DuckDB
~ pip install duckdb

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

import duckdb
print(duckdb.sql("SELECT 'DuckDB работает :D' AS message;"))