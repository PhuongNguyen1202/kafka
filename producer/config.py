import os

class Config:
    # Logging Setting
    LOG_FOLDER = "logging"
    LOG_NAME = "producer"

    # Kafka Producer Setting
    KAFKA_SERVERS = os.getenv("KAFKA_SERVERS", "localhost:29092")
    KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "my-topic")
    KAFKA_TOPIC_PARTITIONS = os.getenv("KAFKA_TOPIC_PARTITIONS", 3)
    KAFKA_REPLICATION_FACTOR = os.getenv("KAFKA_REPLICATION_FACTOR", 1)
