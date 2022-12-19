# demo-stock-data-producer
====================================================
Генератор фейковых биржевых данных
<br>
Данные сохраняются в Kafka.<br>
В качестве шедулера - apscheduler, вебсервер - uvicorn, фреймворк - FastApi

Запуск проекта
-----------------------------
Для запуска необходимо передать три переменные окружения:

    KAFKA_TOPIC_PREFIX, по умолчанию - 'dev_'
    KAFKA_URL по умолчанию - 'localhost:9092'
    TICKERS_LIST писок, разделенный запятыми 'test1,test2'

Команда для локального запуска:

    uvicorn producer:app


Docker:

    docker run -e KAFKA_URL=localhost:9092 -e KAFKA_TOPIC_PREFIX=prod_ -e TICKERS_LIST=ticker_00,ticker_01 baloover/stock-producer-back:0.1.0

Файловая структура
-----------------------------
| File                     | Contents                    |
|--------------------------|-----------------------------|
| producer.py              | FastApi (запуск, роуты)     |
| settings.py              | Файл конфигурации           |
| moduled/                 | Бизнес-функции хранятся тут |
| -stock_data_generator.py | функционал генерации данных |
| infrastructure/          |                             |
| -kafka.py                | функционал работы с Kafka   |
| -scheduler.py            | все, что касается заданий   |

