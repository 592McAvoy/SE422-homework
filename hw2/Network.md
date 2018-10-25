# Network

## 计算机网络概念

计算机网络是指，利用通信设备和线路将地理位置不同的、功能独立的多个计算机系统连接起来，以功能完善的网络软件实现网络的硬件、软件及资源共享和信息传递的系统。

## 计算机网络硬件

### 网络硬件

- 服务器(server)
  
  ![server][1]
  
  服务器是具有较高计算能力，能够提供给多个用户使用的计算机。服务器通常需要24小时不间断运行，并且有足够的稳定性。PC机用户通过网络访问服务器上的应用。

- 调制解调器(modem)

  调制解调器本质上是一个信号的转换器。将通过光纤、电话线等传输的模拟信号与计算机能接受的数字信号互相转换，保证计算机能与网络连接。

- 路由器(router)

  ![router][2]
  
  路由器位于两个或更多个网络的交汇处，负责在计算机 **网络之间** 的数据传输，使网络之间能够相互通信。

- 交换机(switch)
  
  ![switch][3]
  
  交换机位于某一计算机网络之下，负责将当前 **网络下** 的各个设备连接，使这些设备能够相互通信

- 防火墙(firewall)

  ![firewall][5]

  防火墙在网络与计算机之间，通过设定规则，来过滤特定的网络包的传输。通常用于企业等大型组织的网络中。

### 硬件层次

![network][4]

1. 网络上的数据包先通过调制解调器(Modem)进行信号的转换
2. 由路由器(Router)转发至本地局域网中某个交换机(Swich)
3. 由交换机(Switch)转发至指定设备
4. 防火墙(Firewall)通常设置于路由器(Router)与互联网之间，过滤所有网络包

## 计算机网络性能指标

1. 速率(Speed)

    网络中的速率是指连续在计算机网络上的主机在数字信道上传送数据的速率或比特率，单位是bit/s

2. 吞吐量(Throughput)

    表示在单位时间内通过某个网络（或信道、接口）的数据量。吞吐量受网络的带宽或网络的额定速率的限制

    - 瞬时吞吐量（instantaneous throughput）
  
        从服务器到客户机通过计算机网络传送一个大文件，任意时刻客户机接收该文件的速率

    - 平均吞吐量（average throughput）

        假设客户机接收该文件的所有F比特用了T秒，那么 F/T即平均吞吐量

    吞吐量等于瓶颈链路（bottle link）的传输速率。以下图为例。

    ![throughput][7]

    R(s)表示服务器和路由器之间的链路速率，R(c)表示路由器和客户机之间的链路速率，显然，该服务器不能以快于R(s)的速率向链路中输送比特，路由器也不能以快于R(c)的速率转发比特。

    上图中吞吐量为 <code>min{R(c), R(s)}</code> bps

3. 带宽(Bandwidth)

    信道传输的是电磁波信号，而电磁波是有一定的频率范围，带宽指的就是这段有效的频率范围的值

    带宽 = 最高有效频率 - 最低有效频率

    不同的信道，其带宽（频率范围）是不一样的，根据带宽的不同，可将信道划分为窄带信道（0 - 300Hz）, 音频信道（300 - 3400Hz）和宽带信道（带宽为3400Hz以上）。我们平常说的“装宽带”，意思就是安装3400Hz以上带宽的信道的意思

    在计算机网络中，宽带往往还表示网络的通信线路所能传达数据的能力，单位时间能通过链路的数据量，指最大速率，即速率上限。

4. 时延(Delay)

    ![delay][6]

    是指数据（一个报文或分组）从网络（或链路）的一端传送到另一端所需要的总的时间。它由四个部分构成：发送时延、传输时延、处理时延和排队时延。

    以上图中，数据包由路由器A传输到路由器B为例

    - 节点处理时延(nodal processing delay)

        当分组到达路由器A时，首先要做的是检查分组首部并决定将该分组导向何处，并检查比特级差错，这部分的时间消耗叫做处理时延。

    - 排队时延(queuing delay)
        
        分组在经过路由器A的处理后，下一步就是传输出去。一个分组的排队时延取决于先到达的，正在排队等待向链路传输的分组的数量。

        - 如果前面没有分组正在从路由器A向链路传输的话，排队时延为0
        - 如果流量很大，前面有很多分组正在传输或也在等待传输，那么就要消耗很大的排队时延了。

    - 传输时延(transmission delay)
  
        传输时延是路由器A将分组的所有比特推出路由器A，推向链路所需要的时间。传输时延取决于两个因素：

        - 单个分组长度
        - 数据传输速率

        假设分组的长度为L比特，数据传输速率为R (bps) 那么  传输时延 = L/R

    - 传播时延(propagation delay)

        传播时延指的是分组的一个比特从路由器A到达到路由器B所需要的时间，传播时延取决于两个因素：

        - 链路介质（双绞线，光纤）的传播速率
        - 节点间的距离（两个路由器间的距离）

        假设路由A，B距离为d, 链路介质传播速率为s，那么传播时延 = d/s

5. 时延带宽积(Bandwidth-delay Product)

    若发送端连续发送数据，在发送的第一个比特即将到达终点时，表示发送端已经发出的比特数。即，时延带宽积=传播时延*信道带宽。 考虑一个代表链路的圆柱形管道，其长度表示链路的传播时延，横截面积表示链路带宽，则时延带宽积表示该管道可以容纳的比特数量。

6. 往返时延(Round-Trip Time)

    表示从发送端发送数据开始，到发送端收到来自接受段的确认（接收端接受到数据后立即发送确认 ），总共经历的时延。在互联网中，往返时延还包括各中间点的处理时延，排队时延以及转发数据时的发送时延。

7. 丢包率(Packet Loss Rate)

    丢包意为分组丢失，这和排队时延有关。当大量分组在短时间内到达路由器的时候，因为无法一次性处理完毕，分组需要排队，但是基于路由器的设计和成本，分组队列的长度是有限的。所以当队列满了的时候，下一个分组到达的时候，路由器会选择丢弃该分组, 这个分组便丢失了，这就是所谓的丢包

    丢包率与分组长度以及分组发送频率相关。

8. 误码率(Bit Error Rate)
    
    误码率是衡量通信系统传输可靠性的指标，它指的是错误接收的码元数在所传输的总码元数的比例

9. TCP-RR 

    表示在同一次 TCP 长链接中进行多次 Request/Response 通信时的响应效率。TCP-RR 在数据库访问链接中较为普遍

10. UDP-STREAM

    表示 UDP 进行批量数据传输时的数据传输吞吐量，能反映网卡的极限转发能力

11. TCP-STREAM

    表示 TCP 进行批量数据传输时的数据传输吞吐量


## 如何测试网络性能

所使用的工具安装过程省略。

### 1. 网络带宽测试

测试机端:

```
$ iperf3 -s
```

其他机器:

```
$ iperf3 -c ${server ip} -b 2G -t 300 -P ${网卡队列数目}
```

### 2. UDP-STREAM 测试

推荐使用其他八台机器来对测试机进行测试。

netperf 可在 [github: HewlettPackard/netperf][8] 下载

测试机端:

```
$ netserver
$ sar -n DEV 2
```

其他机器:

```
$ ./netperf -H <被测试机器内网IP地址-l 300 -t UDP_STREAM -- -m 1 &
```

### 3. TCP-RR 测试

推荐使用其他八台机器来对测试机进行测试。

测试机端:

```
$ netserver
$ sar -n DEV 2
```

其他机器:

```
$ ./netperf -H <被测试机器内网IP地址-l 300 -t TCP_RR -- -m 1 &
```


以上测试均可以启动多个 <code>netperf</code> 实例

### 4. 网络延迟测试

可以简单地通过 <code>ping</code> 命令得到往返时延和丢包率。

以 www.baidu.com 为例：

```
$ ping www.baidu.com

PING www.a.shifen.com (14.215.177.38): 56 data bytes
64 bytes from 14.215.177.38: icmp_seq=0 ttl=45 time=113.190 ms
64 bytes from 14.215.177.38: icmp_seq=1 ttl=45 time=93.999 ms
64 bytes from 14.215.177.38: icmp_seq=2 ttl=45 time=71.767 ms
64 bytes from 14.215.177.38: icmp_seq=3 ttl=45 time=65.411 ms
64 bytes from 14.215.177.38: icmp_seq=4 ttl=45 time=100.141 ms
64 bytes from 14.215.177.38: icmp_seq=5 ttl=45 time=123.588 ms
^C
--- www.a.shifen.com ping statistics ---
6 packets transmitted, 6 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 65.411/94.683/123.588/20.778 ms
```

## 评价

家用网络现在通常只需要一个调制解调器、路由器二合一的设备就可以满足正常使用需求。

企业级网络就需要专门的机房放置服务器、路由器等各种设备，同时还要保证其高可用性，有多个副本。

至于网络性能问题，为了达到更快的网速，尽量采用光纤等有线连接方式，无线虽然方便，毕竟不如有线更快。

若购买云服务器，尽量选择与目标用户地理位置更近的服务器。比如都是国内用户的话，就购买国内云服务器，而不是境外云服务器。

[1]:https://upload.wikimedia.org/wikipedia/commons/thumb/f/f5/Rack001.jpg/440px-Rack001.jpg
[2]:https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Adsl_connections.jpg/440px-Adsl_connections.jpg
[3]:https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/24-port_3Com_switch.JPG/440px-24-port_3Com_switch.JPG
[4]:https://assets.vonage.com/sfdc/vbs/images/answers/993/networkingguidelines-ss-ideal3.png
[5]:https://3.imimg.com/data3/TV/SD/MY-9106007/hardware-firewall-appliance-500x500.png
[6]:https://ask.qcloudimg.com/http-save/yehe-1148650/q9o2sy9k9e.png?imageView2/2/w/1620
[7]:https://ask.qcloudimg.com/http-save/yehe-1148650/6l1gil2uh3.png?imageView2/2/w/1620
[8]:https://github.com/HewlettPackard/netperf