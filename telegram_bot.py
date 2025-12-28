import telebot
from telebot import types
import logging
from settings import Config  # Берем настройки из вашего файла settings.py

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота
bot = telebot.TeleBot(Config.TELEGRAM_BOT_TOKEN)

# Вспомогательная статистика (в реальном боте данные можно брать из RiskManager)
bot_stats = {
    "is_active": True,
    "signals_count": 0
}

def get_dashboard_markup():
    """Создает кнопки для управления ботом"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    # Кнопка включения/выключения
    status_text = "🟢 Работает" if bot_stats["is_active"] else "🔴 Остановлен"
    btn_toggle = types.InlineKeyboardButton(f"Статус: {status_text}", callback_data="toggle_bot")
    
    # Кнопки статистики и настроек
    btn_stats = types.InlineKeyboardButton("📊 Статистика", callback_data="show_stats")
    btn_settings = types.InlineKeyboardButton("⚙️ Настройки", callback_data="show_settings")
    
    markup.add(btn_toggle)
    markup.add(btn_stats, btn_settings)
    return markup

@bot.message_handler(commands=['start', 'dashboard'])
def send_welcome(message):
    """Главная команда для вызова Dashboard"""
    welcome_text = (
        "<b>🤖 Панель управления сигнальным ботом</b>\n\n"
        "Здесь вы можете контролировать работу алгоритма и просматривать текущую статистику."
    )
    bot.send_message(
        message.chat.id, 
        welcome_text, 
        parse_mode='HTML', 
        reply_markup=get_dashboard_markup()
    )

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    """Обработка нажатий на кнопки Dashboard"""
    if call.data == "toggle_bot":
        bot_stats["is_active"] = not bot_stats["is_active"]
        logger.info(f"Статус бота изменен: {bot_stats['is_active']}")
        
    elif call.data == "show_stats":
        stats_text = (
            "📈 <b>Текущая статистика:</b>\n"
            f"- Отправлено сигналов: {bot_stats['signals_count']}\n"
            f"- Баланс: ${Config.INITIAL_BALANCE}"
        )
        bot.answer_callback_query(call.id, "Статистика обновлена")
        # Обновляем текст сообщения на статистику
        bot.edit_message_text(
            stats_text, 
            call.message.chat.id, 
            call.message.message_id, 
            parse_mode='HTML', 
            reply_markup=get_dashboard_markup()
        )
        return

    # После любого действия обновляем основную панель
    bot.edit_message_reply_markup(
        call.message.chat.id, 
        call.message.message_id, 
        reply_markup=get_dashboard_markup()
    )
    bot.answer_callback_query(call.id, "Обновлено")

if __name__ == "__main__":
    logger.info("Dashboard запущен...")
    bot.polling(none_stop=True)
