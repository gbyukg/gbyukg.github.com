---
title: "Ansible —— 开始使用"
date: 2018-11-09T11:19:08+08:00
tags:
  - Ansible
categories:
  - DevOps
draft: true
---

作为开发运维人员，平时很大一部分工作是在与服务器打交道：安装软件、更新系统、执行批量脚本、部署程序等等。对于只有少数几台服务器来说，我们通常是手动登录到每一台服务器上执行相应的操作。但是如果要对成百上千台服务器进行操作时，手动方式显然不可取。试想一下，如果要为 100 台服务器安装 Nginx 服务，将是一个无比漫长和枯燥的过程。同时，这还会大大增加风险，因为手动执行的步骤越多，犯错的几率就会越大。

聪明的程序员并不会被这一个小小的挫折所打败，

Ansible 通常被描述为配置管理工具（Configuration Management Tool），通过将期待的状态写到配置文件中，最终使得目标机器的状态满足我们配置文件的要求。

## 工作原理

## 安装 Ansible

由于 Ansible 采用 SSH 协议与目标服务器通信，因此我们只需在本地操作机上安装 Ansible 可执行程序即可，而目标服务器只需保证可以通过 SSH 连接（即开启 SSHD 服务），并且正确安装了 Python2(2.6 及以上版本) 或是 Python3（3.5 及以上版本） 及以上版本即可（Ansible 采用 Python 开发，在目标机器上执行指令时会通过 Python 对指令进行解析），无需在安装任何客户端程序（agent）。目前所有主流系统几乎默认都会为我们安装好 SSHD 服务和 Python，因此大部分时候，我们不需要对目标机器做任何操作。

Ansible 客户端可以通过多种方式被安装到多种系统中，下面我介绍了一些常见的安装方式，如果想查看完整的安装方式，请参考[官方文档](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)。

### Ubuntu

在 Ubuntu 上安装最新版本的 Ansible， 我们需要手动添加 Ansible 官方 [PPA](https://launchpad.net/~ansible/+archive/ubuntu/ansible) 仓库到本地，之后再利用 `apt-get install` 命令进行安装。

不过在这之前，首先确保系统中已经安装了 `software-properties-common`, 使用下面命令安装 `software-properties-common`：

``` sh
$ sudo apt install software-properties-common
$ sudo apt-get update
```

添加 Ansible PPA 仓库：

``` sh
$ sudo apt-add-repository --yes ppa:ansible/ansible
$ sudo apt-get update
```

最后执行安装步骤：

``` sh
$ sudo apt-get install -y ansible
```

### CentOS/RHEL 7

CentOS/RHEL 系统中默认已经包含了 Ansible 包，因此我们可以直接通过 `yum` 命令安装 Ansible：

``` sh
$ sudo yum install ansible
```

但是，通过这种方式安装的 Ansible 有可能不是当前最新版本（理论上来说应该是当前最稳定的版本），如果需要安装最新版本的 Ansible， 添加 [EPEL（Extra Package for Enterprise Linux）](https://fedoraproject.org/wiki/EPEL) 到本地仓库，在使用 `yum install` 命令进行安装，即可获取最新版本：

``` sh
# 我当前系统使用的是 CentOS7，所以安装的是 epel-release-latest-7
# 请针对你的系统选择使用对应的仓库
$ sudo yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
$ sudo yum update
$ sudo yum install -y ansible
```

或是手动下载

``` sh
wget https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
$ sudo rpm  -i epel-release-latest-7.noarch.rpm
```

下载 RPM 包安装：

``` sh
https://releases.ansible.com/ansible/rpm/release/epel-7-x86_64/ansible-2.7.1-1.el7.ans.noarch.rpm
```

### 使用 pip 安装

Ansible 自身使用 Python 开发，因此它支持使用 `pip` 安装，这是最简单的安装方式，同时也是官方推荐的安装方式。

在已经安装了 `pip` 的机器上，利用 `pip install` 进行安装：

``` sh
$ pip install ansible
$ pip install ansible==2.4.1.0
```

#### Upgrade

``` bash
pip install ansible --upgrade
```

<!-- more -->

---

## 开始使用 Ansible

当成功安装 Ansible 后，可以通过 `ansible --version` 命令查看 Ansible 版本信息，以下是我当前 Ansible 版本信息：

``` sh
$ ansible --version
```

输出结果为：

``` sh
ansible 2.7.0
  config file = /etc/ansible/ansible.cfg
  configured module search path = [u'/home/vagrant/.ansible/plugins/modules', u'/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python2.7/site-packages/ansible
  executable location = /usr/bin/ansible
  python version = 2.7.5 (default, Jul 13 2018, 13:06:57) [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
```

可以看到，当前我所安装的 Ansible 版本为 `2.7`。

### 执行你的第一个 Ansible 命令

Ansible 支持两种方式对目标机器运行指令：Ad-Hoc Commands 和 Playbook。

Ad-Hoc 允许我们快速对目标机器执行一些一次性指令，就像是在 bash 中执行某个指令；Playbook 则将我们要执行的 task 保存在配置文件中，之后可以多次执行。

#### Ad-Hoc Commands

下面让我们看一条简单的命令：

``` sh
$ ansible localhost -m ping
```

输出结果为：

``` sh
localhost | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```

在这条指令中，第一个参数 `localhost` 指定我们要执行操作的目标机器，即对当前主机进行操作；`-m ping` 指定我们要使用的 Ansible 的 `ping` 模块。Ansible 在目标执行的任何操作都是通过 Ansible 模块来实现的，`command`，`shell`，`copy`，`apt`，`yum`，

Ansible 目前支持 2000 多个模块

[模块列表](https://docs.ansible.com/ansible/latest/modules/list_of_all_modules.html?highlight=modules)

``` sh
ansible localhost -m command -a 'echo Hello World.'

ansible localhost -m command -a date

ansible localhost -a date
```

#### Playbook

一系列任务，可以保存起来，供我们多次使用。

```
- name: Configure webserver with nginx
  hosts: webservers
  become: True
  tasks:
    - name: install nginx
      apt: name=nginx update_cache=yes

    - name: copy nginx config file
      copy: src=files/nginx.conf dest=/etc/nginx/sites-available/default

    - name: enable configuration
      file: >
        dest=/etc/nginx/sites-enabled/default
        src=/etc/nginx/sites-available/default
        state=link

    - name: copy index.html
      template: src=templates/index.html.j2 dest=/usr/share/nginx/html/index.html
        mode=0644

    - name: restart nginx
      service: name=nginx state=restarted
```

## Inventeory

## Variables

## Playbook

## Modules

---

```
1. Configuration Management:
    It helps you configuring your web and application servers. It easy to version your files and you can also use it to manage different configurations in your development staging and production environment.

2. Application Deployments:
    It is also used for application deployments, it can fully automate your multi-tier application deployment. Of course it can handle groups of web servers application servers and databases.

3. Service Orchestration:
    You need to take out a note from load-balancing before you start a deployment, ansible can orchestrate services on multiple tiers


There are a lot of other tool in the market that try to solve the same kind of problems. 
Ansible is one of the simple solutions, 


How Ansible works:


What are playbooks?
You can use them to define your deployment steps and configuration. They are modular, they can contain variables and the can be used to orchestrate deployment steps across multiple machines. Playbooks are config files written in simple YAML.

the tasks make use of modules, 
You don't have to write any custom code, and Ansible ships with the long list reusable and mature modules.
Those modules mostly also handle differences between different Linux distributions and versions.





Configuration Management Tool: it can be used to setup and config computers.

Maintained by Red Hat

Essentially free and Open Source

Install on Control machine, that's can be your desktop system, or dedicated server, target server however no configuration is no needed.

Ansible use ssh connection method, the first thing to make sure is that you can log into the server via SSH.

To make this more convenient I'm creating an SSH Key so I don't have to type password every time.

Most modern Linux distributions already provide packages for Ansible. 

In order to install the latest version, a little bit more work needs to be done. Essentially add a repository to the system and install Ansible from that repository:
apt-add-repository ppa:ansible/ansible: add repository
apt-get update: update repository cache of the system
apt-get install ansible
ansible --version

/etc/ansible: basic configuration
If you want to manage multiple platforms from one control machine, it's better to create a copy of that directory and work on the copy instead

ad-hoc command aren't the usual way to interact with your servers, but ad-hoc commands do come in handy for small tasks and changes to the platform like temporarily adding a user or querying information from the servers.

check hostname values of every server, normally you would have to login to every server and run the command hostname by yourself.

shell module that let's you execute any command, all you have to type is: ansible all -m shell -a 'hostname'

the available disk space on : ansible all -m shell -a 'df -h'

ansible -m shell -a 'whoami' all

getent passwd | grep testuser



role is just a list of commands that ansible will execute on a target machine in a given order, a playbook is then used to determine which role should be applied to each target machine.

- name: "Installing additional software"
  apt: pkg={{ item }} state=installed
  with_items:
  - dnsutils
  - git
  - vim

ansible-playbook -K playbook.yml
```

---

- Ansible inventories
- Ansible modules
- YAML
- Ansible playbooks, breakdown of sections
- Ansible playbooks, variables
- Ansible playbooks, facts
- Templating with Jinja2
- Ansible palybooks, creating and executing

Modules:

---

- Setup Module: Used for gathering facts when executing playbooks.
  This module is automatically called by playbooks to gather useful variables about remote hosts that can be used in playbooks.
  It can also be execute directly by `/usr/bin/ansible` to check what variables are avaliable to a host.

- File Module: Used for file, symlinks and directory manipulation.
  Sets attribulte of files, symlinks and directories, or removes files/symlinks/directories.
  Many other modules support the same options as the `file` module - including `copy`, `template` and `assemble`.
  For Windows targets use the `win_file` module instead.

YAML

---

- YAML - yet another markup language
- Structure of YAML files
- Indentation
- Quotes
- Multiline values
- True/false
- Lists and dictionaries

> http://yaml-online-parser.appspot.com


http://www.zsythink.net/archives/2698

https://symfonycasts.com/screencast/ansible/ansible-intro