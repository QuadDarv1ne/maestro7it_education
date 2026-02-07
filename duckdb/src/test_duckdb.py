# Скрипт тестирования для проверки установки DuckDB
# Автор: Дуплей Максим Игоревич

import duckdb
print(duckdb.sql("SELECT 'DuckDB работает :D' AS message;"))