"""
Скрипт для обновления структуры базы данных с новыми полями
"""
import sqlite3
import os

def update_database_schema():
    """Обновление схемы базы данных для добавления новых полей"""
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'chess_calendar.db')
    
    # Проверяем существование базы данных
    if not os.path.exists(db_path):
        print(f"База данных не найдена: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Проверяем, существуют ли уже новые столбцы
        cursor.execute("PRAGMA table_info(tournament)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Добавляем новые столбцы, если они не существуют
        if 'prize_fund_usd' not in columns:
            cursor.execute("ALTER TABLE tournament ADD COLUMN prize_fund_usd INTEGER")
            print("✅ Добавлен столбец prize_fund_usd")
        
        if 'players_count' not in columns:
            cursor.execute("ALTER TABLE tournament ADD COLUMN players_count INTEGER")
            print("✅ Добавлен столбец players_count")
        
        if 'time_control' not in columns:
            cursor.execute("ALTER TABLE tournament ADD COLUMN time_control TEXT")
            print("✅ Добавлен столбец time_control")
        
        conn.commit()
        conn.close()
        
        print("🎉 Обновление схемы базы данных успешно завершено!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при обновлении схемы базы данных: {e}")
        return False

if __name__ == "__main__":
    update_database_schema()