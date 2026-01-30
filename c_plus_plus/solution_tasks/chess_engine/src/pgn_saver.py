#!/usr/bin/env python3
"""
Система сохранения и загрузки шахматных партий в формате PGN
PGN (Portable Game Notation) - стандартный формат для записи шахматных партий
"""

from datetime import datetime
import re
from typing import List, Dict, Optional, Tuple

class PGNSaver:
    """Класс для сохранения и загрузки партий в формате PGN"""
    
    def __init__(self):
        self.required_tags = [
            'Event', 'Site', 'Date', 'Round', 'White', 'Black', 'Result'
        ]
        
    def save_game(self, moves: List[str], metadata: Dict[str, str], filename: str) -> bool:
        """
        Сохраняет партию в PGN файл
        
        Args:
            moves: Список ходов в алгебраической нотации
            metadata: Метаданные партии (Event, Site, Date, и т.д.)
            filename: Имя файла для сохранения
            
        Returns:
            bool: Успешность операции
        """
        try:
            # Создаем PGN контент
            pgn_content = self._create_pgn_content(moves, metadata)
            
            # Записываем в файл
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(pgn_content)
            
            print(f"✅ Партия успешно сохранена в {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка сохранения партии: {e}")
            return False
    
    def load_game(self, filename: str) -> Optional[Tuple[List[str], Dict[str, str]]]:
        """
        Загружает партию из PGN файла
        
        Args:
            filename: Имя файла для загрузки
            
        Returns:
            Tuple[List[str], Dict[str, str]]: Кортеж (ходы, метаданные) или None при ошибке
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Парсим PGN
            moves, metadata = self._parse_pgn_content(content)
            
            print(f"✅ Партия успешно загружена из {filename}")
            print(f"   Ходов: {len(moves)}")
            print(f"   Белые: {metadata.get('White', 'Неизвестно')}")
            print(f"   Черные: {metadata.get('Black', 'Неизвестно')}")
            print(f"   Результат: {metadata.get('Result', '?')}")
            
            return moves, metadata
            
        except Exception as e:
            print(f"❌ Ошибка загрузки партии: {e}")
            return None
    
    def _create_pgn_content(self, moves: List[str], metadata: Dict[str, str]) -> str:
        """Создает PGN контент из ходов и метаданных"""
        
        # Добавляем обязательные теги если их нет
        default_metadata = {
            'Event': 'Casual Game',
            'Site': 'Local',
            'Date': datetime.now().strftime('%Y.%m.%d'),
            'Round': '1',
            'White': 'Player1',
            'Black': 'Player2', 
            'Result': '*'
        }
        
        # Объединяем метаданные
        for key, value in default_metadata.items():
            if key not in metadata:
                metadata[key] = value
        
        # Создаем заголовок с тегами
        header = ""
        for tag in self.required_tags:
            if tag in metadata:
                header += f'[{tag} "{metadata[tag]}"]\n'
        
        # Добавляем дополнительные теги
        for tag, value in metadata.items():
            if tag not in self.required_tags:
                header += f'[{tag} "{value}"]\n'
        
        header += "\n"
        
        # Форматируем ходы
        formatted_moves = self._format_moves(moves)
        
        # Добавляем результат
        result = metadata.get('Result', '*')
        formatted_moves += f" {result}"
        
        return header + formatted_moves
    
    def _format_moves(self, moves: List[str]) -> str:
        """Форматирует ходы в PGN нотацию"""
        formatted = []
        
        for i, move in enumerate(moves):
            move_number = (i // 2) + 1
            
            # Добавляем номер хода для белых
            if i % 2 == 0:
                formatted.append(f"{move_number}.")
            
            # Конвертируем в стандартную нотацию если нужно
            standard_move = self._convert_to_standard_notation(move)
            formatted.append(standard_move)
        
        return " ".join(formatted)
    
    def _convert_to_standard_notation(self, move: str) -> str:
        """Конвертирует ход в стандартную алгебраическую нотацию"""
        # Упрощенная реализация - в реальном проекте нужна полная конвертация
        # Здесь просто возвращаем ход как есть, предполагая что он уже в правильном формате
        return move
    
    def _parse_pgn_content(self, content: str) -> Tuple[List[str], Dict[str, str]]:
        """Парсит PGN контент"""
        lines = content.strip().split('\n')
        
        metadata = {}
        moves = []
        
        # Парсим теги
        i = 0
        while i < len(lines) and lines[i].startswith('['):
            tag_match = re.match(r'\[(\w+)\s+"(.*)"\]', lines[i])
            if tag_match:
                tag_name = tag_match.group(1)
                tag_value = tag_match.group(2)
                metadata[tag_name] = tag_value
            i += 1
        
        # Пропускаем пустые строки
        while i < len(lines) and not lines[i].strip():
            i += 1
        
        # Парсим ходы
        if i < len(lines):
            moves_text = " ".join(lines[i:])
            moves = self._parse_moves(moves_text)
        
        return moves, metadata
    
    def _parse_moves(self, moves_text: str) -> List[str]:
        """Парсит текст ходов"""
        # Убираем результат
        moves_text = re.sub(r'\s*(1-0|0-1|1/2-1/2|\*)\s*$', '', moves_text)
        
        # Разбиваем на отдельные элементы
        elements = moves_text.split()
        
        moves = []
        for element in elements:
            # Пропускаем номера ходов
            if element.endswith('.') or re.match(r'^\d+\.$', element):
                continue
            
            # Добавляем ход
            moves.append(element)
        
        return moves
    
    def validate_pgn(self, filename: str) -> bool:
        """Проверяет валидность PGN файла"""
        try:
            moves, metadata = self.load_game(filename)
            if moves is None:
                return False
            
            # Проверяем обязательные теги
            for tag in self.required_tags:
                if tag not in metadata:
                    print(f"❌ Отсутствует обязательный тег: {tag}")
                    return False
            
            # Проверяем формат результата
            result = metadata.get('Result', '')
            if result not in ['1-0', '0-1', '1/2-1/2', '*']:
                print(f"❌ Неверный формат результата: {result}")
                return False
            
            print("✅ PGN файл валиден")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка валидации PGN: {e}")
            return False
    
    def parse_pgn(self, pgn_content: str) -> Optional[Dict[str, any]]:
        """
        Парсит PGN содержимое и возвращает структурированные данные
        
        Args:
            pgn_content: Текст в формате PGN
            
        Returns:
            Dict с ключами 'white', 'black', 'result', 'moves', 'metadata'
        """
        try:
            moves, metadata = self._parse_pgn_content(pgn_content)
            
            return {
                'white': metadata.get('White', 'Player1'),
                'black': metadata.get('Black', 'Player2'),
                'result': metadata.get('Result', '*'),
                'moves': moves,
                'metadata': metadata
            }
        except Exception as e:
            print(f"❌ Ошибка парсинга PGN: {e}")
            return None

class GameRecorder:
    """Класс для записи партии в реальном времени"""
    
    def __init__(self):
        self.moves = []
        self.metadata = {}
        self.pgn_saver = PGNSaver()
    
    def start_recording(self, white_player: str = "Player1", black_player: str = "Player2"):
        """Начинает запись новой партии"""
        self.moves = []
        self.metadata = {
            'Event': 'Recorded Game',
            'Site': 'Local Chess Engine',
            'Date': datetime.now().strftime('%Y.%m.%d'),
            'Round': '1',
            'White': white_player,
            'Black': black_player,
            'Result': '*'
        }
        print(f"⏺️  Начата запись партии: {white_player} vs {black_player}")
    
    def add_move(self, move: str):
        """Добавляет ход к записи"""
        self.moves.append(move)
        print(f"➕ Ход добавлен: {move} (всего ходов: {len(self.moves)})")
    
    def set_result(self, result: str):
        """Устанавливает результат партии"""
        valid_results = ['1-0', '0-1', '1/2-1/2', '*']
        if result in valid_results:
            self.metadata['Result'] = result
            print(f"🏁 Результат установлен: {result}")
        else:
            print(f"❌ Неверный результат: {result}")
    
    def save_to_file(self, filename: str) -> bool:
        """Сохраняет записанную партию в файл"""
        if not self.moves:
            print("❌ Нет ходов для сохранения")
            return False
        
        return self.pgn_saver.save_game(self.moves, self.metadata, filename)
    
    def get_current_pgn(self) -> str:
        """Возвращает текущую партию в формате PGN"""
        if not self.moves:
            return ""
        
        return self.pgn_saver._create_pgn_content(self.moves, self.metadata)
    
    def get_pgn(self) -> str:
        """Алиас для get_current_pgn для совместимости с API"""
        return self.get_current_pgn()

# Демонстрационные функции
def demonstrate_pgn_saver():
    """Демонстрирует работу системы сохранения PGN"""
    print("=== ДЕМОНСТРАЦИЯ СИСТЕМЫ PGN ===")
    
    # Создаем тестовую партию
    test_moves = [
        "e4", "e5", "Nf3", "Nc6", "Bb5", "a6", "Ba4", "Nf6", 
        "O-O", "Be7", "Re1", "b5", "Bb3", "d6", "c3", "O-O"
    ]
    
    test_metadata = {
        'Event': 'Demo Tournament',
        'Site': 'Chess Engine Demo',
        'Date': '2026.01.30',
        'Round': '1',
        'White': 'Magnus Carlsen',
        'Black': 'Garry Kasparov',
        'Result': '1/2-1/2'
    }
    
    # Создаем saver
    saver = PGNSaver()
    
    # Сохраняем партию
    print("\n💾 Сохранение тестовой партии...")
    success = saver.save_game(test_moves, test_metadata, "demo_game.pgn")
    
    if success:
        # Загружаем партию
        print("\n📂 Загрузка партии...")
        loaded_data = saver.load_game("demo_game.pgn")
        
        if loaded_data:
            loaded_moves, loaded_metadata = loaded_data
            
            print(f"\n📋 Загруженные данные:")
            print(f"   Ходов: {len(loaded_moves)}")
            print(f"   Белые: {loaded_metadata.get('White')}")
            print(f"   Черные: {loaded_metadata.get('Black')}")
            print(f"   Результат: {loaded_metadata.get('Result')}")
            print(f"   Первые 5 ходов: {' '.join(loaded_moves[:5])}")
        
        # Проверяем валидность
        print("\n✅ Проверка валидности...")
        is_valid = saver.validate_pgn("demo_game.pgn")
        print(f"   Валидность: {'Да' if is_valid else 'Нет'}")
    
    # Демонстрация GameRecorder
    print("\n" + "="*50)
    print("🎮 ДЕМОНСТРАЦИЯ GameRecorder:")
    
    recorder = GameRecorder()
    recorder.start_recording("Alice", "Bob")
    
    # Добавляем несколько ходов
    demo_moves = ["e4", "e5", "Nf3", "Nc6", "Bb5"]
    for move in demo_moves:
        recorder.add_move(move)
    
    recorder.set_result("1-0")
    
    # Сохраняем
    recorder.save_to_file("recorded_game.pgn")
    
    print(f"\n📝 Текущий PGN:")
    print(recorder.get_current_pgn())

if __name__ == "__main__":
    try:
        demonstrate_pgn_saver()
        print("\n\nНажмите Enter для завершения...")
        input()
    except KeyboardInterrupt:
        print("\n\nДемонстрация прервана пользователем")
    except Exception as e:
        print(f"\nОшибка: {e}")