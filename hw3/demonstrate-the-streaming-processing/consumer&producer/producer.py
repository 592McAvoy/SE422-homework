from kafka import KafkaProducer
import logging
import sys

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

if __name__=='__main__':
    logger = logging.getLogger('kafka')
    logger.addHandler(logging.StreamHandler(sys.stdout))
    logging.basicConfig(filename='producer.log', level=logging.DEBUG, format=LOG_FORMAT)

    producer = KafkaProducer(bootstrap_servers=['47.106.8.44:9092'])
    for i in range(5):
        future = producer.send('my_topic' , key= b'my_key', value= b'my_value', partition= 0)
        result = future.get(timeout= 10)
        print(result)
