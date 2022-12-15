from pykafka import KafkaClient
from settings import KAFKA_URL

client = KafkaClient(KAFKA_URL)

topic = client.topics["topicname"]
producer = topic.get_producer()
consumer = topic.get_simple_consumer()
