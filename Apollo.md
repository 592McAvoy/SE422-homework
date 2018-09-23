# Apollo


 

  A highly scalable and coordinated scheduling framework
 ----
 
## 什么是Apollo 
Apollo是Microsoft旗下的一个共享集群状态的的分布式调度框架。目前，Apollo已被部署在Microsoft的集群生产环境之中，每天负责上万台服务器上数以十亿计的高并发任务的调度和管理。从实际结果来看，Apollo具有很好的可扩展性，稳定性及良好的性能。


----------


## 特性
面对大规模集群调度的挑战，Apollo主要有以下技术特性：


- 采用**分布式** (*distributed*)和 **松散协调** (*loosely coordinated*)的调度框架。每个调度器独立地进行调度，但在做出调度决定之前会综合考虑根据整个集群的资源利用信息。      
· 优点：规避了完全“去中心化”架构所造成的调度冲突问题，同时突破了传统中心式框架的可扩展性瓶颈限制，实现了可扩展性和调度质量的平衡

-  通过**估计模型** (*estimation model*)对任务完成时间进行预估，将每个任务的完成时间最小化。模型中同时考虑数据的局部性、服务器负载和其他各种因素，并根据这些因素进行加权决策。随着调度任务的执行，估计模型还可以通过观测到的类似任务的运行数据来对时间估计策略进行进一步的优化。      
· 优点：对任务完成时间进行了有效的预估，帮助了调度器做出最优的调度决定

- 引入**轻量级的硬件独立机制**来为调度器提供集群中所有服务器上的资源使用情况。每个调度器都拥有整个集群的信息，掌握了未来短期内每个服务器的可利用资源情况，在此基础上再进行调度决策。   
· 优点：避免了因调度任务不均衡，使服务器出现过载或空闲情况

- 提供了一系列的**修正机制** (*correction mechanisms*)，在运行时动态地调整和修正非最优的调度决定。例如，在面对调度冲突时采用延迟修正机制等。    
· 优点：针对集群中可能会出现任务运行时间估计不准确、任务冲突、运行时一些不正常的行为等意外状况做出了及时的处理，避免了任务搁置情况的出现

- 引入了**机会调度** (*opportunistic scheduling*)策略。Apollo将作业分成了两类，常规作业(*regular tasks*)和机会作业(*opportunistic tasks*)，并引入了基于token的机制来管理容量并通过限制常规任务的总数来避免集群的负载过高。     
· 优点：在保证低延迟的同时提高了集群资源的利用率。

- 支持**分阶段部署和验证**。       
· 优点：避免了使用Apollo替代既有框架时对服务和性能造成影响


----------


## 架构设计

![Apollo架构][1]

上图是Apollo的整体架构图。


**Job Manager（JM）**就是一个调度器，它负责对作业进行调。每一个集群都会拥有一个**Resource Monitor（RM）**，每一台服务器都拥有一个**Process Node（PN）**，它们两个协调工作来为调度器提供一个全局的视角，供调度器进行调度决策时使用。每个PN负责对本地服务器的资源进行管理，RM会从集群中每个服务器上的PN那里收集信息，汇总成全局信息后给每个JM。

下图描述了JM,PN和RM之间的通信，展示了Apollo是如何兼顾**分布式调度**和**共享集群状态**两个方面。

![TIM图片20180923153008.png](https://upload-images.jianshu.io/upload_images/14161520-ca9d0ae979fd770f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



----------
## 评价
Apollo的特点在于，它在采用分布式架构的同时，实现了集群状态的共享，既避免了服务器负载不均，又减少了调度冲突，还能获得较高的可扩展性。

然而，我猜想共享状态架构也可能会带来一些问题。因为状态共享基于PN和RM不断反馈运行信息，在高竞争情况下，信息量非常巨大，JM需要耗费额外资源来接受、处理这些信息，反而可能影响整体调度性能。

从总体上看，Apollo是个优秀的集群调度框架。

----------


#### 参考资料：
 1. [Apollo：Scalable and Coordinated Scheduling for Cloud-Scale Computing][2]
 2. [每周论文·Apollo: Scalable and Coordinated Scheduling for Cloud-Scale Computing][3]
 3.  [集群调度框架的架构演进之路][4]
 4.  [十大主流集群调度系统大盘点][5]


  [1]: http://m.qpic.cn/psb?/V13Ti98m05LW5b/VKONLDuOCi6o0pzkGE2pRVUZG1yKdAStt9UfBXWD2wk!/b/dDQBAAAAAAAA&bo=ggPwAgAAAAADB1E!&rf=viewer_4
  [2]: https://www.usenix.org/conference/osdi14/technical-sessions/presentation/boutin
  [3]: https://blog.csdn.net/violet_echo_0908/article/details/78174782
  [4]:http://developer.51cto.com/art/201603/507376.htm
  [5]:https://blog.csdn.net/vip_iter/article/details/80123228
