# Ceph
## 什么是Ceph
Ceph是一种为优秀的性能、可靠性和可扩展性而设计的统一的、分布式的存储系统。

具体而言，“统一的”意味着Ceph可以一套存储系统同时提供对象存储、块存储和文件系统存储三种功能，以便在满足不同应用需求的前提下简化部署和运维。而“分布式的”在Ceph系统中则意味着真正的无中心结构和没有理论上限的系统规模可扩展性。在实践当中，Ceph可以被部署于上千台服务器上。截至2013年3月初，Ceph在生产环境下部署的最大规模系统为Dreamhost公司的对象存储业务集群，其管理的物理存储容量达到了3PB。

### Ceph核心组件及概念介绍
![img](https://images2017.cnblogs.com/blog/1109179/201711/1109179-20171106211611450-2111366494.png)
#### Monitor
一个Ceph集群需要多个Monitor组成的小集群，它们通过Paxos同步数据，用来保存OSD的元数据。

#### OSD
OSD全称Object Storage Device，也就是负责响应客户端请求返回具体数据的进程。一个Ceph集群一般都有很多个OSD。

#### MDS
MDS全称Ceph Metadata Server，是CephFS服务依赖的元数据服务。

#### Object
Ceph最底层的存储单元是Object对象，每个Object包含元数据和原始数据。

#### PG
PG全称Placement Grouops，是一个逻辑的概念，一个PG包含多个OSD。引入PG这一层其实是为了更好的分配数据和定位数据。

#### RADOS
RADOS全称Reliable Autonomic Distributed Object Store，是Ceph集群的精华，用户实现数据分配、Failover等集群操作。

#### Librados
Librados是Rados提供库，因为RADOS是协议很难直接访问，因此上层的RBD、RGW和CephFS都是通过librados访问的，目前提供PHP、Ruby、Java、Python、C和C++支持。

#### CRUSH
CRUSH是Ceph使用的数据分布算法，类似一致性哈希，让数据分配到预期的地方。

#### RBD
RBD全称RADOS block device，是Ceph对外提供的块设备服务。

#### RGW
RGW全称RADOS gateway，是Ceph对外提供的对象存储服务，接口与S3和Swift兼容。

#### CephFS
CephFS全称Ceph File System，是Ceph对外提供的文件系统服务。

## 特点
### 高性能
- 摒弃了传统的集中式存储元数据寻址的方案，采用CRUSH算法，数据分布均衡，并行度高。
- 考虑了容灾域的隔离，能够实现各类负载的副本放置规则，例如跨机房、机架感知等。
- 能够支持上千个存储节点的规模，支持TB到PB级的数据。

### 高可用性
- 副本数可以灵活控制。
- 支持故障域分隔，数据强一致性。
- 多种故障场景自动进行修复自愈。
- 没有单点故障，自动管理。

## 高可扩展性
- 去中心化。
- 扩展灵活。
- 随着节点增长而线性增长。

## 特性丰富
- 支持三种存储接口：块存储、文件存储、对象存储。
- 支持自定义接口，支持多种语言驱动。

## 架构
![img](https://ss.csdn.net/p?https://mmbiz.qpic.cn/mmbiz_png/icNyEYk3VqGk91oZGzW0jMNv73lKibM81QhjcewG8mWGufpxnich313icS4HGmxNIzYyuIprM5TxmXkO7xjoRbyvog/640?wx_fmt=png)
如图所示，Ceph支持三种接口：
- Block：支持精简配置、快照、克隆。
- File：Posix接口，支持快照。
- Object：有原生的API，而且也兼容Swift和S3的API。

### 块存储
![img](https://ss.csdn.net/p?https://mmbiz.qpic.cn/mmbiz_png/icNyEYk3VqGk91oZGzW0jMNv73lKibM81QE6EUHFUa27icXn4tP6EjjMnmKbmPoZibVoIs3nl49Whzh3r3xeOypGuQ/640?wx_fmt=png)
典型设备：磁盘阵列，硬盘。
主要是将裸磁盘空间映射给主机使用。

#### 优点：
- 通过Raid与LVM等手段，对数据提供了保护。
- 多块廉价的硬盘组合起来，提高容量。
- 多块磁盘组合出来的逻辑盘，提升读写效率。

#### 缺点：
- 采用SAN架构组网时，光纤交换机，造价成本高。
- 主机之间无法共享数据。

#### 使用场景：
- docker容器、虚拟机磁盘存储分配。
- 日志存储。
- 文件存储。
- ……

### 文件存储
![img](https://ss.csdn.net/p?https://mmbiz.qpic.cn/mmbiz_png/icNyEYk3VqGk91oZGzW0jMNv73lKibM81Qicfib5EPlj7hfohLckHyUTZIlr5WrDmw2GvuXLPc2r1LUnKoiaica9ZVQg/640?wx_fmt=png)
典型设备：FTP、NFS服务器
为了克服块存储文件无法共享的问题，所以有了文件存储。
在服务器上架设FTP与NFS服务，就是文件存储。

#### 优点：
- 造价低。
- 方便文件共享。

#### 缺点：
- 读写速率低。
- 传输速率慢。

#### 使用场景：
- 日志存储。
- 有目录结构的文件存储。
- ……

### 对象存储
![img](https://ss.csdn.net/p?https://mmbiz.qpic.cn/mmbiz_png/icNyEYk3VqGk91oZGzW0jMNv73lKibM81Q8go0TCzngrZmNa4qof0wFJcqabowz5quM1mSSSPliaiaiar2Uw3PWIyjA/640?wx_fmt=png)
典型设备： 内置大容量硬盘的分布式服务器(swift, s3)
多台服务器内置大容量硬盘，安装上对象存储管理软件，对外提供读写访问功能。

#### 优点：
- 具备块存储的读写高速。
- 具备文件存储的共享等特性。

#### 使用场景： (适合更新变动较少的数据)
- 图片存储。
- 视频存储。
- ……

## Ceph IO流程及数据分布
![img](https://ss.csdn.net/p?https://mmbiz.qpic.cn/mmbiz_png/icNyEYk3VqGk91oZGzW0jMNv73lKibM81QB28g0d4YL1efUDyTjglTuYyT4qJibQM3pCQkASGquwicftaJ1HkILapA/640?wx_fmt=png)

### 正常IO流程图
![img](https://ss.csdn.net/p?https://mmbiz.qpic.cn/mmbiz_png/icNyEYk3VqGk91oZGzW0jMNv73lKibM81QdPp686PopXr4JB0vxFdJfAITHhUBnibISkzHoVoz4P76bpVvF4dRTIw/640?wx_fmt=png)

#### 步骤：
- client 创建cluster handler。
- client 读取配置文件。
- client 连接上monitor，获取集群map信息。
- client 读写io 根据crshmap 算法请求对应的主osd数据节点。
- 主osd数据节点同时写入另外两个副本节点数据。
- 等待主节点以及另外两个副本节点写完数据状态。
- 主节点及副本节点写入状态都成功后，返回给client，io写入完成。

### 数据分布
#### Ceph Pool和PG分布情况
![img](https://ss.csdn.net/p?https://mmbiz.qpic.cn/mmbiz_png/icNyEYk3VqGk91oZGzW0jMNv73lKibM81Qv4kuu5tIG1WmrBowssMa5NqyVwOreM9wvk6bU44q6vE13rO3sdZsZA/640?wx_fmt=png)

- pool是ceph存储数据时的逻辑分区，它起到namespace的作用。
- 每个pool包含一定数量(可配置)的PG。
- PG里的对象被映射到不同的Object上。
- pool是分布到整个集群的。
- pool可以做故障隔离域，根据不同的用户场景不一进行隔离。

#### Ceph数据扩容PG分布
##### 场景数据迁移流程：
- 现状3个OSD, 4个PG
- 扩容到4个OSD, 4个PG

##### 现状：
![img](https://ss.csdn.net/p?https://mmbiz.qpic.cn/mmbiz_png/icNyEYk3VqGk91oZGzW0jMNv73lKibM81QeXpKERorhVFPAlt8Mlcice0Su7A0h7ic524HohZT34eAryKzTjuU1xTA/640?wx_fmt=png)

##### 扩容后：
![img](https://ss.csdn.net/p?https://mmbiz.qpic.cn/mmbiz_png/icNyEYk3VqGk91oZGzW0jMNv73lKibM81QMEAuXzdQqtYqRuCenPBAINFiaS3lstEHKkgQJiaRFic6kKAYoia8PDEicEA/640?wx_fmt=png)

每个OSD上分布很多PG, 并且每个PG会自动散落在不同的OSD上。如果扩容那么相应的PG会进行迁移到新的OSD上，保证PG数量的均衡。

## 评价
### 优点
作为一个分布式文件系统，Ceph的优点是显然的：
- 扩展性高。在需要扩容的时候，直接加入一台机器或者存储设备即可。
- 平衡存储负载。对于单机的存储情况，假设A地区的信息都存储在A地区的设备上，很可能导致地区服务器的存储负载严重不平衡，造成资源浪费现象。分布式的文件系统更能平衡各服务器的存储负载。
- 具有fault tolerance的能力。在分布式文件系统的情况下，即便是有一台服务器挂掉，别的服务器可以暂时分担这台服务器的业务，而不用担心数据丢失（因为有replica的存在）。
- 可以实现更大容量的存储。由于分布式文件系统是建立于各个分散存储设备之上，所以可以实现更大容量得存储（PB级别）。

### 缺点
由于要保证一致性，Ceph通过Paxos协议来保证数据一致性，这期间可能需要时间较长的网络通信。在IO流程图中可以看到，当client发送请求后，Primary需等到Replica都成功提交后才能将结果返回给client，相较于单机来说，用户等待的latency会变高。
同时由于数据不在只存在于一台单机上，primary在处理请求时可能也需要访问远端的数据，同样会增加耗时和latency。
