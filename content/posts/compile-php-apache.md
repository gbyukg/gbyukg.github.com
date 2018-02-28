---
title: "CentOS7 下编译安装 Apache2.4 + PHP5.6"
date: 2018-02-02T16:52:47+08:00
keywords:
  - php
  - apache
  - centos
  - 编译
  - compile
  - centos
  - centos7
tags:
  - PHP
  - Apache
  - CentOS
categories:
  - DevOps
  - Linux
  - PHP
---

- Apache 是迄今为止全世界中使用最广泛的 WEB 服务器软件，它快速、可靠并且可通过简单的API扩充，将 PHP，Python 等解释器编译到服务器中。
- PHP 是最流行的 WEB 开发语言**之一**，它简单，易上手，尤其是 PHP7 的发布，对 PHP 的性能有了质的飞跃。并且 PHP 是世界上最好的语言（来打我呀🤣）

虽然各种发行版的 Linux 系统为我们提供了很方便的包管理工具来帮助我们快速安装 PHP 和 Apache，比如 Ubunt 系统的 `apt`，RedHat 系列的 `yum`。这些工具使用起来简单便捷，只需通过简单的几行命令，即可快速搭建出 PHP + Apache 的 WEB 环境，最重要的是，这些工具能够自动为我们处理最令人恼火的包依赖问题。通常情况下，使用包管理工具来安装这些中间件，是比较明智的选择，如：

``` sh
# 可以快速安装 apache 和 php
sudo yum install httpd php -y
```
</br>

<!--more-->

但总有些时候，需要我们手动对他们进行编译安装，比如：

- 当我们需要在系统中安装多个不同版本的 Apache 或是 PHP 的时候。
- 当我们想要有更多自定义功能选择的时候。
- 当我们需要对源码作出改动的时候。
- 当我们的系统无法连接网络的时候。

本文将详细介绍如果在 `CentOS 7` 中通过手动编译的方式来安装 `Apache2.4` 和 `PHP5.6`。

---

## 安装前的准备

在开始编译之前，首先需要确保系统中已经正确安装了 `gcc` 和 `make`。

- `gcc` 是 Linux 系统下的一款开源的编译器工具，他可以用来编译由 C，C++，Java，Object-C 等一系列语言变编写的源码文件，来生成可执行的二进制文件。
- `make` 是另一款 Linux 下强大的开源命令行工具，它通过解析定义在 Makefile 文件中的一系列规则，实现项目源码的自动化编译功能。

在某些系统中，这两款工具默认可能并没有被安装，我们可以通过查看他们的版本信息来简单检测系统中是否已经安装了这两款工具：

``` sh
# 查看 gcc 版本信息
gcc -v

# 查看 make 版本信息
make -v
```

可以通过下面的命令安装这两款工具：

``` sh
# yum 是 RedHat 旗下 Linux 发型包中的包管理工具
sudo yum install gcc make
```

---

## 安装 Apache

由于 PHP 的安装依赖于 Apache 模块，因此需要先安装 Apache。

### 安装前的准备

安装必要的依赖库和工具：

``` sh
yum install -y expat-devel pcre-devel wget
```

### 准备源码
Apache 源码可以直接从[官方网站](https://httpd.apache.org/download.cgi#apache24) 中直接获取，也可以通过下面命令行的方式获取到：

``` sh
# 创建临时目录保存源码
mkdir /tmp/source

# 下载 Apache 源码
wget http://mirrors.shu.edu.cn/apache/httpd/httpd-2.4.29.tar.bz2 -O /tmp/source/httpd-2.4.29.tar.bz2

# 解压源码到 /tmp/source/httpd-2.4.29 目录下
tar xvf httpd-2.4.29.tar.bz2 -C /tmp/source
```

- `wget` 命令会将 Apache 源码包下载到 `/tmp/source` 目录下。
- `tar` 命令将压缩文件解压到 `/tmp/source/httpd-2.4.29` 目录中

**APR 和 APR-Util**
在编译 Apache 时还需要 Apache 旗下额外两个开源库 APR 和 APR-Util，这两个库为 Apache HTTP server 提供了必要的运行时环境。我们可以提前在系统中手动安装好这两个库，并在编译 Apache 时指定这两个库的路径；
或者是更简单的办法，将这两个库的源码文件放到 Apache 源码目录下的 `srclib` 目录中，这样在编译 Apache 的同时，会自动为我们编译这两个库文件：

``` sh
# 首先进入到 apache 源码目录下的 srclib 目录中
cd /tmp/source/httpd-2.4.29/srclib

# 下载并解压 APR 源码
wget http://mirrors.hust.edu.cn/apache/apr/apr-1.6.3.tar.bz2 && \
  tar xvf apr-1.6.3.tar.bz2

# 下载并解压 APR-Util 下载源码
wget http://mirrors.shu.edu.cn/apache/apr/apr-util-1.6.1.tar.bz2 && \
  tar xvf apr-util-1.6.1.tar.bz2

# 重命名 apr 源码目录和 apr-util 源码目录，去掉版本信息
mv apr-1.6.3 apr
mv apr-util-1.6.1 apr-util
```

> 注意，最后两步重命名操作是必要的，一定要去掉文件名后面的版本号，否则编译过程中将会提示无法找到 APR 和 APR-Util 库。

### 开始安装

安装过程比较简单，首先进入到 Apache 源码目录下

``` sh
cd httpd-2.4.29
```

依次执行以下三个命令：

{{< highlight sh "linenos=table,linenostart=1" >}}
./configure --prefix=/usr/local/apache2.4.29/ \
--enable-so \
--enable-modules=most \
--with-mpm=prefork \
--with-included-apr

# 编译
make

# 安装
sudo make install
{{< / highlight >}}

第一行执行 `configure` 命令，事实上，`configure` 是一个 SHELL 脚本文件，该脚本是由 Apache 开发人员使用 `autoconf` 工具生成的，主要用于检测当前系统是否满足安装 Apache 的需求、设置一些安装项、以及生成 Makefile 文件等。通过 `./configure -h` 命令可以打印出完整的帮助文档信息。下面对我们使用到的选项做些简单描述：

- `--prefix` 指定了 Apache 将要被的安装路径。
- `--enable-so` 启用动态加载模块，这样我们就可以通过修改 Apache 的配置文件直接开启或停用模块，而不用重新编译 Apache 源码。
- `enable-modules=most` 
- `with-mpm=prefork` 用于指定 Apache 的[多模块处理](https://httpd.apache.org/docs/2.4/mpm.html)。
- `--with-included-apr` 通知编译器使用我们刚刚拷贝到 `srclib` 目录下的 APR 库。

当 `configure` 脚本执行成功后，下一步就是调用 `make` 命令，该命令会根据上一步生成出来的的 Makefile 文件中定义的规则，对源码进行编译，最终生成可执行的二进制文件。*该过程可能会花费一些时间来完成。*
</br>

最后， `make install` 指令表明开始执行 Makefile 中的 install 规则，将生成出的文件复制到我们通过 `--prefix` 指定的路径下。由于我们所指定的安装路径 `/usr/local/apache2.4.29` 属于系统路径，因此需要使用 `sudo` 转变成 root 权限安装。
</br>

至此，Apache 已经被成功安装到我们的系统中，可以通过命令 `/usr/local/apache2.4.29/bin/httpd -v` 检测我们的安装结果，该命令会返回我们所安装的 Apache 的版本信息。
可以通过命令 `/usr/local/apache2.4.29/bin/apachectl start|stop|restart` 来启动，停止以及重启 Apache web 服务。

### 设置环境变量
如你所见，当我们想要执行某个 Apache 命令时，每次都需要指定命令所在的完整路径信息。这是一件及其麻烦的事，最好是能像执行系统中其他命令那样，直接在命令行输入命令，系统会自动为我们找到该命令所在的位置。
</br>

系统环境变量 `PATH` 正是我们所需要的，它的值是一系列以分号分割的路径，当我们在终端执行任意命令时，Linux 系统会依次在 PATH 环境变量中指定的路径下搜索要执行的命令，并执行第一个被找到的命令。可以通过在命令行输入 `echo $PATH` 打印出当前环境变量 PATH 中的值。
</br>

Apache 所有可执行文件都被保存到了安装路径下的 bin 目录 `/usr/local/apache2.4.29/bin` 中，因此我们只需将该路径信息保存到环境变量 PATH 中即可，添加环境变量非常简单：

``` sh
sudo vim /etc/profile.d/httpd.sh
```

输入小写字母 `i` 进入 VIM 的编辑模式，拷贝一下内容到文件中：

``` sh
pathmunge /usr/local/apache2.4.29/bin
```

按下 `ESC` 键退出 VIM 的编辑模式，按下冒号（:）键进入 VIM 的命令行模式并输入 `wq`，表示保存并退出。

`pathmunge` 命令会将 `/usr/local/apache2.4.29/bin` 目录放到系统环境变量 PATH 指定的搜索路径的最前端。
但此时环境变量并没有生效，我们可以打开一个新的终端，或是通过手动执行命令 `. /etc/profile` 来使其生效。此时再次查看 PATH 内容：`echo $PATH`，Apache 路径已经出现自在了首位。这时我们就可以直接执行 `httpd -v` 命令，而无需在指定完整路径信息了。

{{<admonition title="tip" type="tip">}}
由于我们修改的是全局的 PATH 环境变量，这意味着改动将对所有用户都生效，当然我们也可以针对某些用户进行改动，其方式是修改用户根目录下的 `.bash_profile` 文件。
{{</admonition>}}

### Apache 配置文件

Apache 有着丰富的配置选项，针对不同的 server，不同的场景，配置信息都会有所不同，下面我们将介绍一些常用的 Apache 配置信息。Apache 配置文件位于安装目录下的 `conf/httpd.conf` 文件中。

- `User daemon` 指明 apache 子进程所属的用户，该用户必须是当前系统中的一个有效的用户。通常为创建一个名为 apache 的用户，并将该值修改为 apache。
- `Group daemon` 指明 apache 子进程所属的用户组，该组必须是当前系统中的一个有效的组。通常为创建一个名为 apache 的组，并将该值修改为 apache。

### 启动/停止 Apache

当我们配置好 Apache 之后，就可以通过 `apachectl` 命令来启动 Apache http server 了：

``` sh
apachectl  start
```

此时打开浏览器，输入 http://127.0.0.1 显示 **It works!**，表示 Apache Web 服务器已经安装成功。
</br>

除了 `start` 参数之外，`apachectl` 命令还可以接受一下参数：

``` sh
apachectl start|stop|restart # 启动|停止|重启
apachectl –v # 查看 Apache 版本信息
apachectl –f configuration_file_name # 手动指定apache配置文件
apachectl –t # 检查Apache配置文件语法是否有错误
apachectl -t -D DUMP_MODULES # 列出当前Apache所有模块
apachectl -t -D DUMP_VHOSTS # 列出当前所有虚拟主机模块
```

## 编译 PHP

Apache 安装好之后，就可以开始安装 PHP 了，PHP 的安装流程与 Apache 类似。

### 安装前的准备

首先安装编译 PHP 时所需的必要库：

``` sh
yum install –y perl \
  libxml2-devel \
  bzip2-devel \
  curl-devel \
  openjpeg-devel \
  libjpeg-turbo-devel \
  libpng-devel \
  libmcrypt-devel
```

这些所需的必要库，很大程度上取决于你编译 PHP 时指定的扩展库，例如安装时如果你指定了安装 PHP 的 jpeg 扩展库，那么系统中就要预先安装好 `libpng-devel` 库。

### 准备源码

### 开始安装

{{<admonition type="warning">}}

Warning message

{{</admonition>}}
<!--more-->

{{< highlight bash "linenos=table,linenostart=1" >}}
{{< / highlight >}}

[^1]: 文件名可以是任意的。

[参考](https://blacksaildivision.com/how-to-install-apache-httpd-on-centos)

---

#### APR 和 APR-Util
APR 和 APR-Util 是 Apache 基金会下的两款开源库，Apache 的 HTTP Server 就依赖于这两款库，它们为 Apache HTTP server 提供了运行时的依赖。
Apache HTTP server 在运行时依赖于 `APR` 和 `APR-Utils` 这两个库，因此在编译安装 Apache 之前，首先确保系统中已经安装了这两个库。
</br>

最简单的方式是直接通过包管理工具进行安装：
``` sh
yum install -y apr apr-util
```
</br>

也可以选择手动编译的方式来安装:
</br>

**APR：**
首先在系统中安装 APR。

{{< highlight bash "linenos=table, hl_lines=8-10,linenostart=1" >}}
# 下载源码
wget http://mirrors.hust.edu.cn/apache//apr/apr-1.6.3.tar.bz2
# 解压 APR 源码
tar xvf apr-1.6.3.tar.bz2
# 进入到源码目录
cd apr-1.6.3

./configure --prefix=/usr/local/apr
make
sudo make install
{{< / highlight >}}

- 第 6 行, 执行 `configure` 脚本，该脚本主要用于检测系统是否满足安装该软件的需求，设置，以及生成 Makefile 文件等。`prefix` 选项指定了我们想要安装的目录。通过 `./configure -h` 可以打印出完整的帮助文档。
- 第 7 行，执行 make 命令，根据生成的 Makefile 文件，执行一系列特定的操作，最终生成软件所需的所有二进制文件，配置信息，帮助文档等。
- 第 8 行，将所有必要的文件复制到第 6 行中通过 `prefix` 选项指定的安装目录中，由于我们指定的安装目录的父目录 `/usr/local` 为系统目录，只有 root 用户才有权限对该目录进行写操作，因此，如果是非 root 用户执行 `make install` 命令，需要使用 `sudo` 切换到 root 用户。

**APR-Util：**

APR-Util 的安装方式与 APR 的安装方式完全相同，除了几个特定的安装参数外：

{{< highlight sh "linenos=table, hl_lines=8,linenostart=1" >}}
# 下载源码
wget http://mirrors.shu.edu.cn/apache//apr/apr-util-1.6.1.tar.bz2
# 解压 APR-Util 源码
tar xvf apr-util-1.6.1.tar.bz2
# 进入到源码目录
cd apr-util-1.6.1

./configure \
  --prefix=/usr/local/apr-util \
  --with-apr=/usr/local/apr
make
sudo make install
{{< / highlight >}}

- 由于 APR-Util 依赖于 APR，因此在第 8 行中我们通过 `--with-apr` 参数指定了 APR 的安装目录，来通知 APR-Util 去哪里可以找到 APR 依赖。

{{<admonition title="tip" type="tip">}}
如果在安装 APR 时将所有库文件和头文件安装到了系统的默认目录中（并及时更新了 `ldconfig`），那么在安装 APR-Util 时就可以不用指定 `--with-apr` 参数。
{{</admonition>}}

### 开始安装

一切准备就绪，是时候开始安装 Apache 了。 首先是 **获取 Apache 源码**：
``` sh
# Apache httpd server
wget http://mirrors.shu.edu.cn/apache/httpd/httpd-2.4.29.tar.bz2

# 解压源码
tar xvf httpd-2.4.29.tar.bz2
```