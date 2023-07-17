from fastapi import FastAPI, status
from confluent_kafka import Producer
from starlette.responses import JSONResponse
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka.serialization import StringSerializer

from logger import Logger
from config import Config
from dto import MessageDto


app = FastAPI()


def acked(err, msg):
    """Delivery report handler called on
    successful or failed delivery of message
    """
    if err is not None:
        logger.logError(f'Failed to deliver message: {err}')
    else:
        logger.logInfo(f'Message Information: topic {msg.topic()} - partition [{msg.partition()}] @ offset {msg.offset()}')


@app.on_event("startup")
async def startup_event():
    global logger
    global producer, admin_client

    # Logger Initialization
    logger = Logger(log_dir=Config.LOG_FOLDER, log_name=Config.LOG_NAME, logging_level='INFO')
    logger.logInfo(f'Setting: {Config.__dict__}')

    # Admin Client and Producer Initialization
    admin_client = AdminClient({'bootstrap.servers': Config.KAFKA_SERVERS})
    producer = Producer({'bootstrap.servers': Config.KAFKA_SERVERS})

    # Tạo một KafkaAdminClient để cấu hình số partition
    available_topics = admin_client.list_topics().topics
    if Config.KAFKA_TOPIC not in available_topics:
        new_topic = NewTopic(
            topic=Config.KAFKA_TOPIC,
            num_partitions=int(Config.KAFKA_TOPIC_PARTITIONS),
            replication_factor=int(Config.KAFKA_REPLICATION_FACTOR)
        )
        created_topic_infos = admin_client.create_topics([new_topic])
        for topic, info in created_topic_infos.items():
            try:
                info.result()  # The result itself is None
                logger.logInfo(f"Topic {topic} created.")
            except Exception as e:
                logger.logError(f"Failed to create topic {topic}: {e}.")
    else:
        topic_info = available_topics[Config.KAFKA_TOPIC]
        logger.logInfo(f"Topic {topic_info} with {len(topic_info.partitions)} partitions already created")
        # TODO: check and compare all available settings


@app.on_event("shutdown")
def shutdown_event():
    logger.logInfo(f"Waiting for all messages in the Producer queue to be delivered.")
    producer.flush()


# API endpoint để gửi message vào Kafka
@app.post("/send-message")
async def send_message(message: MessageDto):
    try:
        # Tính toán partition cho message dựa trên key
        # partition = hash(message.key) % num_partitions
        # print(partition)

        # Gửi message vào Kafka topic với partition tương ứng
        record_key: bytes = StringSerializer()(message.key)
        record_value: bytes = StringSerializer()(message.value)
        if message.partition is not None:
            print('-----with partition-------')
            producer.produce(
                topic=Config.KAFKA_TOPIC,
                key=record_key,
                value=record_value,
                partition=message.partition,
                on_delivery=acked,
            )
        else:
            print('-----without partition-------')
            producer.produce(
                topic=Config.KAFKA_TOPIC,
                key=record_key,
                value=record_value,
                on_delivery=acked,
            )
        # print(f'produced message: key {record_key} value {record_value}')
        # producer.flush()  # Đảm bảo message được gửi đi
        producer.poll(0)
        logger.logInfo(f'Produced message: key={record_key}, value={record_value}.')
        return JSONResponse({
            "statusText" : "Message Delivery Complete",
            "statusCode" : status.HTTP_200_OK,
            "message" : message.__dict__,
        })
    except Exception as error:
        logger.logError(f'Producing record failed! with error: {error}')
        return JSONResponse({
            "statusText" : "Producing record failed!",
            "statusCode" : status.HTTP_500_INTERNAL_SERVER_ERROR,
            "errorMessage": error,
        })

# @app.post("/message")
# def create_message(message: str):
#     return {"status": message}


# if __name__ == "__main__":
#     uvicorn.run(":app", host="localhost", port=8081, reload=True)
