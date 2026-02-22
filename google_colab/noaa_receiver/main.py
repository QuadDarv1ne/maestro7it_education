"""
NOAA APT Receiver - Главный пайплайн

Полный цикл приёма и обработки изображений с погодных спутников NOAA.

Использование:
    python main.py capture --duration 600    # Захват сигнала
    python main.py decode --iq file.bin      # Декодирование IQ-файла
    python main.py schedule                  # Расписание проходов
    python main.py full                      # Полный цикл
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

from .config import Config
from .logger import setup_logger, get_logger
from .rtl_sdr import RTLSDRInterface
from .decoder import NOAADecoder
from .visualizer import SignalVisualizer
from .image_processor import ImageProcessor
from .satellite_tracker import SatelliteTracker
from .telegram_bot import TelegramNotifier, SimpleTelegramBot


class NOAAReceiverPipeline:
    """
    Главный класс пайплайна NOAA APT Receiver
    """
    
    def __init__(self, config_path: str = None):
        self.config = Config(config_path)
        self.logger = setup_logger(
            name="noaa_receiver",
            level=self.config.get("logging", "level", default="INFO"),
            log_file=self.config.get("logging", "file", default=None),
            log_format=self.config.get("logging", "format", default=None),
        )
        
        # Инициализация компонентов
        self.sdr = RTLSDRInterface(self.config)
        self.decoder = NOAADecoder(self.config)
        self.visualizer = SignalVisualizer(self.config)
        self.image_processor = ImageProcessor(self.config)
        self.tracker = SatelliteTracker(self.config)
        
        # Telegram (опционально)
        self.telegram = None
        if self.config.get("telegram", "enabled", default=False):
            token = self.config.get("telegram", "bot_token", default="")
            chat_id = self.config.get("telegram", "chat_id", default="")
            if token and chat_id:
                self.telegram = SimpleTelegramBot(token, chat_id)
        
        # Создание директории для выходных файлов
        self.output_dir = self.config.output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger.info("🛰️  NOAA APT Receiver инициализирован")
    
    def capture(
        self,
        duration: float = 600,
        frequency: float = None,
        save_iq: bool = True,
    ) -> str:
        """
        Захват сигнала со спутника
        
        Args:
            duration: Длительность захвата (сек)
            frequency: Частота (Гц)
            save_iq: Сохранять IQ-данные
        
        Returns:
            Путь к IQ-файлу
        """
        self.logger.info("=" * 60)
        self.logger.info("📡 ЗАХВАТ СИГНАЛА NOAA APT")
        self.logger.info("=" * 60)
        
        # Подключение к SDR
        if not self.sdr.connect():
            self.logger.warning("Работа в режиме симуляции")
        
        # Частота по умолчанию
        if frequency is None:
            frequency = self.config.center_freq
        
        self.logger.info(f"Частота: {frequency/1e6:.3f} MHz")
        self.logger.info(f"Длительность: {duration} сек ({duration/60:.1f} мин)")
        
        # Захват
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        iq_file = self.output_dir / f"iq_{timestamp}_{frequency/1e6:.3f}MHz.bin"
        
        iq_data = self.sdr.capture(
            duration=duration,
            output_file=str(iq_file) if save_iq else None,
        )
        
        # Визуализация
        if self.config.get("visualization", "plot_spectrum", default=True):
            self.logger.info("📊 Создание визуализаций...")
            viz_dir = self.output_dir / "visualizations"
            self.visualizer.plot_all(
                iq_data,
                self.config.sample_rate,
                output_dir=str(viz_dir),
                prefix=f"{timestamp}_",
            )
        
        self.sdr.close()
        
        self.logger.info(f"✅ Захват завершён: {iq_file}")
        
        return str(iq_file)
    
    def decode(
        self,
        iq_file: str = None,
        iq_data = None,
        save_image: bool = True,
        apply_enhancement: bool = True,
    ) -> str:
        """
        Декодирование IQ-данных в изображение
        
        Args:
            iq_file: Путь к IQ-файлу
            iq_data: IQ-данные (альтернатива файлу)
            save_image: Сохранять изображение
            apply_enhancement: Применять улучшение
        
        Returns:
            Путь к изображению
        """
        self.logger.info("=" * 60)
        self.logger.info("🔄 ДЕКОДИРОВАНИЕ СИГНАЛА")
        self.logger.info("=" * 60)
        
        # Загрузка IQ-данных
        if iq_data is None:
            if not iq_file:
                raise ValueError("Необходимо указать iq_file или iq_data")
            self.logger.info(f"Загрузка IQ-файла: {iq_file}")
            iq_data = self.sdr.load_iq(iq_file)
        
        # Декодирование
        results = self.decoder.decode_full(iq_data, save_intermediate=True)
        
        # Улучшение изображения
        if apply_enhancement:
            self.logger.info("🎨 Улучшение изображения...")
            image = results['image']
            
            # Удаление шумов
            image = self.image_processor.denoise(image, method='median', strength=0.5)
            
            # Улучшение контраста
            image = self.image_processor.enhance_contrast(image, method='clahe')
            
            results['image'] = image
        
        # Сохранение
        if save_image:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_file = self.output_dir / f"noaa_apt_{timestamp}.png"
            
            metadata = {
                'timestamp': datetime.now().isoformat(),
                'lines': results['metadata'].get('lines', 0),
                'shape': str(results['image'].shape),
            }
            
            self.image_processor.save_image(
                results['image'],
                str(image_file),
                metadata=metadata,
            )
            
            # Сохранение отдельных каналов
            if results.get('channel1') is not None:
                ch1_file = self.output_dir / f"noaa_ch1_{timestamp}.png"
                self.image_processor.save_image(results['channel1'], str(ch1_file))
            
            if results.get('channel2') is not None:
                ch2_file = self.output_dir / f"noaa_ch2_{timestamp}.png"
                self.image_processor.save_image(results['channel2'], str(ch2_file))
            
            self.logger.info(f"✅ Изображение сохранено: {image_file}")
            
            # Уведомление в Telegram
            if self.telegram:
                self.telegram.send_pass_alert(
                    type('obj', (object,), {
                        'satellite_name': 'NOAA',
                        'aos': datetime.now(),
                        'los': datetime.now(),
                        'max_elevation': 45,
                        'duration_seconds': 600,
                    })()
                )
            
            return str(image_file)
        
        return None
    
    def schedule(self, days: int = 3, min_elevation: float = 15):
        """Показать расписание проходов"""
        self.tracker.print_schedule(days=days, min_elevation=min_elevation)
    
    def export_schedule(self, output_file: str, days: int = 7, format: str = 'text'):
        """Экспорт расписания"""
        self.tracker.export_schedule(output_file, days=days, format=format)
    
    def full(
        self,
        duration: float = 600,
        frequency: float = None,
    ) -> dict:
        """
        Полный цикл: захват + декодирование
        
        Returns:
            Словарь с результатами
        """
        self.logger.info("🚀 ЗАПУСК ПОЛНОГО ЦИКЛА")
        
        # Захват
        iq_file = self.capture(duration=duration, frequency=frequency)
        
        # Декодирование
        image_file = self.decode(iq_file=iq_file)
        
        return {
            'iq_file': iq_file,
            'image_file': image_file,
            'timestamp': datetime.now().isoformat(),
        }
    
    def close(self):
        """Очистка ресурсов"""
        self.sdr.close()
        self.logger.info("👋 NOAA Receiver остановлен")


def main():
    """Точка входа CLI"""
    parser = argparse.ArgumentParser(
        description="NOAA APT Satellite Receiver",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Команды")
    
    # Capture
    capture_parser = subparsers.add_parser("capture", help="Захват сигнала")
    capture_parser.add_argument("-d", "--duration", type=float, default=600,
                                help="Длительность захвата (сек)")
    capture_parser.add_argument("-f", "--frequency", type=float, default=None,
                                help="Частота (Гц)")
    capture_parser.add_argument("--no-save-iq", action="store_true",
                                help="Не сохранять IQ-данные")
    
    # Decode
    decode_parser = subparsers.add_parser("decode", help="Декодирование")
    decode_parser.add_argument("--iq", type=str, help="Путь к IQ-файлу")
    decode_parser.add_argument("--no-enhance", action="store_true",
                               help="Без улучшения изображения")
    
    # Schedule
    schedule_parser = subparsers.add_parser("schedule", help="Расписание проходов")
    schedule_parser.add_argument("--days", type=int, default=3,
                                 help="Дней прогноза")
    schedule_parser.add_argument("--min-elev", type=float, default=15,
                                 help="Мин. элевация (град)")
    
    # Export
    export_parser = subparsers.add_parser("export", help="Экспорт расписания")
    export_parser.add_argument("-o", "--output", type=str, required=True,
                               help="Выходной файл")
    export_parser.add_argument("--days", type=int, default=7,
                               help="Дней прогноза")
    export_parser.add_argument("--format", choices=['text', 'json', 'ics'],
                               default='text', help="Формат")
    
    # Full
    full_parser = subparsers.add_parser("full", help="Полный цикл")
    full_parser.add_argument("-d", "--duration", type=float, default=600,
                             help="Длительность захвата (сек)")
    full_parser.add_argument("-f", "--frequency", type=float, default=None,
                             help="Частота (Гц)")
    
    # Config
    config_parser = subparsers.add_parser("config", help="Управление конфигурацией")
    config_parser.add_argument("--show", action="store_true", help="Показать конфиг")
    config_parser.add_argument("--init", type=str, help="Создать конфиг")
    
    args = parser.parse_args()
    
    # Загрузка конфигурации
    config_path = "noaa_config.yaml"
    if Path(config_path).exists():
        pipeline = NOAAReceiverPipeline(config_path)
    else:
        pipeline = NOAAReceiverPipeline()
    
    try:
        if args.command == "capture":
            pipeline.capture(
                duration=args.duration,
                frequency=args.frequency,
                save_iq=not args.no_save_iq,
            )
        
        elif args.command == "decode":
            pipeline.decode(
                iq_file=args.iq,
                apply_enhancement=not args.no_enhance,
            )
        
        elif args.command == "schedule":
            pipeline.schedule(days=args.days, min_elevation=args.min_elev)
        
        elif args.command == "export":
            pipeline.export_schedule(
                output_file=args.output,
                days=args.days,
                format=args.format,
            )
        
        elif args.command == "full":
            pipeline.full(duration=args.duration, frequency=args.frequency)
        
        elif args.command == "config":
            if args.show:
                import yaml
                print(yaml.dump(pipeline.config.config, default_flow_style=False))
            elif args.init:
                pipeline.config.save(args.init)
                print(f"Конфигурация сохранена: {args.init}")
            else:
                parser.print_help()
        
        else:
            parser.print_help()
    
    finally:
        pipeline.close()


if __name__ == "__main__":
    main()
