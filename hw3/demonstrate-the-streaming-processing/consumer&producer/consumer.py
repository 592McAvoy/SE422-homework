from kafka import KafkaConsumer
import logging
import sys

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

if __name__=='__main__':
    logger = logging.getLogger('kafka')
    logger.addHandler(logging.StreamHandler(sys.stdout))
    logging.basicConfig(filename='consumer.log', level=logging.DEBUG, format=LOG_FORMAT)
    consumer = KafkaConsumer('my_topic', group_id= 'group2', bootstrap_servers= ['47.106.8.44:9092'])
    for msg in consumer:	
        print(msg)
        logging.debug("Received Message: " + str(msg))
