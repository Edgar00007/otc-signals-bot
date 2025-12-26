import telebot
from telebot import types
import numpy as np
import time
import requests
import warnings
warnings.filterwarnings('ignore')

# Импорт твоих мозгов проекта
try:
    from data_manager import DataManager
from trading_model import TradingModel
except ImportError:
    print("Ошибка: папка 'src' должна быть рядом с этим файлом!")

# ================= НАСТРОЙКИ =================
TOKEN = '8569495893:AAHKLwB94XMXFCAGAqDxSYTKp4XyEp0GZQs'
bot = telebot.TeleBot(TOKEN)

# Список активов для кнопок
ASSETS = [
    "EUR/USD (OTC)", "GBP/USD (OTC)", "USD/JPY (OTC)", 
    "AUD/USD (OTC)", "BTC/USD", "ETH/USD (OTC)"
]

# Инициализация логики
data_manager = DataManager()
model = TradingModel()

# Функция для создания кнопок
def main_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(text=asset, callback_data=f"analyze_{asset}") for asset in ASSETS]
    markup.add(*buttons)
    return markup

# Приветствие при команде /start
@bot.message_message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id, 
        "<b>Добро пожаловать в OTC Master!</b>\n\nВыберите валютную пару ниже, чтобы получить мгновенный сигнал:", 
        parse_mode='HTML', 
        reply_markup=main_markup()
    )

# Обработка нажатия на кнопки
@bot.callback_query_handler(func=lambda call: call.data.startswith('analyze_'))
def callback_analyze(call):
    asset = call.data.split('_')[1]
    
    # 1. Имитируем получение цены и анализ
    price = round(np.random.uniform(1.0, 1.2), 5)
    tick_data = {'price': price, 'asset': asset}
    features = data_manager.add_tick(tick_data)
    
    # Сообщаем пользователю, что бот "думает"
    bot.answer_callback_query(call.id, text=f"Анализирую {asset}...")
    
    # 2. Делаем прогноз
    prediction = model.predict(features)
    direction = "ВВЕРХ 🟢" if prediction > 0.5 else "ВНИЗ 🔴"
    conf = int(prediction * 100) if prediction > 0.5 else int((1-prediction) * 100)
    
    # 3. Красивое сообщение с иконкой
    icon_url = "https://i.ibb.co/S764pY6/chart-icon.png"
    msg = (f'<b><a href="{icon_url}">📈</a> СИГНАЛ: {asset}</b>\n'
           f"━━━━━━━━━━━━━━━━━━\n"
           f"Прогноз: <b>{direction}</b>\n"
           f"Экспирация: <b>1 минута</b>\n"
           f"Цена: <b>{price}</b>\n"
           f"Надежность: <b>{conf}%</b>\n"
           f"━━━━━━━━━━━━━━━━━━")
    
    # Отправляем сигнал и снова показываем кнопки
    bot.send_message(call.message.chat.id, msg, parse_mode='HTML', reply_markup=main_markup())

if __name__ == "__main__":
    print("🚀 Бот с кнопками запущен! Напиши ему /start в Telegram.")
    bot.polling(none_stop=True)
