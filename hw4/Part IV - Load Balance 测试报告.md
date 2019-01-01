# Part IV - Load Balance 测试报告


---

## 测试环境 ##

 - 本测试在虚拟机Ubuntu 14.04中进行，处理器核数为4核，内存容量为10G  
 - Kubernetes集群通过minikube构建，集群中运行了一个bookstore网页应用，前端和数据库service对外暴露端口。

集群中共部署了三个service：front（front-end），bookstore-back（back-end）和mysql（database）

    $ kubectl get service
    NAME            TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
    bookstore-back   ClusterIP   10.99.195.117   <none>        8080/TCP         6h
    front            NodePort    10.109.25.130   <none>        8080:32008/TCP   6h
    kubernetes       ClusterIP   10.96.0.1       <none>        443/TCP          4d
    mysql            NodePort    10.102.177.13   <none>        3306:32006/TCP   6h


每一个service都由对应的ReplicaController来对副本的数量进行监控和调整

    $ kubectl get rc
    NAME       DESIRED   CURRENT   READY     AGE
    back-rc    1         1         1         5h
    front-rc   10        10        10        5h
    mysql-rc   1         1         1         5h



----------
## 实验设计 ##

 - 测试工具：Jmeter 
 - 测试样例：设置10000个线程，对front
   service的/和/like页面持续发送30s请求，测量不同数量的front replica下的服务性能 
 - 测试数量：对replica =   1，2，5，7，10五种情况进行了测试

----------
## 测试结果 ##

![测试数据][1]


----------


## 测试分析 ##
### 1. Throughput（RPS） ###
![RPS][2]     

可见replica数量从1增加为2时性能获得了急剧的提升，replica数量为5时达到RPS的最高峰，在此之后虽然replica数量上升，但是分发请求和维护replica的额外开销对整体性能造成了影响

### 2. Response Time ###
![response time][3]      

可见response time也随replica数量增多而出现先下降后上升的情况，与RPS测试结果一致，在replica=5时响应最迅速，但是值得留意的是，replica=10的平均响应时间比为1时还要长，可见均衡负载尺度过大时，反而会对用户体验造成不好的影响 

### 3. Error ###
![error][4]    

可见replica数目过多或过少时出错率都较高，分析原因：
 - replica少时，单个服务器负载过大，因而易出错
 - replica多时，controller需要监控维护很多服务的状态并分发请求，整个集群为了维持大量的服务器也需要额外耗损很多资源，因此容易出错

  [1]: http://m.qpic.cn/psb?/V13Ti98m05LW5b/Py5QtAcfJBJqIySqgMZ.KO7POmmQkr6p2rT8n4fDG9Q!/b/dLYAAAAAAAAA&bo=QwZyAQAAAAADBxQ!&rf=viewer_4
  [2]: http://m.qpic.cn/psb?/V13Ti98m05LW5b/0V3G8dHw03MlXQ20tdbITwYfE3TjCd9bd*NNxeQvK.s!/b/dMAAAAAAAAAA&bo=8ALDAQAAAAADFwI!&rf=viewer_4
  [3]: http://m.qpic.cn/psb?/V13Ti98m05LW5b/oFLVEwV9Jay9FBjalaKnt5X8O.D*IjlUwCNN2xnKwJc!/b/dL8AAAAAAAAA&bo=8ALDAQAAAAADBxI!&rf=viewer_4
  [4]: http://m.qpic.cn/psb?/V13Ti98m05LW5b/W36vk5HKe0nGoQ4doRH6tHFQmtW8a5TN2LW*eLE.2gY!/b/dMMAAAAAAAAA&bo=8ALDAQAAAAADBxI!&rf=viewer_4
