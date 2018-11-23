# kafka集群性能测试
## 测试环境
本测试中，kafka集群配置在阿里云服务器的docker里，CPU核数为1核，内存容量为2G。
本测试分为两个部分：
- 利用kafka自带的性能测试脚本进行测试
- 在另外两台电脑上分别跑producer和consumer，测试producer和client方的throughput（每分钟发消息数/每分钟收消息数），为了实现容易，本测试中改为打印
每发送100条消息和每收取100条消息所需时间，producer和consumer的代码如下：
```
#producer.py
from kafka import KafkaProducer
import logging
import sys
import time

if __name__=='__main__':
    producer = KafkaProducer(bootstrap_servers=['47.106.8.44:9092'])
    counter = 0
    start = time.time()
    while(1):
        future = producer.send('my_topic' , key= b'my_key', value= b'my_value', partition= 0)
        result = future.get(timeout= 10)
        counter = counter + 1
        if(counter % 100 == 0):
            print(time.time() - start)
```
```
#consumer.py
from kafka import KafkaConsumer
import logging
import sys
import time

if __name__=='__main__':
    consumer = KafkaConsumer('my_topic', group_id= 'group2', bootstrap_servers= ['47.106.8.44:9092'])
    counter = 0
    start = time.time()
    for msg in consumer:	
        counter = counter + 1
        if(counter % 100 == 0):
            print(time.time() - start)
```
同时，使用Prometheus监控docker容器使用资源的情况，并通过Grafana将监控数据可视化。

## 测试一：使用自带性能测试脚本测试kafka server性能
### Producer测试
```
bash-4.4# ./bin/kafka-producer-perf-test.sh --topic test_perf --num-records 1000000 --record-size 1000 --throughput 20000 --producer-props bootstrap.servers=localhost:9092
[2018-11-23 03:12:00,229] WARN [Producer clientId=producer-1] Error while fetching metadata with correlation id 1 : {test_perf=LEADER_NOT_AVAILABLE} (org.apache.kafka.clients.NetworkClient)
706 records sent, 140.0 records/sec (0.13 MB/sec), 1847.5 ms avg latency, 4470.0 max latency.
688 records sent, 134.6 records/sec (0.13 MB/sec), 6917.4 ms avg latency, 9527.0 max latency.
656 records sent, 128.0 records/sec (0.12 MB/sec), 11924.4 ms avg latency, 14620.0 max latency.
672 records sent, 128.9 records/sec (0.12 MB/sec), 17076.3 ms avg latency, 19814.0 max latency.
656 records sent, 128.6 records/sec (0.12 MB/sec), 22214.0 ms avg latency, 24898.0 max latency.
656 records sent, 129.7 records/sec (0.12 MB/sec), 27317.7 ms avg latency, 29939.0 max latency.
org.apache.kafka.common.errors.TimeoutException: Expiring 16 record(s) for test_perf-0: 30192 ms has passed since last append
```
先预设了一个较大的值，可以发现这个测试已经远远超过kafka的极限了，在发送约3500的record后，其他的请求已经timeout，无法成功执行了。
为了获取正常的测试结果，以下测试--num-records都设为1000
#### 测试：和record-size的关系
```
bash-4.4# ./bin/kafka-producer-perf-test.sh --topic test_perf --num-records 1000 --record-size 1000 --throughput 20000 --producer-props bootstrap.servers=localhost:9092
bash-4.4# ./bin/kafka-producer-perf-test.sh --topic test_perf --num-records 1000 --record-size 100 --throughput 20000 --producer-props bootstrap.servers=localhost:9092
bash-4.4# ./bin/kafka-producer-perf-test.sh --topic test_perf --num-records 1000 --record-size 10 --throughput 20000 --producer-props bootstrap.servers=localhost:9092
```
| record-size | MB/S | avg latency |  records/second |
| :------: | :------: | :------: | :------: |
| 1000 | 0.14 | 2864.44ms | 143.678161 |
| 100 | 0.20 | 21.28 | 2096.436059 |
| 10  | 0.02 | 11.10 | 2247.191011 |

- 在record-size为1000时，kafka-server负载较大，导致throughput较低，由此MB/s性能不如size为100时。
- 在record-size为10时，虽然throughput还不错（每秒处理records数），但由于record的size较小，所以MB/s较小。
- 在record-size为100时，比较能充分使用kafka-server的性能。

#### 测试：和throughput的关系
由于上一个测试发现record-size为100时数据比较合适，故选择record-size为100
```
bash-4.4# ./bin/kafka-producer-perf-test.sh --topic test_perf --num-records 1000 --record-size 1000 --throughput 40000 --producer-props bootstrap.servers=localhost:9092
bash-4.4# ./bin/kafka-producer-perf-test.sh --topic test_perf --num-records 1000 --record-size 1000 --throughput 20000 --producer-props bootstrap.servers=localhost:9092
bash-4.4# ./bin/kafka-producer-perf-test.sh --topic test_perf --num-records 1000 --record-size 1000 --throughput 10000 --producer-props bootstrap.servers=localhost:9092
```
| throughput | MB/S | avg latency |  records/second |
| :------: | :------: | :------: | :------: |
| 40000 | 0.16 | 32.36ms | 1663.893511 |
| 20000 | 0.20 | 21.28 | 2096.436059 |
| 10000  | 0.21 | 25.23 | 2247.191011 |

- 在throughput为40000时，推测由于producer发送信息过快，达到server的负载极限，故性能各方面均表现不佳。
- 在throughput为10000时，除latency外均优于其他。latency较高的原因可能为producer发送较慢。
- 在throughput为20000时，比较能充分使用kafka-server的性能

### Consumer测试
由测试二可以得出，consumer并不会成为整个系统的性能瓶颈，故对consumer的自带测试报告这里没有给出。

## 测试二：在另两台电脑上运行producer和consumer
- producer运行环境：
CPU：i7-8700 3.2GHz 6cores
- consumer运行环境：
CPU：i5-4300U 1.9GHz 2cores

### 测试结果
由于核数限制，所以同时跑了6个producer和1个consumer。</br>
在起producer的过程中，从1至6个，成功发送100条msg的时间并没有太多改变，均值为6.4752s。</br>
consumer接收成功的速度会快很多，成功接收100条msg的时间均值为1.0987s，其恰好大约为producer所发送所需时间的1/6。</br>
由此推测，consumer的接收不会成为整个系统的bottle neck。</br>

### Grafana监测结果图
#### 容器内存使用曲线图
![内存使用曲线图](https://github.com/592McAvoy/homework1/blob/master/hw3/%E5%9B%BE%E7%89%87/%E5%86%85%E5%AD%98%E4%BD%BF%E7%94%A8.png)
#### 网络输入流量曲线图
![网络输入流量曲线图](https://github.com/592McAvoy/homework1/blob/master/hw3/%E5%9B%BE%E7%89%87/network%20input.png)
#### 网络输出流量曲线图
![网络输出流量曲线图](https://github.com/592McAvoy/homework1/blob/master/hw3/%E5%9B%BE%E7%89%87/network%20output.png)
