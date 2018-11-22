from kafka import KafkaConsumer
from time import time

last = time()

def toGetMetrics():
    now = time()
    if now - last > 60:
        last = time()
        return true
    return false

if __name__=='__main__':
    consumer = KafkaConsumer('my_topic', group_id= 'group2', bootstrap_servers= ['47.106.8.44:9092'])
    for msg in consumer:
    	
	    print(msg)
