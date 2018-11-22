# Demonstrate the streaming processing

由于一些原因，为了做 Part D，我这里也另外搭建了 Kafka 集群以及 consumer & producer

## Kafka Cluster

- 使用 [wurstmeister/kafka-docker](https://github.com/wurstmeister/kafka-docker) 中的 kafka-docker 
- 在上述 docker-compose.yml 中略作改动，放在与本文档同目录下
- 使用以下命令创建集群、扩容、停止

```
$ docker-compose up -d
$ docker-compose scale kafka=3
$ docker-compose stop
```

## Consumer & Producer

- 使用 python-kafka
- 代码在同目录 ./consumer&producer 中

## Demonstrate 

- 使用 Logging 记录 producer 生产的消息和 consumer 消费的信息
- Producer
    - 不需要添加任何日志记录，默认有记录
    - e.g. 发送了一条 key 为 'my_key'，value 为 'my_value' 的信息，log 记录如下所示
        ```
        2018-11-22 14:52:10,523 - DEBUG - Sending (key=b'my_key' value=b'my_value' headers=[]) to TopicPartition(topic='my_topic', partition=0)
        ```
- Consumer
    - 需要手动添加日志记录
    - e.g. 在 consumer.py 中添加以下代码
        ```
        logging.debug("Received Message: " + str(msg))
        ```
        能够得到以下的 log 记录
        ```
        2018-11-22 14:52:39,871 - DEBUG - Received Message: ConsumerRecord(topic='my_topic', partition=0, offset=72, timestamp=1542869530430, timestamp_type=0, key=b'my_key', value=b'my_value', headers=[], checksum=None, serialized_key_size=6, serialized_value_size=8, serialized_header_size=-1)
        ```
- 根据 log 记录能够清晰地展现出使用 Kafka 后的流式处理过程

## 其他问题
- 使用 python-kafka 做 log 会有大量它自己记录的其他 log 信息，检查起来十分麻烦
- 可以采用 Elastic Search + Fluentd/Logstash + Kibana 来做日志检索