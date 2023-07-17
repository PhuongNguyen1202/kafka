from confluent_kafka import Consumer, KafkaError
import time

kafka_broker = "kafka:9092"
topic = "my-topic1"
group_id = "my-consumer-group"

consumer_config = {
    "bootstrap.servers": kafka_broker,
    "group.id": group_id,
    "auto.offset.reset": "earliest"
}

consumer = Consumer(consumer_config)
consumer.subscribe([topic])

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
            print(f"Consumer 2 Received message: {msg.key()} {msg.value()} with partition {msg.partition()} {msg.offset()}")
        time.sleep(5)

except KeyboardInterrupt:
    pass

finally:
    consumer.close()

