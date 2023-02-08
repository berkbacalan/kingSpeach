from kafka import KafkaProducer, KafkaConsumer, KafkaAdminClient
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError
from json import dumps, loads
import asyncio


class KafkaManager():
    producer = None
    consumer = None
    text_file = open("data.txt", "wb")
    admin_client = None

    def __init__(self) -> None:
        self.admin_client = KafkaAdminClient(
            bootstrap_servers=['localhost:9091'],
            client_id='test'
        )
        try:
            self.create_topic()
        except TopicAlreadyExistsError as e:
            print("LOG: topic already exists.")
        except Exception as e:
            print("Exception occured whiile creatin topic:", str(e))


        self.create_producer()
        self.create_consumer()

    def create_topic(self):
        topic_list = []
        topic_list.append(NewTopic(name="speech.topic.0",
                          num_partitions=1, replication_factor=1))
        self.admin_client.create_topics(
            new_topics=topic_list, validate_only=False)

    def create_consumer(self):
        self.consumer = KafkaConsumer(
            'test',
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='my-group-1',
            value_deserializer=lambda m: loads(m.decode('utf-8')),
            bootstrap_servers=['localhost:9091'])

    def create_producer(self):
        try:
            self.producer = KafkaProducer(
                value_serializer=lambda v: dumps(v).encode('utf-8'),
                bootstrap_servers='localhost:9091')
        except Exception as e:
            print("Exception occured while creating producer:", str(e))

    async def produce(self, message: str = None):
        if message is not None:
            self.producer.send("speech.topic.0", value=message)
            self.producer.flush()

    async def consume(self):
        for m in self.consumer:
            self.text_file.write(m.value)
            print(m.value)
