import json


def callback_kline(
        data: bytes
):
    """
    Обработчик стрима тикеров
    """
    print('--', data)
    data = json.loads(data)
    print(data)

