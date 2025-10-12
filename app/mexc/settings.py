import os
from typing import List

from dotenv import load_dotenv

from API.settings import api_get_intervals, api_get_symbols

load_dotenv()

class __Settings:


    REDIS_HOST: str = os.environ.get('REDIS_HOST')
    REDIS_PORT: str = os.environ.get('REDIS_PORT')
    REDIS_PASSWORD: str = os.environ.get('REDIS_PASSWORD')
    REDIS_CANDLE_DB: int = int(os.environ.get('REDIS_CANDLE_DB'))

    INTERVALS: List[int] = api_get_intervals()
    SYMBOLS: List[str] = api_get_symbols()
    CHANNEL_TYPE: str = 'linear'
    TEST_NET: bool = False

settings = __Settings()