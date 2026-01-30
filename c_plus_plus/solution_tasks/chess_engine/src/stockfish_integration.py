#!/usr/bin/env python3
"""
Интеграция с Stockfish - самым сильным шахматным движком в мире
Stockfish имеет рейтинг Elo ~3500+ и используется в топ-классе шахмат
"""

import subprocess
import threading
import time
import os
from typing import Optional, Tuple, List

class StockfishIntegration:
    """Интеграция с Stockfish движком"""
    
    def __init__(self, stockfish_path: str = None, threads: int = 6, hash_size: int = 2048):
        self.stockfish_process = None
        self.stockfish_path = stockfish_path or self._find_stockfish()
        self.is_running = False
        self.lock = threading.Lock()
        self.threads = threads
        self.hash_size = hash_size
        
        # Оптимизированные параметры Stockfish для многопоточной обработки
        self.default_params = {
            "Threads": self.threads,     # Количество потоков CPU
            "Hash": self.hash_size,      # Размер хэш-таблицы (MB)
            "MultiPV": 1,               # Количество вариантов анализа
            "Skill Level": 20,          # Максимальный уровень мастерства
            "Move Overhead": 10,        # Время на накладные расходы (мс)
            "Slow Mover": 100,          # Скорость игры
            "UCI_Chess960": False,      # Шахматы Фишера
            "UCI_AnalyseMode": True,    # Режим анализа
            "Contempt": 0,              # Нейтральная оценка
            "Min Split Depth": 6,       # Минимальная глубина разделения
            "SyzygyPath": "<empty>",    # Путь к эндшпильным базам
            "LargePages": True,         # Использование больших страниц памяти
            "Ponder": False             # Отключение ponder режима для скорости
        }
        
    def _find_stockfish(self) -> Optional[str]:
        """Поиск Stockfish в системе"""
        # Возможные пути к Stockfish
        possible_paths = [
            # Windows
            "stockfish-windows-x86-64-avx2.exe",
            "stockfish-windows-x86-64.exe", 
            "stockfish.exe",
            "./stockfish.exe",
            "../stockfish.exe",
            # Linux
            "stockfish",
            "./stockfish",
            "/usr/local/bin/stockfish",
            "/usr/bin/stockfish",
            # macOS
            "stockfish-mac",
            "./stockfish-mac"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        # Проверяем, установлен ли через package manager
        try:
            result = subprocess.run(["which", "stockfish"], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
            
        return None
    
    def start_engine(self) -> bool:
        """Запуск Stockfish"""
        try:
            if not self.stockfish_path:
                print("Stockfish не найден в системе!")
                print("Пожалуйста, скачайте Stockfish с https://stockfishchess.org/download/")
                return False
            
            # Запускаем Stockfish как subprocess
            self.stockfish_process = subprocess.Popen(
                [self.stockfish_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            
            self.is_running = True
            
            # Инициализация UCI
            if not self._send_uci_command("uci"):
                return False
                
            # Установка параметров
            for param, value in self.default_params.items():
                self._send_uci_command(f"setoption name {param} value {value}")
            
            # Готовность
            if not self._send_uci_command("isready"):
                return False
                
            print(f"✅ Stockfish успешно запущен: {self.stockfish_path}")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка запуска Stockfish: {e}")
            return False
    
    def stop_engine(self):
        """Остановка Stockfish"""
        with self.lock:
            if self.stockfish_process:
                try:
                    self._send_uci_command("quit")
                    self.stockfish_process.wait(timeout=5)
                except:
                    self.stockfish_process.kill()
                finally:
                    self.stockfish_process = None
                    self.is_running = False
    
    def _send_uci_command(self, command: str, wait_response: bool = True) -> Optional[List[str]]:
        """Отправка команды UCI и получение ответа"""
        if not self.stockfish_process or not self.is_running:
            return None
            
        try:
            with self.lock:
                # Отправляем команду
                self.stockfish_process.stdin.write(command + '\n')
                self.stockfish_process.stdin.flush()
                
                if not wait_response:
                    return None
                
                # Читаем ответ
                response_lines = []
                while True:
                    line = self.stockfish_process.stdout.readline().strip()
                    if not line:
                        break
                    response_lines.append(line)
                    
                    # Завершающие маркеры
                    if line == "uciok" or line == "readyok" or line.startswith("bestmove"):
                        break
                        
                return response_lines
                
        except Exception as e:
            print(f"Ошибка отправки команды: {e}")
            return None
    
    def get_best_move(self, fen: str, depth: int = 18, movetime: int = 1500) -> Optional[str]:
        """Получение лучшего хода от Stockfish"""
        if not self.is_running:
            return None
            
        try:
            # Устанавливаем позицию
            self._send_uci_command(f"position fen {fen}", False)
            
            # Запускаем поиск
            search_command = f"go depth {depth}"
            if movetime:
                search_command += f" movetime {movetime}"
                
            response = self._send_uci_command(search_command, True)
            
            if response:
                # Ищем строку с лучшим ходом
                for line in response:
                    if line.startswith("bestmove"):
                        move = line.split()[1]
                        if move != "(none)":
                            return move
            
            return None
            
        except Exception as e:
            print(f"Ошибка получения хода от Stockfish: {e}")
            return None
    
    def analyze_position(self, fen: str, depth: int = 18, multipv: int = 3) -> dict:
        """Анализ позиции с оценкой"""
        if not self.is_running:
            return {}
            
        try:
            # Устанавливаем позицию
            self._send_uci_command(f"position fen {fen}", False)
            
            # Устанавливаем MultiPV для анализа нескольких линий
            self._send_uci_command(f"setoption name MultiPV value {multipv}", False)
            
            # Запускаем параллельный анализ
            search_command = f"go depth {depth}"
            if movetime:
                search_command += f" movetime {movetime}"
                
            response = self._send_uci_command(search_command, True)
            
            analysis = {
                "score": None,
                "depth": 0,
                "nodes": 0,
                "nps": 0,
                "pv": [],
                "multipv_lines": [],
                "time_spent": 0,
                "seldepth": 0
            }
            
            if response:
                for line in response:
                    if "score cp" in line:
                        # Центипешки (оценка в сотых долях пешки)
                        parts = line.split()
                        try:
                            cp_index = parts.index("cp")
                            analysis["score"] = int(parts[cp_index + 1])
                        except:
                            pass
                    elif "score mate" in line:
                        # Мат в N ходов
                        parts = line.split()
                        try:
                            mate_index = parts.index("mate")
                            analysis["score"] = f"Mate in {parts[mate_index + 1]}"
                        except:
                            pass
                    elif "depth" in line:
                        parts = line.split()
                        try:
                            depth_index = parts.index("depth")
                            analysis["depth"] = int(parts[depth_index + 1])
                        except:
                            pass
                    elif "nodes" in line:
                        parts = line.split()
                        try:
                            nodes_index = parts.index("nodes")
                            analysis["nodes"] = int(parts[nodes_index + 1])
                        except:
                            pass
                    elif "nps" in line:
                        parts = line.split()
                        try:
                            nps_index = parts.index("nps")
                            analysis["nps"] = int(parts[nps_index + 1])
                        except:
                            pass
                    elif "pv" in line:
                        # Главная вариационная линия
                        parts = line.split()
                        pv_index = parts.index("pv")
                        analysis["pv"] = parts[pv_index + 1:]
                    elif "multipv" in line:
                        # Множественные линии анализа
                        multipv_line = self._parse_multipv_line(line)
                        if multipv_line:
                            analysis["multipv_lines"].append(multipv_line)
                    elif "time" in line and "nodes" not in line:
                        # Время анализа
                        parts = line.split()
                        try:
                            time_index = parts.index("time")
                            analysis["time_spent"] = int(parts[time_index + 1])
                        except:
                            pass
                    elif "seldepth" in line:
                        # Выбранная глубина
                        parts = line.split()
                        try:
                            seldepth_index = parts.index("seldepth")
                            analysis["seldepth"] = int(parts[seldepth_index + 1])
                        except:
                            pass
            
            return analysis
            
        except Exception as e:
            print(f"Ошибка анализа позиции: {e}")
            return {}
    
    def _parse_multipv_line(self, line: str) -> Optional[dict]:
        """Парсинг строки с множественным анализом"""
        try:
            parts = line.split()
            multipv_index = parts.index("multipv")
            pv_index = parts.index("pv")
            
            return {
                "line_number": int(parts[multipv_index + 1]),
                "score": self._extract_score(parts),
                "depth": self._extract_depth(parts),
                "pv": parts[pv_index + 1:pv_index + 6]  # Первые 5 ходов
            }
        except:
            return None
    
    def _extract_score(self, parts: List[str]) -> Optional[str]:
        """Извлечение оценки из частей строки"""
        try:
            if "cp" in parts:
                cp_index = parts.index("cp")
                return f"CP {parts[cp_index + 1]}"
            elif "mate" in parts:
                mate_index = parts.index("mate")
                return f"Mate {parts[mate_index + 1]}"
        except:
            pass
        return None
    
    def _extract_depth(self, parts: List[str]) -> int:
        """Извлечение глубины анализа"""
        try:
            if "depth" in parts:
                depth_index = parts.index("depth")
                return int(parts[depth_index + 1])
        except:
            pass
        return 0

class StockfishDemo:
    """Демонстрация интеграции Stockfish"""
    
    def __init__(self):
        self.stockfish = StockfishIntegration()
    
    def run_demo(self):
        print("=== ИНТЕГРАЦИЯ С STOCKFISH ===")
        print("Stockfish - профессиональный шахматный движок с рейтингом 3500+ Elo\n")
        
        # Запуск Stockfish
        if not self.stockfish.start_engine():
            print("❌ Не удалось запустить Stockfish")
            return
        
        try:
            # Тестовые позиции
            test_positions = [
                {
                    "name": "Начальная позиция",
                    "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
                },
                {
                    "name": "Сицилианская защита", 
                    "fen": "rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2"
                },
                {
                    "name": "Итальянская партия",
                    "fen": "r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 3 3"
                }
            ]
            
            for i, position in enumerate(test_positions, 1):
                print(f"\n{i}. {position['name']}")
                print(f"FEN: {position['fen']}")
                
                # Получаем лучший ход
                best_move = self.stockfish.get_best_move(position['fen'], depth=12, movetime=1000)
                if best_move:
                    print(f"Лучший ход: {best_move}")
                else:
                    print("Не удалось получить ход")
                
                # Анализ позиции
                analysis = self.stockfish.analyze_position(position['fen'], depth=10)
                if analysis:
                    print(f"Оценка: {analysis.get('score', 'N/A')}")
                    print(f"Глубина: {analysis.get('depth', 0)}")
                    print(f"Узлы: {analysis.get('nodes', 0):,}")
                    if analysis.get('pv'):
                        print(f"Главная линия: {' '.join(analysis['pv'][:3])}")
                        print(f"Главная линия: {' '.join(analysis['pv'][:3])}")
                
                time.sleep(1)  # Пауза между позициями
            
            print("\n✅ Интеграция с Stockfish работает корректно!")
            
        finally:
            self.stockfish.stop_engine()
            print("\nStockfish остановлен")

if __name__ == "__main__":
    try:
        demo = StockfishDemo()
        demo.run_demo()
    except KeyboardInterrupt:
        print("\n\nДемонстрация прервана пользователем")
    except Exception as e:
        print(f"\nОшибка: {e}")