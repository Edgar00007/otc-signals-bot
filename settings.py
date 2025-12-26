import os
from datetime import time

class Config:
    # API Settings
    API_DEMO_URL = "https://api.pocketoption.com/demo"
    API_REAL_URL = "https://api.pocketoption.com"
    
    # Telegram Settings - ИСПРАВЛЕНО
    TELEGRAM_BOT_TOKEN = '8569495893:AAHKLwB94XMXFCAGAqDxSYTKp4XyEp0GZQs'
    TELEGRAM_CHANNEL_ID = '@edgar_signals_otc'
    TELEGRAM_GROUP_ID = '-1001234567890'
    
    # Trading parameters
    INITIAL_BALANCE = 10.0
    TRADE_AMOUNT = 1.0
    ASSETS = ["EURUSD", "GBPUSD", "USDJPY", "BTCUSD", "ETHUSD"]
    EXPIRY_TIME = 60
    TRADE_TYPE = "binary"
    
    # Model parameters
    CONFIDENCE_THRESHOLD = 0.65
    RETRAIN_INTERVAL = 100
    WARMUP_PERIOD = 50
    
    # Risk management
    MAX_DAILY_LOSS = 5.0
    MAX_DRAWDOWN = 10.0
    STOP_LOSS_STREAK = 5
    
    # Data collection
    TICK_HISTORY = 1000
    
    # Trading schedule
    TRADING_HOURS = {
        "start": time(0, 0),   
        "end": time(23, 59)     
    }
