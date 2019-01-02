# prepare a CI/CD environment
本次CI/CD环境搭建选择drone+github，实现了在每次git push之后，drone能够监测到这个push，同时根据repo里.drone.yml的配置进行对应的操作。

具体步骤如下：
- 开启drone监控对应repo
- 修改drone设置
- 修改.drone.yml配置文件

## 开启drone监控对应对应repo
在安装drone后，会显示对应的web界面，用github账号登录即可。

登录后，会显示该账号下的repo列表。在列表中可以选择drone监控哪些repo。在本次实验中，新建了CI-CDtest仓库，用于准备CI/CD环境。

如图所示即可开启drone对CI-CDtest仓库的监控。
![](https://github.com/592McAvoy/homework1/blob/master/hw4/CI%20CD/CI%E6%B5%8B%E8%AF%95.png)

## 修改drone设置
修改drone内目标仓库的设置，使得每次push/pull request/deployment时drone都会进行对应操作。
![](https://github.com/592McAvoy/homework1/blob/master/hw4/CI%20CD/drone%E8%AE%BE%E7%BD%AE.png)

## 修改.drone.yml配置文件
当drone监控到对应仓库的一个动作时，会根据.drone.yml的内容进行对应的动作。

为了实验简单，在本次实验中仅进行build部分的动作，动作为在命令行打出"start build..."。

配置内容如下：
```
workspace:
  base: /test
  path: src/github.com/derFischer/CI-CDtest
pipeline:
  build:
    image: maven:3.6.0-jdk-8-alpine
    commands:
      - echo "start build..."
```
在配置后，每当drone监控到一个动作，就会在build的image下执行对应动作（此处为echo "start build..."）。

尝试对这个仓库进行commit，drone在监测到后成功执行了对应动作。
![](https://github.com/592McAvoy/homework1/blob/master/hw4/CI%20CD/CI%E6%B5%8B%E8%AF%95%E6%88%90%E5%8A%9F.png)

# 使用drone对web应用进行自动打包至docker hub
通过配置.drone.yml文件，可以实现drone在监测到仓库行为后自动搭建并打包项目至docker hub。

本次实验在derFischer/swms-frontend（web应用的前端部分）和derFischer/swms-backend（web应用的后端部分）这两个仓库进行。

开启监控与drone设置如上一部分所述。

在修改配置文件时，由于前端和后端部分需要在不同的镜像中安装必要的文件，所以build的阶段需要做对应修改。同时还需增加publish阶段来进行打包。

swms-frontend的配置文件修改如下：
```
workspace:
  base: /front
  path: src/github.com/derFischer/swms-frontend
pipeline:
  build:
    image: node:latest
    commands:
      - npm install
      - npm run-script build
  publish:
    image: plugins/docker
    repo: dingd/swmsfrontend
    tags: ["latest", "v2"]
    secrets: [ docker_username, docker_password ]
    dockerfile: Dockerfile
```
其中publish的image是drone所写的插件，可以方便地把项目打包至docker hub。repo指定了打包的地址，secrets指定了docker用户名与密码。

build的commands阶段，依前端要求增加了npm install和npm run-script build。


swms-backend的配置文件修改如下：
```
workspace:
  base: /back
  path: src/github.com/derFischer/swms-backend
pipeline:
  build:
    image: maven:3.6.0-jdk-8-alpine
    commands:
      - mvn install
  publish:
    image: plugins/docker
    repo: dingd/swmsbackend
    tags: ["latest", "v2"]
    secrets: [ docker_username, docker_password ]
    dockerfile: Dockerfile
```
修改与frontend类似。

# 示例
在对swms-frontend仓库进行push后，drone成功监控到了这个行为，同时进行build和publish操作，并将打包内容上传至了docker hub上。
![](https://github.com/592McAvoy/homework1/blob/master/hw4/CI%20CD/CD%E8%87%AA%E5%8A%A8%E6%89%93%E5%8C%85%E5%89%8D%E7%AB%AFpush.png)
swms-frontend与swms-backend的CI/CD环境均测试成功。
