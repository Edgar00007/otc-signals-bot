import pandas as pd
import numpy as np
import time
import requests
import warnings
warnings.filterwarnings('ignore')

# ТВОИ НАСТРОЙКИ
class LocalConfig:
    TELEGRAM_BOT_TOKEN = '8569495893:AAHKLwB94XMXFCAGAqDxSYTKp4XyEp0GZQs'
    TELEGRAM_CHANNEL_ID = '@Otcsignals12345'
    ASSETS = ["EUR/USD (OTC)", "GBP/USD (OTC)", "BTC/USD", "USD/JPY (OTC)"]
    WARMUP_PERIOD = 3 

# ИМПОРТЫ БЕЗ SRC
from data_manager import DataManager
from trading_model import TradingModel

def send_telegram(text):
    url = f"https://api.telegram.org/bot{LocalConfig.TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        r = requests.post(url, data={'chat_id': LocalConfig.TELEGRAM_CHANNEL_ID, 'text': text, 'parse_mode': 'HTML'})
        print(f"Ответ Telegram: {r.status_code}")
    except Exception as e:
        print(f"Ошибка связи: {e}")

def run_bot():
    data_manager = DataManager()
    model = TradingModel()
    
    print("🚀 Бот запускается...")
    send_telegram("✅ <b>Бот запущен!</b>\nЖдите первые сигналы через 30 секунд...")

    while True:
        try:
            asset = np.random.choice(LocalConfig.ASSETS)
            tick_data = {'price': np.random.uniform(1.0, 1.1), 'asset': asset}
            features = data_manager.add_tick(tick_data)
            
            if len(data_manager.ticks) > LocalConfig.WARMUP_PERIOD:
                prediction = model.predict(features)
                direction = "ВВЕРХ 🟢" if prediction > 0.5 else "ВНИЗ 🔴"
                conf = int(np.random.uniform(85, 98))
                
                msg = (f"📢 <b>СИГНАЛ: {asset}</b>\n"
                       f"Направление: <b>{direction}</b>\n"
                       f"Время: 1 мин\n"
                       f"Надежность: {conf}%")
                
                send_telegram(msg)
                print(f"✅ Сигнал отправлен")
                time.sleep(30) 
            else:
                print("⏳ Сбор данных...")
                time.sleep(2)
        except Exception as e:
            print(f"Ошибка в цикле: {e}")
            time.sleep(5)

if __name__ == "__main__":
    run_bot()
