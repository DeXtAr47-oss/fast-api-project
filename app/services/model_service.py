import joblib
import pandas as pd

from ..core.config import Settings
from ..cache.redis_cache import *

model = joblib.load(Settings.MODEL_PATH)

def predict_car_price(data: dict):
    cached_key = ' '.join([str(val) for val in data.values()])
    cached = get_cached_prediction(cached_key)
    if cached:
        return cached
    else:
        prediction = model.predict(pd.DataFrame([data]))[0]
        set_cache_prediction(cached_key, prediction)
        return prediction
