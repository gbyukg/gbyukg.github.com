---
title: "AIX System Upgrade"
date: 2018-02-22T14:25:05+08:00
tags:
  - AIX
categories:
  - AIX
  - DevOps
---

AIX 系统升级还是比较方便，本文将简单介绍如何通过 AIX 的图形界面工具 `smitty` 来安装。
</br>

系统环境：
当前系统版本为： `7100-03-05-1524`
目标版本为：`7100-04-02-1614`

## 获取安装补丁
### 从 IBM Fix Center 下载补丁
在安装系统补丁时，首先需要获取系统升级补丁，对于非 IBM 内部服务器来说，通常我们可以到 [IBM Fix Center](http://www-933.ibm.com/support/fixcentral/main/System+p/AIX) 网站中获取到对应的补丁文件。
</br>

<!-- more -->

**1. 首先选择适当的操作系统**
![This is an image](/img/devops/download-aix-patch-1.png)

**2. 选择对应的版本信息，点击 continue 进入到补丁列表页**
![This is an image](/img/devops/download-aix-patch-2.png)

**3. 下载所需的补丁**
![This is an image](/img/devops/download-aix-patch-3.png)
</br>

### 直接将含有补丁的系统挂在到本地
对于 IBM 内部系统来说，我们可以直接挂载 `rtpmsa` 服务器到本地，来获取补丁文件：

``` sh
mount rtpmsa.raleigh.ibm.com:/msa/.projects/p10/ibmpublic /mnt
```

## 安装前的准备
在开始安装补丁之前，还要确保当前系统中没有任何 installp 文件锁存在，可以通过下面命令查看当前系统中存在哪些 installp 锁：

``` sh
/usr/sbin/emgr -P
```

![This is an image](/img/devops/aix-installp-locks.png)
</br>

上图说明当前我们的系统中存在 6 个 installp 文件锁，在安装之前我们需要确保这些所全部被释放掉：

``` sh
# 释放锁 IV69033s9a
/usr/sbin/emgr -r -L IV69033s9a

# 释放后确认是否还有锁存在
/usr/sbin/emgr -P
```

重复上述指令，直到所有的锁全部为释放掉。

## 安装补丁
当所有锁全部被释放掉后，就可以升级 AIX 系统了，首先进入到补丁目录，这里我们是通过挂载的方式获取补丁的，因此进入到挂在目录：
``` sh
cd /mnt/inst.images/aix/7.1/7100-04-03.2-1642_full

# 启动 smitty
smitty
```

smitty 启动以后，依次按照下图安装补丁：

![This is an image](/img/devops/aix-upgrade-step-1.png)
</br>
![This is an image](/img/devops/aix-upgrade-step-2.png)
</br>
![This is an image](/img/devops/aix-upgrade-step-3.png)
</br>
因为我们已经进入到补丁目录，因此这里的路径选择当前路径 `./` 即可
![This is an image](/img/devops/aix-upgrade-step-4.png)
</br>

选择接受 license：
将光标移动到 `ACCEPT new license agreements?`，按下 `Tab` 键切换成 Yes 即可
![This is an image](/img/devops/aix-upgrade-step-5.png)
</br>

按下 `Enter` 键，弹出确认框，再次按 `Enter` 键，开始安装。过程可能需要会持续十几到几十分钟，慢慢等待。
</br>

出现下图，表明安装成功。
![This is an image](/img/devops/aix-upgrade-step-6.png)
</br>

最后重启系统
``` sh
reboot
```
