---
title: "DB2 大版本升级"
date: 2018-01-31T16:16:09+08:00
tags:
  - DB2
  - DevOps
categories:
  - DevOps
  - 数据库
---

一不小心，又到了 DB2 升级的时候了😂 。每次升级过程中总是会遇到各种各样的升级问题，这次终于下定决心记录下所有升级步骤，以便供下次升级参考使用。
</br>

# #安装 DB2

本次升级是将 DB2 从V10.5 升级到 V11，属于大版本升级，不同于小版本的升级，小版本直接升级数据库文件（`/opt/IBM/db2/V10.5`）和实例即可。而对于大版本升级来说，首先要在系统上安装新版的数据库，新版本数据库的安装并不会对系统中的老版数据库造成任何影响，因为新版本数据库将会被安装在另一个独立的目录中，当新版数据库安装完成后，在对当前系统中的实例以及实例下的数据库进行升级。

### 安装前的检测

在安装 DB2 之前，对系统环境进行检测是很有必要的，这可以帮助我们快速查看当前系统是否满足安装某个 DB2 版本的必要条件。检查脚本 `db2prereqcheck` 可以在 DB2 的安装目录中找到：

``` sh
# 检查当前系统对每个 DB2 版本的支持情况
db2prereqcheck

# 检查当前系统对指定 DB2 版本的支持情况
db2prereqcheck -v 11.1.2.2
```

一旦系统满足了我们所要安装的 DB2 版本所有要求，就可以进行安装了。

### 安装
安装 DB2 总体来说有两种方式：图形界面方式安装（db2setup） 和 命令行方式安装（db2_install）。
</br>

图形界面安装比较简单，直接在安装目录下运行 `db2setup` 命令，该命令会打开 DB2 的图形安装界面，按照页面提示操作一步一步进行安装即可，这里就不做过多介绍了。

{{<admonition title="tip" type="tip">}}
从 DB2 response 文件进行安装，也是通过调用 `db2setup` 命令，并通过 `-r` 参数指定 response 文件进行安装的，如： `db2setup -r db2server.rsp`
{{</admonition>}}

这里主要介绍一下命令行安装方式，执行安装目录下的 `db2_install` 命令，便会触发命令行安装方式，该命令可以接收多个命令行参数，下面介绍了几个常用的参数，要想获取完整的参数列表帮助文档，可执行 `db2_install -h` 命令查看.
</br>

- `-n`：指定为非交互模式。如果指定了该参数，`-b` 和 `-p` 也必须同时被指定。
- `-b`：指定 DB2 的安装路径。
- `-p`：
- `-l`：指定安装日志文件路径和名称，root用户默认/tmp/db2_install.log.进程号。
- `-y`：表示接受 DB2 协议。

根据是否指定了 `-n` 参数，命令行安装方式又分为 **交互模式** 和 **非交互模式**，下面分别介绍一下这两种安装方式。

#### 交互式

交互式是指在安装过程中，系统会多次出现提示信息，并等待用户输入相关信息。这也是一种比较简单的安装方式。启动交互安装模式最简单的方法是在安装目录下直接执行 `db2_install` 命令，该命令默认开启的是交互模式，下图展示了交互模式的安装过程：
<br/>

![This is an image](/img/devops/db2_install_interactive.png)

安装过程中有以下 4 项需要用户提供输入：
- ① 输入 YES 表示接受 DB2 许可。
- ② 选择要安装的类型，输入 SERVER 表示安装完整的服务器端。
- ③ 选择 DB2 安装路径，输入 YES 使用默认路径。
- ④ 选择是否安装 pureScale 功能，输入 NO 表示不需要。

#### 非交互式

如果只是安装几台 DB2 server，通过交互式命令来安装是完全可行的，但是如果有几十台甚至上百台服务器需要进行安装操作，非交互式模式才是最好的选择，不仅节省大量的输入时间，同时可以将安装命令集成到安装脚本中，实现自动化安装。如：

``` sh
# 将 DB2 安装到 /opt/IBM/db2/V11.1 目录下
./db2_install -n -y -b /opt/IBM/db2/V11.1 -p XXXXX
```

{{<admonition type="warning">}}
由于本次只是升级安装，系统中已经存在了必要的 DB2 用户和组，如果是初次安装 DB2，并且选择命令行模式安装，必须自行创建好用户和组。
{{</admonition>}}

---

## 升级实例

当新版数据库安装完成后，就可以依次升级数据库实例和实例下的数据库了。
</br>

### 首先确保断开一切与数据库的连接

  - 停止 WEB 服务器，禁用所有 crontab
  - 关闭 Cast Iron
  - 停止 DataOptimizer，移除数据库 trigger

### 对主数据库进行离线备份

``` sh
nohup db2 backup db saleconn to /db/a1insctp/db2backup compress &
```

### 设置 HADR

1. 首先检查数据库 HADR，确保处于 PEER 状态。
``` sh
db2pd -db saleconn -hadr
```

2. 确保 `HADR_SYNCMODE` 的属性为 `NEARSYNC`

``` sh
# 获取 HADR_SYNCMODE 状态
db2 get db cfg for saleconn | grep -i SYN
```

{{<admonition title="info" type="info">}}
info
{{</admonition>}}

{{<admonition title='Note' type="note">}}
note
{{</admonition>}}
