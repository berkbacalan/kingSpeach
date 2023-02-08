from kafka import KafkaProducer
from json import dumps, loads

try:
    pro = KafkaProducer(
                # security_protocol="SSL",
                value_serializer=lambda v: dumps(v).encode('utf-8'),
                bootstrap_servers='localhost:9091')
except Exception as e:
    print("ERROR1:", str(e))

try:
    pro.send(topic="speech.topic.0", value="asd")
    print("message sended")
except Exception as e:
    print("ERROR2:", str(e))

pro.flush()