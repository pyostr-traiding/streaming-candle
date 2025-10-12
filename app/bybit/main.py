import multiprocessing

from dotenv import load_dotenv

from app.bybit.callback import callback_kline
from app.bybit.stream import kline_stream
from app.bybit.settings import settings

load_dotenv()

chunks = []

current_chunk = []

# Разделяем BASE_SYMBOLS на чанки по 10 символов
for symbol in settings.SYMBOLS:
    symbol = symbol.upper() + 'USDT'
    current_chunk.append(symbol)
    if len(current_chunk) == 10:
        chunks.append(current_chunk)
        current_chunk = []

if current_chunk:
    chunks.append(current_chunk)


if __name__ == "__main__":
    queues = []
    processes = []

    for interval in settings.INTERVALS:


        for symbols in chunks:
            queue = multiprocessing.Queue()
            process = multiprocessing.Process(
                target=kline_stream,
                args=(
                    symbols,
                    queue,
                    interval,
                )
            )
            process.start()
            processes.append(process)
            queues.append(queue)

    # Здесь мы можем получать данные из очередей
    try:
        while True:
            for queue in queues:
                while not queue.empty():
                    data = queue.get()
                    if 'kline' in data['topic']:
                        callback_kline(data)  # Обработка данных

    except KeyboardInterrupt:
        print("Shutting down...")

    # Ждем завершения всех процессов
    for process in processes:
        process.join()