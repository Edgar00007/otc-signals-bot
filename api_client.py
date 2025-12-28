import time  # Исправлено: с маленькой буквы
import requests
import json
import numpy as np
from datetime import datetime
import logging

# Предполагаем, что settings.py находится в папке config
try:
    from config.settings import Config
except ImportError:
    # Запасной вариант, если структура папок иная
    class Config:
        API_DEMO_URL = "https://demo.api.pocketoption.com"
        API_REAL_URL = "https://api.pocketoption.com"
        ASSETS = ["EURUSD", "GBPUSD", "BTCUSD", "ETHUSD"]

logger = logging.getLogger(__name__)

class PocketOptionClient:
    def __init__(self, demo_mode=True):
        self.demo_mode = demo_mode
        self.balance = 1000.0  # Начальный баланс для симуляции
        
        # Безопасная проверка наличия Config
        self.base_url = getattr(Config, 'API_DEMO_URL', '') if demo_mode else getattr(Config, 'API_REAL_URL', '')
        
        self.connected = False
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Генерация базовых цен для симуляции Dashboard
        self.price_history = {}
        assets = getattr(Config, 'ASSETS', ["EURUSD", "BTCUSD"])
        for asset in assets:
            if "USD" in asset and "BTC" not in asset and "ETH" not in asset:
                self.price_history[asset] = 1.0 + np.random.uniform(0.05, 0.3)
            elif "BTC" in asset:
                self.price_history[asset] = 50000.0 + np.random.uniform(-5000, 5000)
            elif "ETH" in asset:
                self.price_history[asset] = 3000.0 + np.random.uniform(-300, 300)
            else:
                self.price_history[asset] = 100.0 + np.random.uniform(-10, 10)
        
    def connect(self):
        """Эмуляция подключения к API"""
        logger.info("Connecting to Pocket Option API...")
        try:
            time.sleep(1) # Имитация задержки сети
            self.connected = True
            logger.info("Connected successfully to Pocket Option API!")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to API: {e}")
            return False
            
    def get_current_price(self, asset):
        """Получение текущей цены (симуляция для Dashboard)"""
        if not self.connected:
            logger.warning("Not connected to API. Cannot get price.")
            return None
            
        current_price = self.price_history.get(asset, 1.0)
        
        # Реалистичное движение цены
        if "BTC" in asset or "ETH" in asset:
            change = np.random.normal(0, 0.002) * current_price
        else:
            change = np.random.normal(0, 0.0002) * current_price
            
        new_price = current_price + change
        self.price_history[asset] = new_price
        
        return {
            'asset': asset,
            'price': round(new_price, 5),
            'timestamp': datetime.now(),
            'volume': np.random.randint(100, 1000)
        }
        
    def place_trade(self, asset, amount, direction, expiry):
        """Размещение сделки (симуляция)"""
        if not self.connected:
            return {'success': False, 'error': 'Not connected'}
            
        logger.info(f"Placing trade: {asset}, {direction}, ${amount}")
        time.sleep(0.5)
        
        # Логика выигрыша
        win_chance = 0.65 if self.demo_mode else 0.55
        win = np.random.random() < win_chance
        
        if win:
            payout = amount * 0.92
            self.balance += payout
            outcome = "win"
        else:
            payout = -amount
            self.balance += payout
            outcome = "loss"
            
        return {
            'success': True,
            'outcome': outcome,
            'payout': round(payout, 2),
            'balance': round(self.balance, 2)
        }
        
    def get_balance(self):
        """Возвращает текущий баланс"""
        if not self.connected:
            return 0.0
        return round(self.balance, 2)
        
    def disconnect(self):
        """Отключение"""
        self.connected = False
        self.session.close()
        logger.info("Disconnected from API.")
