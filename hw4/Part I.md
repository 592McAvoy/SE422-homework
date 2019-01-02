# prepare a CI/CD environment
在查询了相关资料之后，发现gitlab自己的CI做得已经非常好了，所以这次使用gitlab来搭建CI/CD环境。
主要搭建步骤分两步：
- 为项目注册gitlab-runner
- 创建.gitlab-ci.yml来配置CI的操作

## 为项目注册gitlab-runner
在gitlab上创建项目后，点击settings->CI/CD->runners->expand即可选择为该项目配置specific runners或shared runners。

其中specific runners只能为制定的工程服务，shared runners可以为所有工程服务，但是只有系统管理员才能够创建shared runners。

### gitlab-runner安装过程
搭建环境为Ubuntu 18.04。

首先执行以下指令添加gitlab的官方package。

```
curl -L https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.deb.sh | sudo bash
```

然后安装gitlab-runner并启动。
```
sudo apt-get install gitlab-runner

gitlab-runner run
```
完成相关配置后，可以在repo的设置中看到正在运行的runner:
![](https://github.com/592McAvoy/homework1/blob/master/hw4/CI%20CD/gitlab-runner.png)

## 创建.gitlab-ci.yml来配置CI的操作
### .gitlab-ci.yml介绍
- .gitlab-ci.yml用来配置CI用你的项目中做哪些操作，这个文件位于仓库的根目录。
- 当有新内容push到仓库后，gitlab会查找是否有.gitlab-ci.yml文件，如果文件存在，runners会根据文件的内容开始build本次commit。

.gitlab-ci.yml默认有3个state：build，test，deploy。在CI部分介绍中，首先介绍build和test部分。

### 配置过程
在仓库根目录创建.gitlab-ci.yml文件，并修改内容如图所示。
![](https://github.com/592McAvoy/homework1/blob/master/hw4/CI%20CD/%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6.png)

图上内容表示在每次push后，首先进行执行before_script（在命令行打出“Restoring Packages”），随后执行build_job阶段的script（打出“Release build...”），最后执行test_job阶段的script（打出“Tests run...”）。

如果配置文件格式无误，gitlab将显示“This GitLab CI configuration is valid.”。

### 最终结果
至此gitlab的CI配置流程已经结束，随后在每次push后，gitlab均会根据.gitlab-ci.yml里的相关配置执行对应的操作，完成自动build与test。build与test的结果会显示在每次push之后。
![](https://github.com/592McAvoy/homework1/blob/master/hw4/CI%20CD/commit%E8%87%AA%E5%8A%A8ci.png)
如图显示此时push已经通过build与test。
![](https://github.com/592McAvoy/homework1/blob/master/hw4/CI%20CD/CI%E8%87%AA%E5%8A%A8%E6%90%AD%E5%BB%BA.png)
![](https://github.com/592McAvoy/homework1/blob/master/hw4/CI%20CD/CI%E8%87%AA%E5%8A%A8%E6%B5%8B%E8%AF%95.png)
