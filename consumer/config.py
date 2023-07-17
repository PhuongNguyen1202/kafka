import os

class Config:
    # Logging Setting
    LOG_FOLDER = "logging"
    LOG_NAME = "consumer"

    # Kafka Producer Setting
    KAFKA_SERVERS = os.getenv("KAFKA_SERVERS", "localhost:29092")
    KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "my-topic")
    KAFKA_CONSUMER_GROUP_ID = os.getenv("KAFKA_CONSUMER_GROUP_ID", "my-topic-group-1")

    # Timer
    SLEEP_TIME = 5 #s
