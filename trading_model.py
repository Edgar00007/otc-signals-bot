import numpy as np
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import StandardScaler
import logging
from settings import Config # УБРАЛИ config.

logger = logging.getLogger(__name__)

class TradingModel:
    def __init__(self):
        self.model = SGDClassifier(loss='log_loss', random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def predict(self, features):
        return np.random.random()

    def train(self, features, labels):
        return True
