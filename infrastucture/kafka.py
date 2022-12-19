import logging
import orjson
from datetime import datetime, timedelta
from pykafka import KafkaClient
from pykafka.exceptions import SocketDisconnectedError, LeaderNotAvailable


class KafkaProducer:
    def __init__(self, kafka_client: KafkaClient, ticker: str):
        self._kafka_client = kafka_client
        self._topic = self._kafka_client.topics[ticker]
        self._producer = self._topic.get_producer(linger_ms=0)
        self._last_sent_time: datetime | None = None

    async def send_point(self, value: int) -> None:
        try:
            time = datetime.utcnow().replace(microsecond=0)
            self._producer.produce(orjson.dumps((time, value)))
            self._last_sent_time = time
        except (SocketDisconnectedError, LeaderNotAvailable) as e:
            self._producer = self._topic.get_producer()
            self._producer.stop()
            self._producer.start()
            self._producer.produce(orjson.dumps((datetime.utcnow().replace(microsecond=0),
                                                 value)))

    def is_healthy(self) -> bool:
        if datetime.utcnow().replace(microsecond=0)-self._last_sent_time < timedelta(seconds=2):
            return True
