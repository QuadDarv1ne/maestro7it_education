#!/usr/bin/env python3
"""
Интеграция анализатора партий с Pygame интерфейсом
Добавляет функции анализа в графический интерфейс
"""

import pygame
import sys
from game_analyzer import GameAnalyzer, MoveQuality

class AnalysisIntegration:
    """Интеграция анализатора с Pygame"""
    
    def __init__(self, chess_engine_wrapper):
        self.analyzer = GameAnalyzer()
        self.engine = chess_engine_wrapper
        self.analysis_results = None
        self.current_move_index = 0
        
    def analyze_current_game(self, player_color="white"):
        """Анализирует текущую партию"""
        if not hasattr(self.engine, 'move_history') or not self.engine.move_history:
            print("❌ Нет ходов для анализа")
            return None
            
        moves = [move['algebraic'] for move in self.engine.move_history]
        self.analysis_results = self.analyzer.analyze_game(moves, player_color)
        self.current_move_index = 0
        
        print("✅ Анализ текущей партии завершен!")
        return self.analysis_results
    
    def get_move_analysis(self, move_index):
        """Получает анализ конкретного хода"""
        if not self.analysis_results or move_index >= len(self.analysis_results['move_analyses']):
            return None
        return self.analysis_results['move_analyses'][move_index]
    
    def get_current_analysis(self):
        """Получает анализ текущего хода"""
        return self.get_move_analysis(self.current_move_index)
    
    def next_move_analysis(self):
        """Переходит к анализу следующего хода"""
        if (self.analysis_results and 
            self.current_move_index < len(self.analysis_results['move_analyses']) - 1):
            self.current_move_index += 1
            return True
        return False
    
    def prev_move_analysis(self):
        """Переходит к анализу предыдущего хода"""
        if self.analysis_results and self.current_move_index > 0:
            self.current_move_index -= 1
            return True
        return False
    
    def get_summary(self):
        """Получает сводку анализа"""
        if self.analysis_results:
            return self.analysis_results['summary']
        return None

class PygameAnalysisDisplay:
    """Отображение анализа в Pygame"""
    
    def __init__(self, screen, font, analysis_integration):
        self.screen = screen
        self.font = font
        self.analysis = analysis_integration
        self.visible = False
        
    def show_analysis(self):
        """Показывает окно анализа"""
        if not self.analysis.analysis_results:
            # Запускаем анализ текущей партии
            self.analysis.analyze_current_game()
            
        self.visible = True
        
    def hide_analysis(self):
        """Скрывает окно анализа"""
        self.visible = False
        
    def handle_event(self, event):
        """Обрабатывает события анализа"""
        if not self.visible:
            return False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.analysis.next_move_analysis()
            elif event.key == pygame.K_LEFT:
                self.analysis.prev_move_analysis()
            elif event.key == pygame.K_ESCAPE:
                self.hide_analysis()
                
        return True
    
    def draw(self):
        """Отрисовывает окно анализа"""
        if not self.visible or not self.analysis.analysis_results:
            return
            
        # Полупрозрачный оверлей
        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(220)
        overlay.fill((0, 0, 30))
        self.screen.blit(overlay, (0, 0))
        
        # Основная панель
        panel_width = 700
        panel_height = 500
        panel_x = (800 - panel_width) // 2
        panel_y = (600 - panel_height) // 2
        
        pygame.draw.rect(self.screen, (40, 40, 60), (panel_x, panel_y, panel_width, panel_height))
        pygame.draw.rect(self.screen, (100, 150, 200), (panel_x, panel_y, panel_width, panel_height), 3)
        
        # Заголовок
        title = self.font.render("АНАЛИЗ ПАРТИИ", True, (255, 255, 255))
        title_rect = title.get_rect(center=(panel_x + panel_width//2, panel_y + 30))
        self.screen.blit(title, title_rect)
        
        # Навигация
        nav_text = self.font.render("←/→ Навигация по ходам  ESC - Закрыть", True, (200, 200, 200))
        nav_rect = nav_text.get_rect(center=(panel_x + panel_width//2, panel_y + 60))
        self.screen.blit(nav_text, nav_rect)
        
        # Текущий ход
        current_analysis = self.analysis.get_current_analysis()
        if current_analysis:
            # Информация о ходе
            move_info = f"Ход {self.analysis.current_move_index + 1}: {current_analysis.move}"
            move_text = self.font.render(move_info, True, (255, 255, 100))
            self.screen.blit(move_text, (panel_x + 20, panel_y + 100))
            
            # Качество хода
            quality_colors = {
                MoveQuality.BEST: (100, 255, 100),
                MoveQuality.GOOD: (150, 255, 150),
                MoveQuality.OKAY: (255, 255, 100),
                MoveQuality.MISTAKE: (255, 150, 100),
                MoveQuality.BLUNDER: (255, 100, 100)
            }
            
            quality_text = self.font.render(
                f"Качество: {current_analysis.quality.value}", 
                True, 
                quality_colors.get(current_analysis.quality, (255, 255, 255))
            )
            self.screen.blit(quality_text, (panel_x + 20, panel_y + 130))
            
            # Оценки
            eval_text = self.font.render(
                f"Оценка вашего хода: {current_analysis.played_move_eval}", 
                True, 
                (200, 200, 255)
            )
            self.screen.blit(eval_text, (panel_x + 20, panel_y + 160))
            
            eval_text2 = self.font.render(
                f"Оценка лучшего хода: {current_analysis.best_move_eval}", 
                True, 
                (200, 255, 200)
            )
            self.screen.blit(eval_text2, (panel_x + 20, panel_y + 185))
            
            # Рекомендация
            rec_lines = self._wrap_text(current_analysis.recommendation, 60)
            for i, line in enumerate(rec_lines[:3]):  # Максимум 3 строки
                rec_text = self.font.render(line, True, (255, 200, 150))
                self.screen.blit(rec_text, (panel_x + 20, panel_y + 220 + i * 25))
            
            # Тактический паттерн
            if current_analysis.tactical_pattern != "none":
                pattern_text = self.font.render(
                    f"Паттерн: {current_analysis.tactical_pattern}", 
                    True, 
                    (255, 180, 255)
                )
                self.screen.blit(pattern_text, (panel_x + 20, panel_y + 310))
            
            # Позиционное преимущество
            if current_analysis.positional_advantage != "none":
                pos_text = self.font.render(
                    f"Преимущество: {current_analysis.positional_advantage}", 
                    True, 
                    (180, 255, 255)
                )
                self.screen.blit(pos_text, (panel_x + 20, panel_y + 340))
        
        # Статистика
        stats = self.analysis.analysis_results['statistics']
        if stats:
            stats_y = panel_y + 380
            stats_text = self.font.render("СТАТИСТИКА:", True, (255, 255, 255))
            self.screen.blit(stats_text, (panel_x + 20, stats_y))
            
            stats_lines = [
                f"Всего ходов: {stats['total_analyzed']}",
                f"Лучшие: {stats['best_moves']} ({stats['best_moves']/stats['total_analyzed']*100:.0f}%)",
                f"Ошибки: {stats['mistakes'] + stats['blunders']} ({(stats['mistakes'] + stats['blunders'])/stats['total_analyzed']*100:.0f}%)",
                f"Средняя разница: {stats['average_eval_difference']}"
            ]
            
            for i, line in enumerate(stats_lines):
                stat_text = self.font.render(line, True, (200, 200, 200))
                self.screen.blit(stat_text, (panel_x + 20, stats_y + 30 + i * 25))
    
    def _wrap_text(self, text, max_chars):
        """Разбивает текст на строки по максимальному количеству символов"""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line + word) <= max_chars:
                current_line += word + " "
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "
        
        if current_line:
            lines.append(current_line.strip())
            
        return lines

def integrate_analysis_with_pygame(chess_engine_wrapper):
    """Интегрирует анализатор с Pygame интерфейсом"""
    
    # Создаем интеграцию
    analysis_integration = AnalysisIntegration(chess_engine_wrapper)
    
    # Добавляем горячие клавиши
    def add_analysis_shortcuts(event, game_state):
        """Добавляет горячие клавиши анализа"""
        if event.type == pygame.KEYDOWN:
            # Ctrl+A - Анализ партии
            if event.key == pygame.K_a and pygame.key.get_mods() & pygame.KMOD_CTRL:
                print("🔍 Запуск анализа партии...")
                analysis_integration.analyze_current_game()
                return True
                
            # Ctrl+N - Следующий ход в анализе
            elif event.key == pygame.K_n and pygame.key.get_mods() & pygame.KMOD_CTRL:
                analysis_integration.next_move_analysis()
                return True
                
            # Ctrl+P - Предыдущий ход в анализе
            elif event.key == pygame.K_p and pygame.key.get_mods() & pygame.KMOD_CTRL:
                analysis_integration.prev_move_analysis()
                return True
    
    # Добавляем функции в игровой объект
    chess_engine_wrapper.analysis_integration = analysis_integration
    chess_engine_wrapper.add_analysis_shortcuts = add_analysis_shortcuts
    
    print("✅ Система анализа интегрирована в Pygame интерфейс")
    print("⌨️  Горячие клавиши:")
    print("   Ctrl+A - Анализ текущей партии")
    print("   Ctrl+N - Следующий ход в анализе")
    print("   Ctrl+P - Предыдущий ход в анализе")
    print("   ←/→ - Навигация в окне анализа")
    
    return analysis_integration

# Демонстрация интеграции
def demonstrate_analysis_integration():
    """Демонстрирует интеграцию анализатора"""
    print("=== ДЕМОНСТРАЦИЯ ИНТЕГРАЦИИ АНАЛИЗАТОРА ===")
    
    # Создаем тестовую интеграцию
    class MockEngine:
        def __init__(self):
            self.move_history = [
                {'algebraic': 'e4'}, {'algebraic': 'e5'},
                {'algebraic': 'Nf3'}, {'algebraic': 'Nc6'},
                {'algebraic': 'Bb5'}, {'algebraic': 'a6'}
            ]
    
    mock_engine = MockEngine()
    analysis_integration = integrate_analysis_with_pygame(mock_engine)
    
    # Тестируем функции
    print("\n🔍 ТЕСТИРОВАНИЕ ФУНКЦИЙ:")
    
    # Анализируем партию
    results = analysis_integration.analyze_current_game("white")
    if results:
        print("✅ Анализ завершен успешно")
        print(f"   Проанализировано ходов: {results['statistics']['total_analyzed']}")
        print(f"   Средняя разница в оценке: {results['statistics']['average_eval_difference']}")
        
        # Получаем анализ конкретного хода
        move_analysis = analysis_integration.get_move_analysis(0)
        if move_analysis:
            print(f"   Первый ход: {move_analysis.move}")
            print(f"   Качество: {move_analysis.quality.value}")
    
    print("\n🎯 ПРЕИМУЩЕСТВА ИНТЕГРАЦИИ:")
    advantages = [
        "Профессиональный анализ качества ходов",
        "Подробные рекомендации по улучшению",
        "Визуализация в графическом интерфейсе",
        "Навигация по ходам партии",
        "Статистика и сводка игры",
        "Горячие клавиши для удобства"
    ]
    
    for advantage in advantages:
        print(f"✅ {advantage}")
    
    print("\n" + "=" * 50)
    print("🎉 ИНТЕГРАЦИЯ АНАЛИЗАТОРА УСПЕШНО РЕАЛИЗОВАНА!")

if __name__ == "__main__":
    try:
        demonstrate_analysis_integration()
        print("\n\nНажмите Enter для завершения...")
        input()
    except KeyboardInterrupt:
        print("\n\nДемонстрация прервана пользователем")
    except Exception as e:
        print(f"\nОшибка: {e}")