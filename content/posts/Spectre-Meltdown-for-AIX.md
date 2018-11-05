---
title: "为系统安装 Spectre/Meltdown 补丁"
date: 2018-02-22T10:39:34+08:00
tags:
  - AIX
  - CentOS
  - Ubuntu
categories:
  - DevOps
  - System
---

## Spectre/Meltdown 漏洞

2018 新年伊始，Google 安全研究团队就爆出了英特尔处理器芯片的两个重要漏洞 Spectre 和 Meltdown。黑客可以通过这些漏洞获取系统中的一些机密信息，比如登录密码、登录秘钥、用户私人照片、邮件甚至是商业秘密文件等。
</br>

在漏洞被爆出的同时，多个系统厂家第一时间提供了补丁文件来修复这一硬件漏洞。本文将介绍如何在 AIX/CentOS7 系统中安装这些补丁文件来修复这两个漏洞。

## AIX
### 安装前的准备
虽然 IBM 第一时间放出了针对于 AIX 的 补丁，但是这些补丁并不是通用的。不同的统版本必须使用与之对应的补丁，下面表格中列出了 AIX 7.1 各个版本对应的补丁版本信息。

版本 | 补丁号 |
---  | ---
7.1.4.3 | IJ03032m3a.180125.epkg.Z
7.1.4.3 | IJ03032m3b.180125.epkg.Z
7.1.4.4 | IJ03032m4a.180125.epkg.Z
7.1.4.5 | IJ03032m5a.180116.epkg.Z
7.1.5.0 | IJ03033m1a.180116.epkg.Z
7.1.5.1 | IJ03033m1a.180116.epkg.Z

<!-- more -->

在安装补丁之前，首先查看当前 AIX 系统版本信息是否存在于上面列表中，可以通过下面命令获取当前系统版本信息：

``` sh
oslevel -s
```

我当前的系统版本为 `7100-04-03-1642`，对应的补丁号为 `IJ03032m3b.180125.epkg.Z`
</br>

如果你当前的系统版本没有出现在上述表格中，则需要将系统升级到指定的版本，关于如何升级 AIX 系统，请参考 [AIX 系统升级]({{< relref "AIX-system-upgrade.md" >}}) 。

### 安装补丁

补丁的安装也比较简单，下面列出了安装补丁所需要的命令：

``` sh
# 下载并解压补丁到 /tmp/spectre_meltdown_fix 目录
# emgr 的 -p 选项用于检测补丁是否可以被正确安装到系统中，而并不会真正去安装补丁
wget ftp://aix.software.ibm.com/aix/efixes/security/spectre_meltdown_fix.tar -O /tmp/spectre_meltdown_fix.tar \
  && tar xvf /tmp/spectre_meltdown_fix.tar -C /tmp \
  && cd /tmp/spectre_meltdown_fix \
  && emgr -e IJ03032m3b.180125.epkg.Z -p

# 安装补丁
# 当前版本 7100-04-03-1642 对应的补丁号为 IJ03032m3b
emgr -e IJ03032m3b.180125.epkg.Z -X

# 删除补丁文件
rm -rf /tmp/spectre_meltdown_fix /tmp/spectre_meltdown_fix.tar
```

当补丁安装完成后，需要对系统进行重启：

``` sh
reboot
```

至此，补丁安装完毕。

## CentOS 7

CentOS 下安装这两个补丁比较简单，首先下载检测脚本检测系统是否受这两个漏洞的影响：

``` sh
# 下载检测脚本
wget https://access.redhat.com/sites/default/files/spectre-meltdown--a79614b.sh -O /tmp/spectre-meltdown.sh

# 执行检测脚本
bash /tmp/spectre-meltdown.sh
```

如果发现系统中存在着两个漏洞，只需更新系统 kernel 即可[^1]：

``` sh
yum update -y kernel microcode_ctl
```

之后自行 `reboot` 命令重启系统即可。

## Ubuntu

同样，首先获取检测脚本检测系统当前是否收到这两个漏洞的影响：

``` sh
wget https://raw.githubusercontent.com/speed47/spectre-meltdown-checker/master/spectre-meltdown-checker.sh
```

对有响应的系统执行下面更新操作：

``` sh
sudo apt-get install linux-generic linux-headers-generic linux-image-generic
```

之后自行 `reboot` 命令重启系统即可。

[^1]: 对于 IBM 内部系统来说，使用 [`ibm-yum.sh`](ftp://ftp3.linux.ibm.com:2121/redhat/ibm-yum.sh) 脚本安装补丁：`bash ibm-yum.sh install -y kernel microcode_ctl`