import logging
import orjson
from datetime import datetime
from pykafka import KafkaClient
from pykafka.exceptions import SocketDisconnectedError, LeaderNotAvailable


class KafkaProducer:
    def __init__(self, kafka_client: KafkaClient, ticker: str) -> None:
        self._kafka_client = kafka_client
        self._topic = self._kafka_client.topics[ticker]
        self._producer = self._topic.get_producer()

    async def send_point(self, value: int) -> None:
        try:
            self._producer.produce(orjson.dumps((datetime.utcnow().replace(microsecond=0),
                                                 value)))
            logging.info(orjson.dumps((datetime.utcnow().replace(microsecond=0),
                                       value)))
        except (SocketDisconnectedError, LeaderNotAvailable) as e:
            self._producer = self._topic.get_producer()
            self._producer.stop()
            self._producer.start()
            self._producer.produce(orjson.dumps((datetime.utcnow().replace(microsecond=0),
                                                 value)))
