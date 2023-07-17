from confluent_kafka import Consumer, KafkaError, TopicPartition
import time

kafka_broker = "kafka:9092"
topic = "my-topic"
group_id = "my-consumer-group"
partition = 0  # Update with the appropriate partition number
offset_to_seek = 10  # Update with the desired offset

consumer_config = {
    "bootstrap.servers": kafka_broker,
    "group.id": group_id,
    "auto.offset.reset": "earliest"
}

consumer = Consumer(consumer_config)
consumer.subscribe([topic])

# Create a TopicPartition object for the desired topic, partition, and offset
tp = TopicPartition(topic, partition, offset_to_seek)

# Assign the TopicPartition to the consumer
consumer.assign([tp])

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(f"Consumer error: {msg.error()}")
        else:
            print(f"Received message: {msg.value().decode('utf-8')}")
        time.sleep(5)

except KeyboardInterrupt:
    pass

finally:
    consumer.close()