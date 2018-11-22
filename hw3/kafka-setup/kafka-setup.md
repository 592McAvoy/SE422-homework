# Setup a kafka cluster

### 下载及安装kafka环境

可以在kafka官网 <http://kafka.apache.org/downloads>下载到最新的kafka安装包，选择下载二进制版本的tgz文件，这里我们选择的版本是0.11.0.1。

Kafka是使用scala编写的运行与jvm虚拟机上的程序，可以运行站在linux和windows的环境下，我在window8和debain8 的环境下均进行过测试，测试均通过。

首先确保你的机器上安装了jdk，kafka需要java运行环境，以前的kafka还需要zookeeper，该版本的kafka已经内置了一个zookeeper环境，所以我们可以直接使用

kafka的安装过程非常简单，只需要将压缩的文件解压即可。

### 配置

在kafka解压目录下下有一个config的文件夹，里面放置的是我们的配置文件

**consumer.properites** 消费者配置，这个配置文件用于配置于2.5节中开启的消费者，此处我们使用默认的即可

**producer.properties** 生产者配置，这个配置文件用于配置于2.5节中开启的生产者，此处我们使用默认的即可

**server.properties kafka**服务器的配置，此配置文件用来配置kafka服务器，目前仅介绍几个最基础的配置

1. broker.id 申明当前kafka服务器在集群中的唯一ID，需配置为integer,并且集群中的每一个kafka服务器的id都应是唯一的，我们这里采用默认配置即可

2. listeners 申明此kafka服务器需要监听的端口号，如果是在本机上跑虚拟机运行可以不用配置本项，默认会使用localhost的地址，如果是在远程服务器上运行则必须配置，例如：

　　　　　　　　　　`listeners=PLAINTEXT:// 192.168.180.128:9092`

​       并确保服务器的9092端口能够访问

3. zookeeper.connect 申明kafka所连接的zookeeper的地址 ，需配置为zookeeper的地址，由于本次使用的是kafka高版本中自带zookeeper，使用默认配置即可

　　　　　　　　　　`zookeeper.connect=localhost:2181`

### 运行kafka和zookeeper

启动zookeeper：bin\windows\zookeeper-server-start.bat config\zookeeper.properties

启动成功后：![](.\zookeeper.png)

启动kafka：bin\windows\kafka-server-start.bat config\server.properties

启动成功后：![](.\server.png)

### 创建生产者和消费者

##### 创建一个topic：

Kafka通过topic对同一类的数据进行管理，同一类的数据使用同一个topic可以在处理数据时更加的便捷

`bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic ``test`

##### 产生一个消费者：

运行配置好的消费者`bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic ``test` `--from-beginning`

![](.\consumer.png)

当生产者发送一个消息时，消费者能够接受到该消息。该例子中为“ this is a test message”.

##### 产生一个生产者：

运行一个已经配置道的生产者`bin/kafka-console-producer.sh --broker-list localhost:9092 --topic ``test`

输入消息“ this is a test message”，此时消费者将接收到该消息，见上图。

![](.\producer.png)

###  使用java程序运行kafka

##### 创建topic：

```
import java.util.ArrayList;
import java.util.Properties;
import java.util.concurrent.ExecutionException;
import org.apache.kafka.clients.admin.AdminClient;
import org.apache.kafka.clients.admin.AdminClientConfig;
import org.apache.kafka.clients.admin.CreateTopicsResult;
import org.apache.kafka.clients.admin.NewTopic;
public class Topic {
    public static void main(String[] args) {
        //创建topic
        Properties props = new Properties();
        props.put("bootstrap.servers", "localhost:9092");
        AdminClient adminClient = AdminClient.create(props);
        ArrayList<NewTopic> topics = new ArrayList<NewTopic>();
        NewTopic newTopic = new NewTopic("test", 1, (short) 1);
        topics.add(newTopic);
        CreateTopicsResult result = adminClient.createTopics(topics);
        try {
            result.all().get();
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (ExecutionException e) {
            e.printStackTrace();
        }
    }
}

```

#####  Producer生产者发送消息

```

import java.util.Properties;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.clients.producer.Producer;


public class producer {
    public static void main(String[] args){
        Properties props = new Properties();
        props.put("bootstrap.servers", "localhost:9092");
        props.put("acks", "all");
        props.put("retries", 0);
        props.put("batch.size", 16384);
        props.put("linger.ms", 1);
        props.put("buffer.memory", 33554432);
        props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
        props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");

        Producer<String, String> producer = new KafkaProducer<String, String>(props);
        for (int i = 0; i < 100; i++) {
            System.out.println(i);
            producer.send(new ProducerRecord<String, String>("test", Integer.toString(i), Integer.toString(i)));
        }
        producer.close();

    }
}

```

##### Consumer消费者消费消息：

```
import java.util.Arrays;
import java.util.Collection;
import java.util.Properties;
import org.apache.kafka.clients.consumer.ConsumerRebalanceListener;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.common.TopicPartition;


public class consumer {
    public static void main(String[] args){
        Properties props = new Properties();
        props.put("bootstrap.servers", "localhost:9092");
        props.put("group.id", "test");
        props.put("enable.auto.commit", "true");
        props.put("auto.commit.interval.ms", "1000");
        props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
        props.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
        final KafkaConsumer<String, String> consumer = new KafkaConsumer<String,String>(props);
        consumer.subscribe(Arrays.asList("test"),new ConsumerRebalanceListener() {
            public void onPartitionsRevoked(Collection<TopicPartition> collection) {
            }
            public void onPartitionsAssigned(Collection<TopicPartition> collection) {
                //将偏移设置到最开始
                consumer.seekToBeginning(collection);
            }
        });
        while (true) {
            ConsumerRecords<String, String> records = consumer.poll(100);
            for (ConsumerRecord<String, String> record : records) {
                System.out.println(record.key());
                System.out.printf("offset = %d, key = %s, value = %s%n", record.offset(), record.key(), record.value());

            }
        }
    }
}

```

##### 运行结果：

该生产者将发送1到99的<key,value>对到消费者，消费者接受该消息，然后输出<offset,key,value>。P.S. (在运行前需要运行zookeeper和kafka)

**消费者结果：**![](.\javaConsumer.png)

**生产者结果：**

![](.\javaProducer.png)

