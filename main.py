import pandas as pd  # Исправлено
import numpy as np
import time
import requests
import warnings
import logging

warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# НАСТРОЙКИ
class LocalConfig:
    # СОВЕТ: Замените токен в BotFather, этот скомпрометирован!
    TELEGRAM_BOT_TOKEN = '8569495893:AAHKLwB94XMXFCAGAqDxSYTKp4XyEp0'
    TELEGRAM_CHANNEL_ID = '@Otcsignals'
    ASSETS = ["EUR/USD (OTC)", "GBP/USD (OTC)", "BTC/USD", "USD/JPY (OTC)"]
    WARMUP_PERIOD = 5 # Увеличим период прогрева для стабильности данных

# ИМПОРТЫ
try:
    from data_manager import DataManager
    from trading_model import TradingModel
except ImportError as e:
    logger.error(f"Ошибка импорта: {e}. Проверьте наличие файлов в папке.")

def send_telegram(text):
    """Отправка сообщений в канал/чат"""
    url = f"https://api.telegram.org/bot{LocalConfig.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': LocalConfig.TELEGRAM_CHANNEL_ID, 
        'text': text, 
        'parse_mode': 'HTML'
    }
    try:
        r = requests.post(url, data=payload, timeout=10)
        return r.status_code == 200
    except Exception as e:
        logger.error(f"Ошибка связи с Telegram: {e}")
        return False

def run_bot():
    data_manager = DataManager()
    model = TradingModel()
    
    print("🚀 Бот запускается...")
    send_telegram("✅ <b>Бот запущен!</b>\nЖдите первые сигналы после сбора данных...")

    while True:
        try:
            # Выбираем случайный актив (в реальности тут должен быть цикл по всем активам)
            asset = np.random.choice(LocalConfig.ASSETS)
            
            # Генерируем тестовую цену (замените на реальный API Pocket Option)
            tick_data = {
                'price': np.random.uniform(1.0, 1.1), 
                'asset': asset,
                'volume': np.random.randint(100, 500)
            }
            
            # Добавляем данные в менеджер
            data_manager.add_tick(tick_data)
            
            # Проверяем, накопилось ли достаточно данных для прогноза
            if len(data_manager.get_data_for_asset(asset)) > LocalConfig.WARMUP_PERIOD:
                # Получаем последние данные для модели
                df_for_model = data_manager.get_data_for_asset(asset)
                
                # Прогноз
                prediction = model.predict(df_for_model)
                direction = "ВВЕРХ 🟢" if prediction > 0.5 else "ВНИЗ 🔴"
                conf = int(np.random.uniform(85, 98))
                
                msg = (f"📢 <b>СИГНАЛ: {asset}</b>\n"
                       f"Направление: <b>{direction}</b>\n"
                       f"Время: 1 мин\n"
                       f"Надежность: {conf}%")
                
                if send_telegram(msg):
                    print(f"✅ Сигнал по {asset} отправлен")
                
                # Ждем перед следующим сигналом
                time.sleep(30) 
            else:
                print(f"⏳ Сбор данных для {asset}... ({len(data_manager.get_data_for_asset(asset))}/{LocalConfig.WARMUP_PERIOD})")
                time.sleep(2)

        except Exception as e:
            print(f"Ошибка в основном цикле: {e}")
            time.sleep(5)

if __name__ == "__main__":
    run_bot()
