import pandas as pd
import numpy as np
from datetime import datetime
import logging
# УБРАЛИ CONFIG.
from settings import Config

logger = logging.getLogger(__name__)

class DataManager:
    def __init__(self):
        self.ticks = pd.DataFrame(columns=['timestamp', 'price', 'volume', 'asset'])
        
    def add_tick(self, tick_data):
        new_tick = pd.DataFrame([{'timestamp': datetime.now(), 'price': tick_data['price'], 'asset': tick_data['asset']}])
        self.ticks = pd.concat([self.ticks, new_tick], ignore_index=True)
        return new_tick

    def get_data_len(self):
        return len(self.ticks)
