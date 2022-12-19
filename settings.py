from envparse import Env

env = Env()
# env.read_envfile()

HOST = env('HOST', default='0.0.0.0')
PORT = env.int('PORT', default=8000)
AUTO_RELOAD = env.bool('AUTO_RELOAD', default=True)
DEBUG = env.bool('DEBUG', default=False)

####################################
# Kafka
####################################
KAFKA_URL = env('KAFKA_URL', default='localhost:9092')
KAFKA_TOPIC_PREFIX = env('KAFKA_TOPIC_PREFIX', default='dev_')
####################################
# Producers
####################################
TICKERS_LIST = env.list('TICKERS_LIST', default=['test1','test2'])

