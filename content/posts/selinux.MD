---
title: "SElinux"
date: 2018-03-01T20:17:24+08:00
keywords:
  - selinux
tags:
  - CentOS
  - Linux
categories:
  - System
draft: true
---

『没吃过猪肉，还没见过猪跑？』这句俏皮话用在 SELinux 上在适合不过了，很多 Linux 系统管理员不清楚什么是 SELinux，但一定都使用过某个命令来关闭它。甚至在某些 『安装好 XX 系统后应该做的 XX 件事情』类似的文章中，关闭 SELinux 被列举到了前10名。之所以出现这样的局面，其主要原因是由于 SELinux 配置的复杂性，往往一个小小的疏忽，轻者造成程序无法启动，重者甚至导致系统无法正常启动。
</br>

本文意在向读者简单介绍什么是 SELinux，以及使用 SELinux 的正确姿势。

## 什么是 SELinux
在正是开始学习 SELinux 之前，我们首先需要了解什么是 SELinux，为什么要使用 SELinux 以及它的优劣势。
</br>

SELinux(Security-Enhanced Linux) 是由美国国家安全局（NSA）研发的一套 Linux 权限控制系统，从其强大的出身背景中，我们似乎已经可以领略到 SELinux 的强大。SELinux 在 Linux 系统中现有的权限控制基础上，提供了更细粒度的权限控制机制，它通过读取系统中提前设定好的一些规则，可以达到精确控制某个用户或进程可以访问哪些文件、目录或是端口等目的。

早在 2003 年，Linux 就已将 SELinux 集成到 2.6 内核中了。 2.6 版本时，就已将 SELinux 集成到内核当中了。



很多黑客攻击系统时，并不是直接攻破你的主机，从而以超级管理员的身份登录到系统中，而是在系统中又某个有超级管理权限的用户运行的进程中找出漏洞，通过该进程对系统进行攻击。

## 为什么要使用 SELinux
想要了解为什么使用 SELinux，在了解什么是 SELinux 之前，首先让我们看一下 Linux 系统下默认的权限管理机制 DAC（discretionary access control）和 ACLs(access control lists)。

SELinux 是在 DAC 的基础上，又增加了一层保护机制，它通过 policy（策略）允许指定进程可以执行什么，不可以执行什么。

## SELinux 工作原理
先介绍几个必要的的概念：object，subject，context，label，role

对于 SELinux 来说，它只关心进程的 context

And when we say everything, we mean users, roles, processes, and files. The policy defines how each of these entities are related to one another.
An SELinux policy defines user access to roles, role access to domains, and domain access to types.


[参考1](https://www.digitalocean.com/community/tutorials/an-introduction-to-selinux-on-centos-7-part-1-basic-concepts)