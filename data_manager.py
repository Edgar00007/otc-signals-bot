import pandas as pd
import numpy as np
from datetime import datetime
import logging
from settings import Config # УБРАЛИ config.

logger = logging.getLogger(__name__)

class DataManager:
    def __init__(self):
        self.ticks = pd.DataFrame(columns=['timestamp', 'price', 'volume', 'asset'])
        
    def add_tick(self, tick_data):
        new_tick = pd.DataFrame([{'timestamp': datetime.now(), 'price': tick_data['price'], 'asset': tick_data['asset']}])
        self.ticks = pd.concat([self.ticks, new_tick], ignore_index=True)
        return new_tick
