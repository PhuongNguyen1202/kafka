import uvicorn
from fastapi import FastAPI
from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka.serialization import IntegerSerializer, StringSerializer
from pydantic import BaseModel
from typing import Optional
import os

app = FastAPI()

# Model để xác định kiểu dữ liệu của request body
class Message(BaseModel):
    key: Optional[int] = None
    value: str

# Lấy giá trị của biến môi trường KAFKA_TOPIC_PARTITIONS
num_partitions = int(os.getenv("KAFKA_TOPIC_PARTITIONS", 3))
print(num_partitions)

# Tạo một KafkaAdminClient để cấu hình số partition
admin_client = AdminClient({"bootstrap.servers": "localhost:29092"})
topic = NewTopic("my-topic1", num_partitions=num_partitions, replication_factor=1)
fs = admin_client.create_topics([topic])

for topic, f in fs.items():
    try:
        f.result()  # The result itself is None
        print("Topic {} created".format(topic))
    except Exception as e:
        print("Failed to create topic {}: {}".format(topic, e))


# Khởi tạo Producer
producer_config = {"bootstrap.servers": "localhost:29092"}
producer = Producer(producer_config)

# @app.on_event('shutdown')
# def shutdown():
#     producer.flush()


# API endpoint để gửi message vào Kafka
@app.post("/send-message")
async def send_message(message: Message):
    # Tính toán partition cho message dựa trên key
    # partition = hash(message.key) % num_partitions
    # print(partition)

    # Gửi message vào Kafka topic với partition tương ứng
    if record_key is not None:
        record_key = IntegerSerializer()(message.key)
    else:
        record_key = message.key
    record_value = StringSerializer()(message.value)
    producer.produce(
        topic="my-topic",
        key=record_key,
        value=record_value,
    )
    print(f'produced message: key {record_key} value {record_value}')
    producer.flush()  # Đảm bảo message được gửi đi

    return {f"message": "Message sent to Kafka, key {record_key} value {record_value}"}


@app.post("/message")
def create_message(message: str):
    return {"status": message}


if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8081, reload=True)