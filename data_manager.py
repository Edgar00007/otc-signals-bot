import pandas as pd  # Исправлено: с маленькой буквы
import numpy as np
from datetime import datetime
import logging

# Попытка импорта настроек
try:
    from settings import Config
except ImportError:
    # Заглушка, если файл settings.py не найден
    class Config:
        MAX_TICK_HISTORY = 1000

logger = logging.getLogger(__name__)

class DataManager:
    def __init__(self):
        # Инициализируем структуру данных
        self.columns = ['timestamp', 'price', 'volume', 'asset']
        self.ticks = pd.DataFrame(columns=self.columns)
        
        # Лимит истории (берем из настроек или ставим 1000 по умолчанию)
        self.max_history = getattr(Config, 'MAX_TICK_HISTORY', 1000)
        
    def add_tick(self, tick_data):
        """
        Добавляет новые данные о цене в таблицу.
        tick_data должен содержать: 'price', 'asset' и опционально 'volume'
        """
        try:
            # Создаем новую строку данных
            new_row = {
                'timestamp': datetime.now(),
                'price': tick_data.get('price'),
                'asset': tick_data.get('asset'),
                'volume': tick_data.get('volume', 0)
            }
            
            # Превращаем в DataFrame
            new_tick = pd.DataFrame([new_row])
            
            # Добавляем к основной базе данных
            if self.ticks.empty:
                self.ticks = new_tick
            else:
                self.ticks = pd.concat([self.ticks, new_tick], ignore_index=True)
            
            # ОГРАНИЧЕНИЕ ПАМЯТИ: оставляем только последние N записей
            # Это критично для работы Dashboard, чтобы бот не "падал"
            if len(self.ticks) > self.max_history:
                self.ticks = self.ticks.tail(self.max_history).reset_index(drop=True)
                
            return new_tick
            
        except Exception as e:
            logger.error(f"Ошибка при сохранении данных (DataManager): {e}")
            return None

    def get_data_for_asset(self, asset):
        """Возвращает историю только по конкретному активу (для графиков)"""
        return self.ticks[self.ticks['asset'] == asset]

    def get_last_price(self, asset):
        """Возвращает последнюю цену актива"""
        asset_data = self.get_data_for_asset(asset)
        if not asset_data.empty:
            return asset_data.iloc[-1]['price']
        return None

    def clear_history(self):
        """Полная очистка данных"""
        self.ticks = pd.DataFrame(columns=self.columns)
        logger.info("История котировок очищена.")
