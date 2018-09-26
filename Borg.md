# Borg
## 一、Borg是什么

Borg是由Google开发的第一个集群管理工具，或者说容器管理工具。
Borg可以同时运行数以十万计的job，这些job可以来自上千个不同的应用，并且跨越多个集群，每个集群又可以由上万机器组成。

Borg的设计初衷，就是为了让开发者能够专注于业务开发，而不用担心资源管理问题，并做到 **集群管理资源利用最大化** 。

Borg作为第一个集群管理工具，在如今的集群管理工具之中可以看到Borg一些设计的影子。



## 二、Borg的历史背景

在Borg诞生之前，对于服务的管理由Babysitter解决，同时使用Global Work Queue来管理batch job。但是Google公司对于容器技术的持续研究，并付诸实践，修改inux内核使之能够直接对容器提供良好的支持，为用户服务与CPU-hungry的进程提供了良好的隔离性。在这块基石之上，Borg诞生了，它基于进程级别性能隔离的机器共享这一特性，大幅提高了services与batch jobs在集群管理时的资源利用率，减小了开销。

## 三、用户眼中的Borg

用户使用Borgcfg（命令行）或者Web UI提交需要跑的应用（Task） 到系统，Task可以是任何一种东西，比如说他是一个应用程序，或者是一个批处理任务，或者是一个（MR）的任务。他把这个任务通过Borgcfg提交到BorgMaster，然后BorgMaster会接受这个请求，把请求放到队列里面去，并由Scheduler来扫描这个队列，查看这个应用的资源需求，并在集群中寻找匹配的机器。

### 1、工作负载

borg上运行的服务通常可以分为两类：

- prod：长时间运行服务，延迟敏感，如gmail，google docs，google搜索等
- non-prod：batch job，时延不敏感，通常几小时或者几天即可跑完


### 2、集群和cell

　　一个cell中的机器通常属于单个集群，并且由数据中心规模的高性能网络结构连接起来。一个集群通常存在于单个数据中心里，而多个数据中心的集合构成了一个site。一个集群通常包含一个大的cell，也许其中还有一些小规模用于测试或者其他特殊目的的cell。我们总是极力避免单点故障发生。


### 3、job和task

　　job的属性包括：名称，owner，tasks，同时还包括一些调度的约束条件，例如处理器架构，os版本，ip地址等等，这些会影响borg-master调度的结果，当然这些条件不一定是强制约束的，分hard和soft两种。

一个job只能跑在一个cell里，每个job会有N个task，每个task运行期间会有多个进程，google并没有使用虚拟机的方式来进行task之间的资源隔离，而是使用轻量级的容器技术cgroup。

task也有自己的属性：资源需求和一个index，大部分时候一个job里的所有task的资源需求都是一样的。

下图展示了job和task运行走完它们整个生命周期的过程。

![](https://images2015.cnblogs.com/blog/685359/201604/685359-20160408145657390-1699309036.png)

 ### 4、allocs

　　Borg的alloc操作是指在一台机器上预留一些资源，从而能够在其上运行一个或者多个资源；这些资源不管是否被使用都是保持被分配状态的。Allocs操作可以被用来保留资源用于未来task的使用，也可以用于在停止以及启动一个task之间保存资源，还可以用于将不同job里的task收集起来，让它们运行在同一台机器中：比如一个web服务器实例以及相关的用于将本地磁盘的服务器URL记录拷贝到分布式文件系统的task。被alloc操作之后的资源和机器中的其他资源是被同等对待的，运行在同一个alloc操作之上的多个task共享其中的资源。如果一个alloc操作必须被重定向到另一台机器上，那么之上的任务就必须随着alloc操作被重新调度。

　　一个alloc集就像是一个job：它是一系列的alloc操作用于在多台机器上预留资源。一旦一个alloc操作被创建，一个或多个job就能被提交并且运行在它之上。简单起见，我们一般用“task”来代之一次alloc操作或者顶层的task（一个在alloc操作之外的task），而“job”指一个job或者一个alloc操作集。

### 5、优先级，配额以及准入控制

　　如果出现了超出处理能力的负载怎么办？我们的解决方法是优先级和配额。

　　- 优先级（priority）
    
    也就是一个小的正整数。一个高优先级的task可以以牺牲另一个较低优先级的task为代价来获取资源，即使这种牺牲包括抢占或者杀死较低优先级的task。

　　- 配额（quota）
 
    表示哪些job能够被调度。配额我们可以理解为在给定优先级下的资源请求向量（CPU，RAM，磁盘等等）。资源请求是指在一段时间内，一般是一个月内，一个用户的job能请求的最大资源数目（比如一个prod请求了20TB的RAM，时间是从现在到七月份，在XX cell中）。配额检查也是准入控制的一部分，而不是调度：一个配额要求未被满足的job是会被立刻拒绝的。

    - 准入控制 (admission control)
    Borg还有一个容量系统，它能给予一些用户以特殊的权限：比如允许管理员删除或修改cell里任意的job，或者运行用户访问限制的内核特性或者Borg的行为，例如在他们的job中禁用资源限制。

### 6、命名以及监控

类似于微服务架构中的服务发现

Borg为每个task创造了一个叫”Borg name service“(BNS)类型的名字，这个名字中包含了cell的名字，job的名字以及task的编号。Borg会将task的主机名，端口号以及这个BNS名字写入Chubby里面一个一致的，高可用的文件中，而这个文件通常被我们的RPC系统用于查找task。BNS名字同样被用作task的DNS名字基础，因此对于用户ubar拥有的一个在叫做cc的cell中的一个叫jfoo的job中的第五十个task，我们就可以通过域名50.jfoo.ubar.cc.borg.google.com访问到。同时Borg会在job的大小或者task的健康状况改变时将它们写入Chubby中，之后负载均衡器就能决定将请求路由到什么地方了。

几乎Borg之下运行的每一个task都有一个内置的HTTP server用于发布task的健康状况以及其他许多的性能指标（RPC延迟等等）。Borg会监视健康检查的URL并且会重启那些没有即使回复的task或者直接返回一个HTTP 错误代码。其他数据通过另外一些监控工具进行监控，并且对服务对象级别的违规行为进行报警。

Borg会记录所有的job提交情况，task事件，以及Infrastore中详细的task执行前的资源使用情况。Infrastore是一个有着类SQL接口的可扩展只读数据存储。这些数据被用作基于使用的计费，调试，系统错误以及长期的容量计划。同时，它们也为Google的集群负载追踪提供了数据。

## 四、架构

一个Borg的cell由一系列的机器组成，通常在cell运行着一个逻辑的中央控制器叫做Borgmaster，在cell中的每台机器上则运行着一个叫Borglet的代理进程。

![borg-architecture](https://res.infoq.com/news/2015/04/google-borg/zh/resources/345.png)

### 1、Borgmaster

　　每个cell的Borgmaster主要由两个进程组成：一个主Borgmaster进程以及一个分离的调度器。主Borgmaster进程用于处理各种客户的RPC请求，这些请求无非包括状态变更（用于创建job）或者对数据的只读访问（用于查询的job）。它还用于管理系统中各个对象（机器，task，alloc等）的状态机，和Borglets之间的交互。。

### 2、调度

　　当一个job被提交的时候，Borgmaster会将该job中的task都加入挂起队列中。这些都是由调度器异步扫描完成的，它会在有足够资源并且符合job的限制条件的时候将task部署到机器上。（调度器主要操作的是task，而不是job）。扫描根据优先级从高到底进行，在同一优先级内按照轮转法进行调节从而确保各用户间的公平性并且避免大型job的头端阻塞。调度算法主要由两部分组成：feasibility checking，用于发现task可以运行的机器，和scoring，选取其中一个可行的机器。

### 3、Borglet

　　　Borglet是一个本地的Borg代理，它会出现在cell中的每一台机器上。它启动，停止task；在task失败的时候重启它们，通过控制操作系统内核设置来管理本地资源以及向Borgmaster和其他监视系统报告机器状态。

　　Borgmaster每过几分钟就轮询每个Borglet获取机器的当前状态，同时向它们发送外部的请求。这能够让Borgmaster控制交互的速率，避免了显示的流量控制和恢复风暴。

# 五、对现代集群管理工具的影响

以上是我个人对于Borg与当今我接触过的集群管理工具的一些对比和感想。

作为第一个集群管理工具Borg对现在的框架工具也很有影响。

Borg基于lxc container，而Kubenetes基于docker container，两者毕竟都出自于Google工程师之手，整体上十分相似。

可能最开始会觉得Borg中job的概念对应于Kubernetes中的pod。

但是job只是逻辑上的概念，Borg实际调度的是task，这跟rancher自己的调度框架cattle是类似的。cattle的一个Application（对应Borg的job）可以包括很多container（对应Borg的task），实际调度的是其中的container。

实际上与pod对应的是borg中的alloc。同一个pod中的docker container共享network namepace和volume，container之间使用localhost通信，被当作一个整体被Kubernetes调度。

而目前Kubenetes也不支持batch job

其中BorgMaster 与 Borglet的主从设计也能在rancher中看到影子。rancher部署集群时，也是先将一台机器作为master节点，之后陆续将其他节点加入，从master节点管理其他子节点。并且rancher加入子节点后，也会自动为其部署健康状态检查等基础设施。

#### 参考资料：
 1. [Large-scale cluster management at Google with Borg][1]
 2. [译：Google的大规模集群管理工具Borg][2]
 3.  [Borg, Omega, and Kubernetes][3]

  [1]: https://storage.googleapis.com/pub-tools-public-publication-data/pdf/43438.pdf
  [2]: https://www.cnblogs.com/YaoDD/p/5351589.html
  [3]: https://queue.acm.org/detail.cfm?id=2898444

