# Borg
## 一、Borg是什么

Borg是由Google开发的第一个集群管理工具，或者说容器管理工具。
Borg可以同时运行数以十万计的job，这些job可以来自上千个不同的应用，并且跨越多个集群，每个集群又可以由上万机器组成。

Borg的设计初衷，就是为了让开发者能够专注于业务开发，而不用担心资源管理问题，并做到 **集群管理资源利用最大化** 。

Borg作为第一个集群管理工具，在如今的集群管理工具之中可以看到Borg一些设计的影子。



## 二、Borg的历史背景

在Borg诞生之前，对于服务的管理由Babysitter解决，同时使用Global Work Queue来管理batch job。但是Google公司对于容器技术的持续研究，并付诸实践，修改inux内核使之能够直接对容器提供良好的支持，为用户服务与CPU-hungry的进程提供了良好的隔离性。在这块基石之上，Borg诞生了，它基于进程级别性能隔离的机器共享这一特性，大幅提高了services与batch jobs在集群管理时的资源利用率，减小了开销。

## 三、如何使用Borg

用户使用Borgcfg（命令行）或者Web UI提交需要跑的应用（Task） 到系统，Task可以是任何一种东西，比如说他是一个应用程序，或者是一个批处理任务，或者是一个（MR）的任务。他把这个任务通过Borgcfg提交到BorgMaster，然后BorgMaster会接受这个请求，把请求放到队列里面去，并由Scheduler来扫描这个队列，查看这个应用的资源需求，并在集群中寻找匹配的机器。

![borg-architecture](https://res.infoq.com/news/2015/04/google-borg/zh/resources/345.png)

## 四、特点

    作为第一个集群管理工具，他的很多设计上的特点都影响着之后的工具。

  - 稳定性、高可用性、资源利用率
   
    Borg已经在Google内部使用很长时间，Gmail、Google Compute Service等都稳定运行于其上，足以说明Borg在性能各方面的极大优势。

  - 可扩展性

    MapReduce system, FlumeJava, Millwhee等框架都在Borg中投入使用，易于扩展。

    ````"We are not sure where the ultimate scalability limit to Borg's centralized architecture will come from; so far, every time we have approached a limit, we've managed to eliminate it."````

    以上是Google工程师对于Borg的可扩展性的评价，足以说明Borg强大的可扩展性。

  - 资源调度
    
    Borg中运行的服务，会根据优先级、配额、准入控制等来进行资源的分配调度，保证最大化利用集群资源。之后出现的集群管理框架也围绕这一点做出自己的设计。

  - Job & Task
    
    Job只是逻辑上的概念，是Task的集合，Borg实际调度的是task。

    这与Rancher默认的轻量级调度框架Cattle是类似的。Cattle的一个Application（对应Borg的Job）可以包括很多Service（对应Borg的task），实际调度的是其中的Service。

  - Alloc
  
    Alloc与如今最流行的开源集群框架Kubernetes中的Pod是相对应的。同一个Pod中的容器共享Network Namepace和Nolume，它们被当作一个整体被调度。

  - BorgMaster & Borglet

    Borg的每一个集群，都有一个BorgMaster作为主节点（其实有五个副本），集群中的每一台机器都有一个Borglet从节点。由BorgMaster管理Borglet。
    
    Cattle集群也类似，不过主节点只有一个，其他机器均为从节点。

  - 资源监控

    Borg中的每个Task都会内置HTTP Server向外发布资源占用信息等。
    
    现在大多数框架也都有该功能，能够监控每个容器运行情况，或者是每个节点的运行情况。

  - 健康检查
    
    Borg中的Task还有一个向外发布健康信息的Url，会重启那些没有即使回复的Task或者直接返回一个HTTP 错误代码。其他数据通过另外一些监控工具进行监控，并且对服务对象级别的违规行为进行报警。

    如今的很多框架也具备这个功能，监控健康情况，并作出相应的措施。

  - 服务发现

    Borg中为每个Task取了一个BNS(Borg Name Service)名字。这个名字中包含了Cell的名字、job的名字、Task的编号。同时Borg会将Task的主机名，端口号以及它的BNS写入Chubby里面一个一致的，高可用的文件中，而这个文件通常被我们的RPC系统用于查找Task。

    在Kubernetes中本身使用环境变量和DNS来实现服务发现。不过可能现在更多的在Kubernetes中使用Istio微服务框架。

## 五、Borg的影响

作为第一个集群管理框架，而且是Google工程师多年的经验积淀产物、经过了Google一线产品的检验，性能对于大多数小项目来说可以说是是过于强大。它的种种设计上都充分解决了运维管理的各种痛点。各种设计也都被其他集群管理框架沿用至今，这在第四部分中已经阐述过。

Kubernetes作为Borg的后继者，与Borg在使用上也十分相似。不过毕竟Borg在Google内部使用多年，经过Google工程师不断地优化，它的性能说是爆炸也不为过，能够同时管理多个上万台机器的集群，这是Kubernetes不能媲美的。

Borg的强大性能是为Google这么庞大的一个公司量身定制的产物，但是世界上大部分用户也并不需要像Borg那么强大的性能，更多的开发者还是需要一个比Borg轻量但也足够强大的集群框架，也就是Kubernetes。

#### 参考资料：
 1. [Large-scale cluster management at Google with Borg][1]
 2. [译：Google的大规模集群管理工具Borg][2]
 3. [Borg, Omega, and Kubernetes][3]
 4. [Kubernetes: Twelve Key Features][4]

  [1]: https://storage.googleapis.com/pub-tools-public-publication-data/pdf/43438.pdf
  [2]: https://www.cnblogs.com/YaoDD/p/5351589.html
  [3]: https://queue.acm.org/detail.cfm?id=2898444
  [4]: https://medium.com/@abhaydiwan/kubernetes-introduction-and-twelve-key-features-cdfe8a1f2d21

