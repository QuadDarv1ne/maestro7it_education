# ============================================================================
# utils/sound_manager.py
# ============================================================================

"""
Модуль: utils/sound_manager.py

Описание:
    Содержит класс SoundManager для управления звуковыми эффектами в шахматной игре.
    Обеспечивает воспроизведение звуков для различных игровых событий.
    
Возможности:
    - Воспроизведение звуков перемещения фигур
    - Воспроизведение звуков взятий
    - Воспроизведение звуков шаха и мата
    - Воспроизведение звуков победы и поражения
    - Управление громкостью звуков
    - Включение/выключение звука
    - Фоновая музыка
"""

import pygame
import os
import time
from typing import Dict, Optional
import logging


class SoundManager:
    """
    Менеджер звуковых эффектов для шахматной игры.
    """
    
    def __init__(self, sound_enabled: bool = True, music_enabled: bool = True, volume: float = 0.7):
        """
        Инициализация менеджера звуков.
        
        Параметры:
            sound_enabled (bool): Включены ли звуковые эффекты по умолчанию
            music_enabled (bool): Включена ли фоновая музыка по умолчанию
            volume (float): Громкость звуков (0.0 - 1.0)
        """
        self.sound_enabled = sound_enabled
        self.music_enabled = music_enabled
        self.volume = max(0.0, min(1.0, volume))
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self._initialized = False
        self.background_music = None
        self.sound_queue = []  # Очередь для предотвращения наложения звуков
        self.last_sound_time = 0  # Время последнего воспроизведения звука
        self.sound_cooldown = 0.1  # Минимальная задержка между звуками
        
        # Инициализируем систему звука
        self._init_sound_system()
        
    def _init_sound_system(self):
        """Инициализация системы звука pygame."""
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self._initialized = True
            logging.info("Sound system initialized successfully")
        except Exception as e:
            logging.warning(f"Failed to initialize sound system: {e}")
            self._initialized = False
            self.sound_enabled = False
            self.music_enabled = False
            
    def _load_sound(self, name: str, filename: str) -> Optional[pygame.mixer.Sound]:
        """
        Загрузка звукового файла.
        
        Параметры:
            name (str): Имя звука
            filename (str): Имя файла звука
            
        Возвращает:
            pygame.mixer.Sound: Загруженный звук или None при ошибке
        """
        if not self._initialized:
            return None
            
        try:
            # Путь к звуковым файлам
            sound_path = os.path.join(os.path.dirname(__file__), "..", "sounds", filename)
            if not os.path.exists(sound_path):
                # Если файл не найден, попробуем стандартные системные звуки
                logging.warning(f"Sound file not found: {sound_path}")
                return None
                
            sound = pygame.mixer.Sound(sound_path)
            sound.set_volume(self.volume)
            self.sounds[name] = sound
            return sound
        except Exception as e:
            logging.warning(f"Failed to load sound {filename}: {e}")
            return None
            
    def play_sound(self, sound_name: str):
        """
        Воспроизведение звукового эффекта.
        
        Параметры:
            sound_name (str): Имя звука для воспроизведения
        """
        if not self.sound_enabled or not self._initialized:
            return
            
        current_time = time.time()
        
        # Проверяем cooldown для предотвращения наложения звуков
        if current_time - self.last_sound_time < self.sound_cooldown:
            return
            
        try:
            if sound_name in self.sounds:
                # Останавливаем предыдущий звук того же типа, если он еще играет
                if sound_name in self.sound_queue:
                    self.sounds[sound_name].stop()
                
                self.sounds[sound_name].play()
                self.last_sound_time = current_time
                # Добавляем звук в очередь для отслеживания
                self.sound_queue.append(sound_name)
            else:
                logging.warning(f"Sound '{sound_name}' not found")
        except Exception as e:
            logging.warning(f"Failed to play sound '{sound_name}': {e}")

    def _create_soft_click_sound(self, duration: float) -> pygame.mixer.Sound:
        """
        Создание мягкого звука клика для интерфейса.
        
        Параметры:
            duration (float): Длительность в секундах
            
        Возвращает:
            pygame.mixer.Sound: Созданный звук
        """
        import numpy as np
        
        sample_rate = 22050
        frames = int(duration * sample_rate)
        arr = np.zeros((frames, 2))  # Стерео
        
        # Создаем более приятный звук с гармоническими обертонами
        for i in range(frames):
            t = i / sample_rate
            # Огибающая для плавного звучания
            envelope = np.exp(-t * 30)  # Быстрый спад для четкости
            if t < duration:
                # Комбинация частот для более приятного звука
                wave1 = np.sin(2 * np.pi * 440 * t)  # Основная частота (ля)
                wave2 = 0.5 * np.sin(2 * np.pi * 880 * t)  # Высокая частота (октава)
                wave3 = 0.3 * np.sin(2 * np.pi * 220 * t)  # Низкая частота (октава вниз)
                wave4 = 0.2 * np.sin(2 * np.pi * 1760 * t)  # Очень высокая частота
                wave = envelope * 4096 * (wave1 + wave2 + wave3 + wave4)
                arr[i][0] = wave  # Левый канал
                arr[i][1] = wave  # Правый канал
            
        return pygame.sndarray.make_sound(arr.astype(np.int16))

    def _create_tone_sound(self, frequency: int, duration: float) -> pygame.mixer.Sound:
        """
        Создание звукового сигнала заданной частоты и длительности.
        
        Параметры:
            frequency (int): Частота в Гц
            duration (float): Длительность в секундах
            
        Возвращает:
            pygame.mixer.Sound: Созданный звук
        """
        import numpy as np
        
        sample_rate = 22050
        frames = int(duration * sample_rate)
        arr = np.zeros((frames, 2))  # Стерео
        
        # Генерируем синусоидальную волну с огибающей для плавного звучания
        for i in range(frames):
            t = i / sample_rate
            # Огибающая для плавного нарастания и спада
            if t < duration * 0.1:  # Первые 10% времени - нарастание
                envelope = t / (duration * 0.1)
            elif t > duration * 0.9:  # Последние 10% времени - спад
                envelope = 1.0 - (t - duration * 0.9) / (duration * 0.1)
            else:  # Середина - максимальная громкость
                envelope = 1.0
                
            wave = envelope * 4096 * np.sin(2 * np.pi * frequency * t)
            arr[i][0] = wave  # Левый канал
            arr[i][1] = wave  # Правый канал
            
        return pygame.sndarray.make_sound(arr.astype(np.int16))

    def load_sounds(self):
        """Загрузка всех звуковых эффектов."""
        if not self._initialized:
            return
            
        # Загружаем стандартные системные звуки если файлы не найдены
        try:
            # Основные игровые звуки
            self.sounds["move"] = self._create_tone_sound(440, 0.15)  # Ля 440 Гц, 150 мс
            self.sounds["capture"] = self._create_tone_sound(220, 0.25)  # Ля 220 Гц, 250 мс
            self.sounds["check"] = self._create_tone_sound(880, 0.35)   # Ля 880 Гц, 350 мс
            self.sounds["checkmate"] = self._create_tone_sound(1760, 0.6)  # Ля 1760 Гц, 600 мс
            self.sounds["castle"] = self._create_tone_sound(330, 0.2)   # Ми 330 Гц, 200 мс
            self.sounds["promote"] = self._create_tone_sound(660, 0.4)  # Ми 660 Гц, 400 мс
            self.sounds["win"] = self._create_tone_sound(523, 0.5)     # До 523 Гц, 500 мс
            self.sounds["lose"] = self._create_tone_sound(196, 0.7)    # Соль 196 Гц, 700 мс
            self.sounds["draw"] = self._create_tone_sound(392, 0.4)    # Соль 392 Гц, 400 мс
            # Улучшенный звук кнопки - более приятный и мягкий
            self.sounds["button"] = self._create_soft_click_sound(0.1)
        except Exception as e:
            logging.warning(f"Failed to create tone sounds: {e}")
            
    def play_background_music(self):
        """
        Воспроизведение фоновой музыки.
        """
        if not self.music_enabled or not self._initialized:
            return
            
        try:
            # Используем файлы из папки soundtrack
            if self.background_music is None:
                soundtrack_path = os.path.join(os.path.dirname(__file__), "..", "soundtrack")
                if os.path.exists(soundtrack_path):
                    # Получаем список MP3 файлов
                    mp3_files = [f for f in os.listdir(soundtrack_path) if f.endswith('.mp3')]
                    if mp3_files:
                        # Выбираем случайный файл из доступных
                        import random
                        selected_file = random.choice(mp3_files)
                        self.background_music = os.path.join(soundtrack_path, selected_file)
                    else:
                        # Если нет MP3 файлов, создаем музыку программно
                        self.background_music = self._create_background_music()
                else:
                    # Если папка soundtrack не существует, создаем музыку программно
                    self.background_music = self._create_background_music()
            
            if self.background_music:
                pygame.mixer.music.load(self.background_music)
                pygame.mixer.music.set_volume(self.volume * 0.7)  # Меньше громкость для фона
                pygame.mixer.music.play(-1)  # Повторять бесконечно
        except Exception as e:
            logging.warning(f"Failed to play background music: {e}")
            
    def _create_background_music(self):
        """
        Создание фоновой музыки программно.
        
        Возвращает:
            str: Путь к временному файлу с музыкой
        """
        import numpy as np
        import tempfile
        
        try:
            # Создаем простую мелодию
            sample_rate = 22050
            duration = 30  # 30 секунд
            frames = int(duration * sample_rate)
            arr = np.zeros(frames)
            
            # Основная мелодия (простая арпеджио)
            notes = [261.63, 329.63, 392.00, 523.25]  # До, Ми, Соль, До
            note_duration = sample_rate // 2  # Полсекунды на ноту
            
            for i in range(len(notes)):
                start = i * note_duration
                end = min(start + note_duration, frames)
                freq = notes[i % len(notes)]
                
                # Создаем огибающую для плавного звучания
                for j in range(start, end):
                    t = (j - start) / note_duration
                    envelope = np.sin(np.pi * t)  # Плавное нарастание и спад
                    wave = envelope * 2048 * np.sin(2 * np.pi * freq * j / sample_rate)
                    arr[j] = wave
                    
            # Преобразуем в стерео
            stereo_arr = np.zeros((frames, 2))
            stereo_arr[:, 0] = arr  # Левый канал
            stereo_arr[:, 1] = arr  # Правый канал
            
            # Сохраняем во временный файл
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            temp_file.close()
            
            # Создаем WAV файл
            import wave
            wav_file = wave.open(temp_file.name, 'w')
            wav_file.setparams((2, 2, sample_rate, frames, 'NONE', 'not compressed'))
            
            # Преобразуем в 16-битный формат
            stereo_arr = stereo_arr.astype(np.int16)
            wav_file.writeframes(stereo_arr.tobytes())
            wav_file.close()
            
            return temp_file.name
        except Exception as e:
            logging.warning(f"Failed to create background music: {e}")
            return None
            
    def stop_background_music(self):
        """
        Остановка фоновой музыки.
        """
        try:
            pygame.mixer.music.stop()
        except Exception as e:
            logging.warning(f"Failed to stop background music: {e}")
            
    def set_volume(self, volume: float):
        """
        Установка громкости всех звуков.
        
        Параметры:
            volume (float): Громкость (0.0 - 1.0)
        """
        self.volume = max(0.0, min(1.0, volume))
        try:
            pygame.mixer.music.set_volume(self.volume * 0.7)
        except Exception:
            pass
            
        for sound in self.sounds.values():
            try:
                sound.set_volume(self.volume)
            except Exception:
                pass
                
    def toggle_sound(self):
        """Переключение состояния звуковых эффектов."""
        self.sound_enabled = not self.sound_enabled
        return self.sound_enabled
        
    def toggle_music(self):
        """Переключение состояния фоновой музыки."""
        self.music_enabled = not self.music_enabled
        if self.music_enabled:
            self.play_background_music()
        else:
            self.stop_background_music()
        return self.music_enabled
        
    def is_sound_enabled(self) -> bool:
        """
        Проверка, включены ли звуковые эффекты.
        
        Возвращает:
            bool: True если звуковые эффекты включены
        """
        return self.sound_enabled and self._initialized
        
    def is_music_enabled(self) -> bool:
        """
        Проверка, включена ли фоновая музыка.
        
        Возвращает:
            bool: True если фоновая музыка включена
        """
        return self.music_enabled and self._initialized
    
    def cleanup(self):
        """
        Очистка всех звуковых ресурсов.
        """
        try:
            # Останавливаем фоновую музыку
            self.stop_background_music()
            
            # Останавливаем все воспроизводимые звуки
            pygame.mixer.stop()
            
            # Освобождаем звуковые файлы
            for sound in self.sounds.values():
                try:
                    sound.stop()
                except:
                    pass
            self.sounds.clear()
            
            # Выгружаем звуковую систему
            pygame.mixer.quit()
            
        except Exception as e:
            logging.warning(f"Error during sound cleanup: {e}")
    
    def __del__(self):
        """
        Деструктор для автоматической очистки ресурсов.
        """
        try:
            self.cleanup()
        except:
            pass

