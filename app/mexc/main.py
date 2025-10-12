import multiprocessing
import json

import websocket
from dotenv import load_dotenv

from app.mexc.callback import callback_kline
from app.mexc.settings import settings

load_dotenv()

chunks = []

current_chunk = []

# Разделяем BASE_SYMBOLS на чанки по 10 символов
for symbol in settings.SYMBOLS:
    current_chunk.append(symbol)
    if len(current_chunk) == 10:
        chunks.append(current_chunk)
        current_chunk = []

if current_chunk:
    chunks.append(current_chunk)


def ticker_stream(symbols, queue):
    def on_open(ws):
        subscription_message = {
            "method": "SUBSCRIPTION",
            "params": [
                "spot@public.kline.v3.api.pb@BTCUSDT@Min15"
            ]
        }
        ws.send(json.dumps(subscription_message))

    def on_message(ws, message):
        queue.put(message)  # put message in the queue

    ws = websocket.WebSocketApp("wss://wbs-api.mexc.com/ws",
                                on_open=on_open,
                                on_message=on_message)

    while True:
        ws.run_forever()

if __name__ == "__main__":
    queues = []
    processes = []
    for symbols in chunks:
        queue = multiprocessing.Queue()
        process = multiprocessing.Process(target=ticker_stream, args=(symbols, queue))
        process.start()
        processes.append(process)
        queues.append(queue)

    try:
        while True:
            for queue in queues:
                while not queue.empty():
                    data = queue.get()
                    if isinstance(data, bytes):
                        callback_kline(data)

    except KeyboardInterrupt:
        pass  # Обработайте прерывание для безопасного завершения

    for process in processes:
        process.join()