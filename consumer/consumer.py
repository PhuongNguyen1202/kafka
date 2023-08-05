import time

from confluent_kafka import Consumer, KafkaException
from confluent_kafka.serialization import StringDeserializer

from config import Config
from logger import Logger


# Logging Initialization
logger = Logger(log_dir=Config.LOG_FOLDER, log_name=Config.LOG_NAME, logging_level='INFO')
logger.logInfo(f'Setting: {Config.__dict__}')

# Kafka Consumer Connection
consumer = Consumer({
    'bootstrap.servers': Config.KAFKA_SERVERS,
    'group.id': Config.KAFKA_CONSUMER_GROUP_ID,
    'auto.offset.reset': 'earliest'
})

# Kafka Consumer subsribes to created topics
consumer.subscribe([Config.KAFKA_TOPIC])

while True:
    try:
        msg = consumer.poll(timeout=1.0)
        if msg is None: continue

        if msg.error():
            logger.logError(f"Kafka Consumer Error: {msg.error()}")
            raise KafkaException(msg.error())
        else:
            record_key: str = StringDeserializer()(msg.key())  # <=> decode('utf-8')
            record_value: str = StringDeserializer()(msg.value())  # <=> decode('utf-8')
            logger.logInfo(f"Message Info: topic {msg.topic()} - partition [{msg.partition()}] @ offset {msg.offset()}")
            logger.logInfo(f"Received message: key={record_key} & value={record_value}")
            time.sleep(Config.SLEEP_TIME)

    except KeyboardInterrupt:
        break

consumer.close()
