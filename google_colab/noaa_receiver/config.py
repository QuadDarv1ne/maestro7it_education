"""
Конфигурация проекта NOAA APT Receiver
"""

import os
from pathlib import Path
from typing import Optional
import yaml


class Config:
    """Класс конфигурации с поддержкой YAML файлов"""
    
    DEFAULT_CONFIG = {
        "sdr": {
            "sample_rate": 2.4e6,
            "center_freq": 137.62e6,
            "gain": 40,
            "ppm_correction": 0,
            "record_iq": True,
            "iq_format": "complex64",
        },
        "decoder": {
            "carrier_freq": 2400,
            "line_rate": 2,
            "pixels_per_line": 4160,
            "audio_sample_rate": 20800,
        },
        "filters": {
            "bandpass_low": 2300,
            "bandpass_high": 2500,
            "filter_order": 5,
            "use_fir": True,
            "fir_taps": 101,
        },
        "image": {
            "apply_denoising": True,
            "denoise_strength": 0.5,
            "apply_geocorrection": True,
            "output_format": "png",
            "colormap": "gray",
        },
        "visualization": {
            "plot_spectrum": True,
            "plot_waterfall": True,
            "plot_signal": True,
            "dpi": 150,
            "figsize": [12, 8],
        },
        "scheduler": {
            "min_elevation": 10,
            "location": {
                "latitude": 55.7558,
                "longitude": 37.6173,
                "altitude": 150,
            },
        },
        "telegram": {
            "enabled": False,
            "bot_token": "",
            "chat_id": "",
        },
        "logging": {
            "level": "INFO",
            "file": "noaa_receiver.log",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
        "output": {
            "directory": "./output",
            "save_iq": True,
            "save_images": True,
            "save_plots": True,
        },
    }
    
    def __init__(self, config_path: Optional[str] = None):
        self.config = self.DEFAULT_CONFIG.copy()
        
        if config_path and os.path.exists(config_path):
            self.load(config_path)
    
    def load(self, path: str) -> None:
        """Загрузка конфигурации из YAML файла"""
        with open(path, 'r', encoding='utf-8') as f:
            user_config = yaml.safe_load(f)
        
        if user_config:
            self._merge_config(user_config)
    
    def _merge_config(self, user_config: dict) -> None:
        """Рекурсивное слияние конфигураций"""
        for key, value in user_config.items():
            if key in self.config and isinstance(value, dict):
                self.config[key].update(value)
            else:
                self.config[key] = value
    
    def save(self, path: str) -> None:
        """Сохранение конфигурации в YAML файл"""
        with open(path, 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
    
    def get(self, *keys, default=None):
        """Получение значения по цепочке ключей"""
        value = self.config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value
    
    @property
    def sample_rate(self) -> float:
        return self.config["sdr"]["sample_rate"]
    
    @property
    def center_freq(self) -> float:
        return self.config["sdr"]["center_freq"]
    
    @property
    def gain(self) -> int:
        return self.config["sdr"]["gain"]
    
    @property
    def ppm_correction(self) -> float:
        return self.config["sdr"]["ppm_correction"]
    
    @property
    def output_dir(self) -> Path:
        return Path(self.config["output"]["directory"])
