import os

from dotenv import load_dotenv

load_dotenv()

class __Settings:


    REDIS_HOST: str = os.environ.get('REDIS_HOST')
    REDIS_PORT: str = os.environ.get('REDIS_PORT')
    REDIS_PASSWORD: str = os.environ.get('REDIS_PASSWORD')
    REDIS_STREAMING_DB: int = int(os.environ.get('REDIS_STREAMING_DB'))



settings = __Settings()