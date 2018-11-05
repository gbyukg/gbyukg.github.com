---
title: "Linux 用户和组"
date: 2016-03-23T18:56:52+08:00
keywords:
  - useradd
  - groupadd
  - id
  - usermod
  - chage
  - ulimit
  - userdel
  - groupdel
  - passwd
  - chpasswd
  - 用户
tags:
  - CentOS
  - Linux
categories:
  - System
---

用户其实就是系统中的账号，只有拥有了账号，我们才可以登录到系统中，执行相应的操作。每个用户又必须属于一个 **主组** 和一个或多个 **其他组**。用户和组又是构成 Linux 权限管理的基础，因此了解用户和组，对学习 Linux 至关重要。
</br>

本文意在向大家简单介绍如何在 Linux 下通过命令行的方式对用户和组进行操作。通过该文的讲解，你将能够掌握到以下命令：

- `useradd` 创建新用户
- `passwd` 和 `chpasswd` 修改用户密码
- `usermod` 修改用户属性
- `chage` 修改用户已日期相关信息
- `userdel` 删除用户
- `groupadd` 创建组
- `groupdel`删除组
- `id` 查看用户信息
- `ulimit` 用户资源限制相关操作

本文所使用的系统环境为 `CentOS 7.4`，并且所有命令都运行在 root 用户下，如果您没有登录 root 用户的权限，则至少有 `sudo` 权限，并在所有命令前使用 `sudo` 命令。

## 用户管理
在这一节中，我们将学习如果创建新用户，查看用户信息，修改用该信息及密码，以及与用户相关的以为文件。

### `useradd` 创建用户

在 Linux 下，我们可以通过命令 `useradd`[^1] 来创建一个新用户，其格式为 `useradd [options] LOGIN`。 它可以接受一个或者多个参数，下面列出了一些常用的参数：
</br>

<!--more-->

- `-d，--home HOME_DIR`：该选项接收一个路径作为参数，用于指定新创建的用户的 home 目录。如果没有指定该选项，则默认在 `/home` 目录下创建一个与用户名同名的文件夹作为新创建用户的 home 目录。
- `-m, --create-home`：如果系统默认设定为不为新用户创建 home 目录时，可以使用该选项明确指定为用户创建 home 目录。另外，如果命令行中同时使用了 -k 选项，该选项也必须被明确指定，才会使 `-k` 选项生效。
- `-M`：不为新创建的这个用户创建任何 home 目录（默认为新用户创建 home 目录）。
- `-u, --uid UID`：每个用户在系统中都存在一个唯一的标识号： UID。 当创建一个新用户时，系统会自动分配一个当前可用的最小 ID 作为这个用户的 UID，在 CentOS 下，普通用户级别的起始 ID 为 1000。通过该选项，我们可以为新创建的用户手动指定一个 UID 。但该 UID 必须没有被使用。
- `-U，--user-group`：创建一个与新用户同名的组，并将该用户添加到这个组中（默认行为）。
- `-g, --gid GROUP`：将组 GROUP 指定为该用户的主组（主组的概念将会在用户组这一节中介绍），GROUP 可以是组名，也可以是组 ID，但前提是该组必须是已经存在的组。
- `-G, --groups GROUP1[,GROUP2,...[,GROUPN]]`：将新创建的用户同时加入到指定的这些组中，各个组之间使用逗号分隔，中间不能含有任何多余的空格。同样，这些组必须都是已经存在的组。
- `-N, --no-user-group`：不会创建与用户名同名的组，如果没有指定 `-g` 选项，则将该用户添加到系统默认组中。
- `-s，--shell SHELL`：用于指定用户的登录 SHELL。默认为 bash
- `-c, --comment COMMENT`：为新创建的用户添加一些说明。
- `-e, --expiredate EXPIRE_DATE`：指定新用户的过期日志，EXPIRE_DATE 格式为： `YYYY-MM-dd`
- `-k, --skel SKEL_DIR`：默认情况下，当新用户被创建后，useradd 命令会将 `/etc/skel` 文件夹下的文件拷贝到新用户的 home 目录中。该参数可以让我们手动指定拷贝 `SKEL_DIR` 目录下的文件到新用户的跟目录下。需要注意的是，如果指定了该选项，则必须同时指定 `-m` 选项，否则不会生效。

#### 示例

**创建一个名为 luke1 的新用户：**

``` bash
[root@localhost ~]$ useradd luke1
```
默认情况下，等同于：
``` sh
[root@localhost ~]$ useradd -m -U luke1
```
该命令将会执行以下几个步骤：
  - 创建一个名为 luke1。
  - 创建一个与用户名同名的新组。
  - 将该用户的主组和其他组全部设定为这个新组。
  - 在 `/home` 目录下创建一个 `luke1` 文件夹作为 luke1 用户的 home 目录。

我们可以使用命令 `id` 来查看用户详细信息：
``` sh
[root@localhost ~]$ id luke1
uid=1000(luke1) gid=1000(luke1) groups=1000(luke1)
```
通过该命令，可以观察到，我们先创建的用户 UID 为 1000，新创建的组 ID 也为 1000.
</br>

**指定其他路径作为新创建用户的根目录为：**

``` sh
[root@localhost ~]$ useradd -d /var/www/ luke2
```
该命令会在 `/var` 目录下创建一个 `www` 文件夹，并将目录 `/var/www` 指定为 luke2 用户的根目录。
</br>

**不创建 home 目录**

``` sh
[root@localhost ~]$ useradd -M luke3
```
不会为 luke3 用户创建根目录，但注意，这并不代表 luke3 用户没有跟目录，只是根目录没有被创建罢了。
</br>

**指定新创建用户的 UID**

``` sh
[root@localhost ~]$ useradd -u 1005 luke4
[root@localhost /]$ id luke4
uid=1005(luke4) gid=1005(luke4) groups=1005(luke4)
```
新创建用户的 UID 为 1005
> 注意：当我们在创建一个新用户时如果为该用户指定了 UID，在这之后创建的用户的 UID 会在该 UID 基础之上进行增加，继续看下面的例子。
</br>

**指定用户的主组**

``` sh
[root@localhost /]$ useradd -N -g 0 luke5
[root@localhost /]$ id luke5
uid=1006(luke5) gid=0(root) groups=0(root)
```
`-N` 选项指明了不会创建 luke5 组，而是将新用户添加到 0（root） 组下。事实上，当指定了 `-g` 参数时，`-N` 可以忽略。
同时，我们注意到，luke5 用户的 UID 为 1006，实在 luke4 的 UID 基础上加 1 得到的。
``` sh
[root@localhost /]$ useradd -N luke5-b
[root@localhost /]$ id luke5-b
uid=1007(luke5-b) gid=100(users) groups=100(users)
```
可以看到，新创建的用户 luke5-b 被添加到系统默认用户组 users 中。
</br>

**将新用户添加到多个组中**

``` sh
[root@localhost /]$ useradd -u 1010 -g luke1 -G luke2,luke3,luke4 -d /var/luke6/ -m luke6
[root@localhost /]$ id luke6
uid=1010(luke6) gid=1002(luke1) groups=1002(luke1),1003(luke2),1004(luke3),1005(luke4)
```
指定 luke6 主组 luke1，该用户同时属于 luke2，luke3 和 luke4 组。并创建 `/var/luke6/` 作为其 home 目录。
</br>

**修改 login shell**
``` sh
[root@localhost /]$ useradd -s /bin/bash -c "Testing user" luke7
```
指定 luke7 用户默认的登录 SHELL 为 bash，并为该用户添加了简短的注释。
</br>

**指定用户过期日期**
``` sh
[root@localhost /]$ useradd -e 2018-02-24 luke8
[root@localhost /]$ chage -l luke8
Last password change					: Feb 23, 2018
Password expires					: never
Password inactive					: never
Account expires						: Feb 24, 2018
Minimum number of days between password change		: 0
Maximum number of days between password change		: 99999
Number of days of warning before password expires	: 7
```
通过 `-e` 选项将账号过期日志指定为 Feb 24, 2018，可以通过 `chage -l username` 方式查看账户过期日期。关于 `chage` 命令的详细说明，将会在下面小节中介绍。
另一个例子：将新创建账号的过期日期设置为 300 天之后
``` sh
useradd -e `date -d "300 days" +"%Y-%m-%d"` luke8
```

### `id` 命令查看用户信息

当我们想要查看某个用户信息时，可以使用命令行工具 `id`，该命令可以让我们获取到用户的用户名，UID，主组名及其主组 ID，所有其他组名称和组 ID 等信息，其基本格式为：`id [OPTION] [USERNAME]`。
</br>

其中 OPTION 和 USERNAME 均为可选参数，如果没有指定任何 username 参数，则获取当前用户信息。
</br>

下面列出了一些常用的选项：

- `-u，--user`：只显示用户的 UID
- `-g，--group`：打印出用户主组 ID。
- `-G，--groups`：打印出用户所有其他组 ID。
- `-n，--name`：显示用户或组的名称，而非他们的 ID。

#### 示例

**获取当前用户的信息：**

``` sh
[root@localhost ~]# id
uid=0(root) gid=0(root) groups=0(root) context=unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023
```
</br>

**获取指定用户的信息**

通过在命令行后指定 luke1，来获取指定用户的信息：
``` sh
[root@localhost ~]# id luke1
uid=1001(luke1) gid=1002(luke1) groups=1002(luke1)
```
</br>

**获取用户 UID**

``` sh
[luke1@promote ~]$ id -u luke1
1001
```
</br>

**获取用户的用户名**

``` sh
[luke1@promote ~]$ id -un luke1
luke1
```
</br>

**获取用户的主组 ID**
通过 `-g` 或 `--group` 命令获取到用户的主组 ID：
``` sh
[luke1@promote ~]$ id -g luke1
1001
```

该命令等同于：`id --group luke1`
</br>

**获取用户的主组名称**
通过 `-n` 或 `--name` 获取相应的名字，而非 ID 值：
``` sh
[luke1@promote ~]$ id -gn luke1
luke1
```
</br>

**获取用户的其他组 ID 和名称**

``` sh
[luke1@promote ~]$ id -G luke1
1002
[luke1@promote ~]$ id -Gn luke1
luke1
```
</br>

### `passwd` 修改用户密码
当成功创建好一个用户后，一般都需要为新创建的用户设置密码。可以使用命令行工具 `passwd` 为某个用户设置密码，其格式为：`passwd [OPTION] [USERNAME]`
</br>

其中 OPTION 和 USERNAME 均为可选参数，如果没有指定任何 username 参数，则为当前用户设置密码。`passwd` 不仅可以帮助我们为用户设置密码，它还可以用来查看和修改密码日期相关信息，比如设置密码过期日期等。
</br>

下面列出了一些常用的选项：
- `-S，--status`：获取指定账号的状态信息。
- `-e，--expire`：使得某个用户的密码即可过期，这会强制用户在下次登录系统时修改密码。执行此命令的用户需要有特殊权限。
- `-n，--mindays MIN_DAYS`：设置两次密码修改的最小间隔天数为 MIN_DAYS。0 表示没有限制。
- `-x，--maxdays MAX_DAYS`：设置密码的有效天数为 MAX_DAYS，当超过 MAX_DAYS 天时，密码将过期。-1 表示密码永不过期。
- `-w，--warndays WARN_DAYS`：设置密码过期前 WARN_DAYS 天，用户开始收到报警信息。
- `-i，--inactive INACTIVE`：设置当密码过期 INACTIVE 天数后，账号将被锁定。被锁定的账号将无法登录到系统中。-1 表示永不锁定账号。
- `-l，--lock`：锁定指定账号的密码。
- `-u，--unlock`：解锁某个使用 `-l` 选项锁定的账号。
- `-d，--delete`：删除指定用户的密码。被删除密码的用户将无法登陆系统。

#### 示例

**修改当前用户密码**
如果直接执行 `passwd` 命令而不加任何参数，系统将提示用户修改当前用户的密码。对于 root 用户来说，修改 root 密码不需要提供当前密码，而对于普通用户来说，需要提供当前密码才能当前用户密码。

root 用户直接输入新密码即可：
``` sh
[root@localhost ~]# passwd
Changing password for user root.
New password:
```

对于普通用户，需要先提供用户的当前密码：
``` sh
[luke1@promote ~]$ passwd
Changing password for user luke1.
Changing password for luke1.
(current) UNIX password:
```
</br>

**特权用户修改其他用户密码**
拥有特权的用户除了可以修改自己密码之外，还可以修改其他用户密码，只需在 `passwd` 命令后指定要修改的用户名即可：

``` sh
[root@localhost ~]# passwd luke1
Changing password for user luke1.
New password:
```
通过这种方式为其他用户修改密码，同样不需要提供用户的当前密码。
</br>

**获取用户账户信息**
使用 `-S` 可以获取指定用户的账号信息，返回的信息共包含 7 个字段，他们分别为：
- 用户的登录名。
- 密码状态信息，包括以下几种状态：
  - `LK`： 表示账号密码被锁定；
  - `NP`： 表示没有为该账号设置密码；
  - `PS`： 表示密码被正确设置了；
- 上次修改密码的时间。
- 两次密码修改的最小间隔天数。
- 密码多少天之后过期。
- 密码过期前多少天开始报警。
- 密码过期几天后帐号会被锁定。
- 密码状态的描述说明。

``` sh
[root@localhost ~]# passwd -S luke1
luke2 PS 2018-02-26 0 99999 7 -1 (Password set, MD5 crypt.)
```

通过上面的输出，我们可以得出以下结论：luke1 账号密码被正确地使用 MD5 设置设置过了；设置密码的日期为 2018-02-26；账号 luke1 对两次密码修改时间的间隔没有任何限制，并且设置了密码用不过期；账号密码会在过期 7 天开始报警（这里该账号密码用不过期，因此该值没有意义）；即使密码过期后也不会锁定该账号。
</br>

**强制用户密码过期**
使用 `-e` 选项强制账户 luke1 的密码过期，当下次使用该账户登录系统时，将提示用户修改密码。

``` sh
[root@localhost ~]# passwd -e luke1
```
</br>

**删除账号密码**
使用 `-d` 删除账号 luke1 的密码，删除密码后 luke1 用户将无法登录到系统中：
``` sh
[root@localhost ~]# passwd -d luke1
Removing password for user luke1.
passwd: Success
[root@localhost ~]# passwd -S luke1
luke1 NP 2018-02-26 1 99999 45 5 (Empty password.)
```
</br>

**锁定账号密码**
通过 `-l` 选项锁定账号 luke1 的密码。锁定账号密码并不影响账号的登录，仅仅是使账号的密码不可用。用户仍然可以使用其他方式，比如 SSH 秘钥的方式登录到系统中。
``` sh
[root@localhost ~]# passwd -l luke1
Locking password for user luke1.
passwd: Success
[root@localhost ~]# passwd -S luke1
luke1 LK 2018-02-26 1 99999 45 5 (Password locked.)
```
</br>

**解锁账号密码**
使用 `-u` 选项可以解锁一个通过 `-l` 选项锁定的账户的密码：
``` sh
[root@localhost ~]# passwd -u luke1
Unlocking password for user luke1.
passwd: Success
[root@localhost ~]# passwd -S luke1
luke1 PS 2018-02-26 1 99999 45 5 (Password set, MD5 crypt.)
```
</br>

**设置两次密码修改的最短间隔**
设置账户 luke1 两次密码修改最短间隔为 2 天：
``` sh
[root@localhost ~]# passwd -n 2 luke1
Adjusting aging data for user luke1.
passwd: Success
[root@localhost ~]# passwd -S luke1
luke1 PS 2018-02-26 2 99999 45 5 (Password set, MD5 crypt.)
```
</br>

**设置密码过期时间**
设置账户 luke1 密码的过期时间在 90 天以后：
``` sh
[root@localhost ~]# passwd -x 90 luke1
Adjusting aging data for user luke1.
passwd: Success
[root@localhost ~]# passwd -S luke1
luke1 PS 2018-02-26 2 90 45 5 (Password set, MD5 crypt.)
```
</br>

对于没有特权的普通用户来说，直接在命令行输入 `pwasswd` 命令后，

对于有超级权限的用户来说，比如 root，不但可以修改自己账户的
当执行如果 `passwd` 命令后没有跟
如果直接在命令行中输入 `passwd` 命令，将会提示修改当前用户的

`passwd` 命令不仅可以帮助我们为用户重置密码，它还可以修改用户密码的过期日期。

#### 在脚本中修改用户密码
`passwd` 采用的是交互式的方式来修改用户密码，但很多时候我们会使用脚本的方式创建账号并设置密码，交互式命令并不能满足我们的要求。这时可以使用 `--stdin` 参数指定标准输入，而不是提示用户输入密码，在通过管道的方式将密码传递个 `passwd` 命令：

``` sh
[root@localhost ~]# echo "password" | passwd --stdin luke1
Changing password for user luke1.
passwd: all authentication tokens updated successfully.
```
</br>

对于某些没有为 `passwd` 命令提供 `--stdin` 参数的系统来说，还可以使用 `chpasswd` 命令来代替：
``` sh
[root@localhost ~]# echo "luke1:password" | chpasswd
```

### `usermod` 更新用户信息
`usermod` 命令可以帮助我们修改系统中已经存在的用户的属性信息，比如修改用户的登录名，home 目录，组信息，登录 SHELL 等。其格式为 `usermod [options] LOGIN`。
</br>

下面列出了一些常用的选项：
- `-l, --login NEW_LOGIN`：更新用户的登录名为 NEW_LOGIN。注意，该选项并不会修改用户的 home 目录和 mail 文件。
- `-u, --uid UID`：
- `-d, --home HOME_DIR`：修改用户的 home 目录至 HOME_DIR，该选项只是简单将用户的 home 目录指向新的目录，而原 home 目录中的内容不会被迁移到新的 home 目录中，可以使用 `-m` 选项对原 home 目录中的内容进行迁移。
- `-m, --move-home`：将当前 home 目录中的内容迁移到新的 home 目录下。该选项必须与 `-d` 选项一起使用。
- `-L, --lock`：锁定用户的密码。该选项与 `passwd -l` 命令效果一样。
- `-U, --unlock`：解锁用户密码。该选项与 `passwd -u` 命令效果一样。
- `-g, --gid GROUP`：将用户的主组设置为 GROUP。GROUP 可以是组名，也可以是组 ID，但必须是系统中已经存在的组。修改用户的主组，用户 home 目录中所有文件的所属组也将同样被修改为该新组，而对于 home 目录之外的文件，需要用户手动进行修改。
- `-G, --groups GROUP1[,GROUP2,...[,GROUPN]]]`：将用户的其他组设置为指定的新组。同样，提供的参数可以是组名，也可以是组 ID。但这些组必须是系统中的有效组。
- `-a, --append`：与 `-G` 一起使用，将 `-G` 指定的组追加到当前用户的其他组中，而不是替换当前用户的其他组。
- `-e, --expiredate EXPIRE_DATE`：设置用户的账号过期日期为 EXPIRE_DATE，日期格式为：YYYY-MM-DD。可以通过指定 EXPIRE_DATE 的值为 -1 禁用账号过期功能。
  > 注意，`usermod -e` 命令用来设置用户的账号过期日期，而 `passwd -x` 用来设置用户的密码过期日期。账号过期的用户将无法登录到系统中，而密码过期的用户仍然可以登录到系统中，并且登录系统是会强制用户修改密码。
- `-f, --inactive INACTIVE`：设置账号密码过期 INACTIVE 天后账号将被锁定。0 表示密码过期时账号立即被锁定；-1 表示不锁定账号。
- `-s, --shell SHELL`：将用户的登录 SHELL 修改为新值 SHELL。
- `-c, --comment COMMENT`：修改用户说明信息。

#### 示例

**修改用户账号的说明信息**
选项 `-c` 用来修改指定账号的说明信息，比如为 luke1 用户增加说明信息：
``` sh
[root@promote ~]# usermod -c "This is Luke1" luke1
```

当设置成功后，可以通过查看 `/etc/passwd` 文件获取该信息，关于该文件的说明，会在下面的小节中介绍到。

``` sh
[root@promote ~]# getent passwd luke1
luke1:x:1001:1002:This is Luke1:/home/luke1:/bin/bash
```
</br>

**更新用户 home 目录**
使用 `-d` 选项将用户的 home 路径指向 `/var/www` 路径。并通过 `-m` 选项将原目录下的文件移动到新 home 路径下。
``` sh
[root@promote ~]# usermod -m -d /var/www luke1
```

如果没有指定 `-m` 选项，则仅仅是将 home 目录指向新目录，原目录中的文件并不会被迁移到新路径下。
</br>

**设置账号的过期日期**
选项 `-e` 用来更新账户的过期日期，日期格式为 `YYYY-MM-DD`。账号日期相关信息可以通过 `chage` 命令查看，我们将会在下节详细介绍 `chage` 命令。在更改账号过期日期前，先让我们查看一下当前用户 luke1 日期相关信息：

``` sh
[root@promote ~]# chage -l luke1
Last password change					: Feb 27, 2018
Password expires					: never
Password inactive					: never
Account expires						: never
Minimum number of days between password change		: 2
Maximum number of days between password change		: -1
Number of days of warning before password expires	: 45
```

`Account expires` 字段描述了账户过期时间，当前账户 luke1 没有设置任何过期时间。现在让我们将 luke1 用户的账号过期日期设置为 `2019-01-01`：
``` sh
[root@promote ~]# usermod -e 2019-01-01 luke1
[root@promote ~]#
[root@promote ~]# chage -l luke1
Last password change					: Feb 27, 2018
Password expires					: never
Password inactive					: never
Account expires						: Jan 01, 2019
Minimum number of days between password change		: 2
Maximum number of days between password change		: -1
Number of days of warning before password expires	: 45
```
</br>

**修改用户主组**
选项 `-g` 用来修改用户的主组，在修改前首先用 `id` 命令查看 luke1 用户信息。
``` sh
[root@promote ~]# id luke1
uid=1001(luke1) gid=1002(luke1) groups=1002(luke1)
```
luke1 用户当前主组为 luke1，更新主组信息：

``` sh
[root@promote ~]# usermod -g 0 luke1
[root@promote ~]# id luke1
uid=1001(luke1) gid=0(root) groups=0(root),1002(luke1)
```
luke1 用户的主组被更新为 root 组。
> 当修改用户主组后，用户 home 目录下的所有文件的所属组都将被更新为新的组。
</br>

**向用户其他组中追加新组**
选项 `-G` 用来修改用户的其他组信息，如果没有指定 `-a` 参数，则将指定的组代替当前用户的其他组信息；如果同时指定了 `-a` 选项，则将指定的组追加到用户的其他组信息中。
``` sh
[root@promote ~]# usermod -aG luke2 luke1
[root@promote ~]# id luke1
uid=1001(luke1) gid=0(root) 1002(luke1),1003(luke2)
```
</br>

**锁定与解锁用户**
当我们想要禁用某个账户时，可以使用 `-L` 选项来锁定该账户：
``` sh
[root@promote ~]# usermod -L luke1
```
> 注意： 被锁定的账户将无法登录到系统中

被锁定的的账户可以通过 `-U` 选项解锁：
``` sh
[root@promote ~]# usermod -U luke1
```
</br>

**修改用户的登录 SHELL**
选项 `-s` 可以帮助我们修改用户的登录 SHELL：
``` sh
usermod -s /bin/zsh luke1
```

### `chage` 修改用户日期设定
在前面的小节中，我们介绍了如果使用 `passwd` 命令和 `usermod` 命令修改用户账号日期相关信息，比如密码过期日期、账号过期日期、密码修改最小间隔时间等。虽然这两个命令可以满足我们大部分的需求，但 Linux 还是提供了更专业的命令行工具 `chage`，来查看和修改与账户日期相关的信息。其基本格式为：`chage [options] LOGIN`。
</br>

下面列出了一些常用的选项：
- `-l, --list`：打印出给定账户相关信息。
- `-M, --maxdays MAX_DAYS`：设置密码有效期天数为 MAX_DAYS 天。当超过指定的天数后，用户再次登录系统时将强制用户修改密码。值 MAX_DAYS 为 -1 表示密码永不过期。
- `-E, --expiredate EXPIRE_DATE`：设置用户的账号过期日期，其值 EXPIRE_DATE 可以使 `YYYY-MM-DD` 格式的日期，也可以是自 1970-01-01 以来到过期日期的天数。值 EXPIRE_DATE 为 -1 表示永不过期。
- `-I, --inactive INACTIVE`：设置账号密码过期 INACTIVE 天后，账号将被锁定。-1 表示关闭此功能。
- `-m, --mindays MIN_DAYS`：设置两次修改密码最少需要间隔 MIN_DAYS 天。
- `-W, --warndays WARN_DAYS`：设置密码过期前 WARN_DAYS 天系统开始提示警告信息。
- `-d, --lastday LAST_DAY`：手动修改上次密码的修改日期，其值 EXPIRE_DATE 可以使 `YYYY-MM-DD` 格式的日期，也可以是自 1970-01-01 以来上次修改密码的天数。如果指定 LAST_DAY 的值为 0，则用户在下次登录系统时将强制该用户修改密码。

> 注意：再次提醒，用户的账号过期与用户的密码过期不同。当账号过期后，用户将无法登录到系统中；当密码过期后，用户仍然可以登录到系统中，只是在登录系统时，系统会强制用户修改当前密码。

#### 示例

**修改用户账号的过期日期**
在修改用户的账号过期日期之前，首先通过 `-l` 选项查看 luke1 账号在修改前的信息：
``` sh
[root@localhost ~]# chage -l luke1
Last password change					: Feb 27, 2018
Password expires					: never
Password inactive					: never
Account expires						: Jan 01, 2019
Minimum number of days between password change		: 2
Maximum number of days between password change		: -1
Number of days of warning before password expires	: 45
```
从输出中可以看出，用户的账号过期日期为 2019/1/1。现在，让我们使用 `-E` 选项为 luke1 用户重新设置账号过期日期：

``` sh
[root@localhost ~]# chage -E -1 luke1
[root@localhost ~]#
[root@localhost ~]# chage -l luke1
Last password change					: Feb 27, 2018
Password expires					: never
Password inactive					: never
Account expires						: never
Minimum number of days between password change		: 2
Maximum number of days between password change		: -1
Number of days of warning before password expires	: 45
```
luke1 账号的过期日期被成功设置为了永不过期。
</br>

**设置用户的密码过期时间**
从上面例子中获取到的信息中，我们可以看到，当前用户 luke1 的密码被设置为了永不过期。
这里，我们将通过 `-M` 参数设置该用户密码每次最多保留 90 天，当 90 天过后，用户密码将过期。

``` sh
[root@localhost ~]# chage -M 90 luke1
[root@localhost ~]#
[root@localhost ~]# chage -l luke1
Last password change					: Feb 27, 2018
Password expires					: May 28, 2018
Password inactive					: Jun 02, 2018
Account expires						: never
Minimum number of days between password change		: 2
Maximum number of days between password change		: 90
Number of days of warning before password expires	: 45
```
</br>

**同时修改多项**
下面，我们将尝试同时修改多项：
``` sh
[root@localhost ~]# chage -I -1 -m 0 -M 99999 -E -1 luke1
```
在这个例子中，我们设置了账号用不过期；两次密码修改间距天数不受限制；用户密码用不过期；即使密码过期，账户也永不过期。
</br>

### `userdel` 删除用户
当某个用户不在使用时，我们应当将该用户从系统中移除掉。可以使用 `userdel` 名来来删除某个用户。基本格式为：`userdel [options] LOGIN`。
</br>

下面列出了一些常用的选项：
- `-f, --force`：强制删除用户，即使被删除的用户当前处于登录状态；同时该选项也会强制删除用户的 home 目录和 mail 文件，即使还有其他用户使用同样的目录作为 home 目录。
- `-r, --remove`：移除账户时，同时删掉该账户的 home 目录，及其所有 mail 文件。默认保留这些文件。

#### 示例：
**删除用户**
``` sh
[root@localhost /]$ userdel luke8
[root@localhost /]$ id luke8
id: luke8: no such user
```
用户 luke8 已经不在存在了。
</br>

**删除用户的同时，删除其对用的 home 目录和 mail**
在上面的例子中，我们仅仅是删除了 luke8 用户，但其 home 目录 `/home/luke8/` 及其 mail 文件并没有被移除
``` sh
[root@localhost /]$ ls -l /home/luke8/
total 0
```
通过 `ls` 命令，我们仍然可以访问到 luke8 用户的 home 目录。
如果想要在删除用户时，同时将他的 home 目录一起删掉，可以在 `userdel` 命令中指定 `-r` 选项
``` sh
[root@localhost /]$ useradd luke8
useradd: warning: the home directory already exists.
Not copying any file from skel directory into it.
Creating mailbox file: File exists
[root@localhost /]$ userdel -r luke8
[root@localhost /]$ ls -l /home/luke8
ls: cannot access /home/luke8: No such file or directory
```
我们首先重新创建 luke8 user，系统会返回一些警告信息，提示 luke8 用户要使用的 home 目录已经存在了，这里可以直接忽略警告。
接着在删除用户时指定 `-r` 参数，再次查看 luke8 用户的 home 目录，此时已经不存在了。
`-r` 选项不仅会删除用户的 home 目录，同时也将用户的 mail 文件一并删除掉。

### 用户相关的系统文件

#### /etc/default/useradd

在[创建用户]({{< relref "#用户管理" >}})那一节中，我们直接使用命令 `useradd luke1` 创建一个名为 luke1 的新 user，虽然我们没有指定 `-m` 和 `-U` 参数，系统仍然为我们创建了 `/home/luke1` 目录作为该用户的 home 目录，并且同时创建了一个同名的组作为该用户的主组。这是因为系统为我们提供了一组默认的行为，当我们创建新用户时，如果忽略了某些选项，则系统会使用这些默认行为来协助我们创建用户。这些默认值保存在 `/etc/default/useradd` 中。让我们通过 `cat` 命令来查看该文件中的内容：

``` sh
[root@localhost ~]# cat /etc/default/useradd
# useradd defaults file
GROUP=100             # 如果创建用户时指定了 -N，并且没有指定 -g，则默认使用组 ID 为 100 的组作为新用户的主组
HOME=/home            # 默认在 /home 目录下创建用户 home 目录
INACTIVE=-1           # 默认账户不过期
EXPIRE=               # 默认不设置密码过期天数
SHELL=/bin/bash       # /bin/bash 作为用户的默认 SHELL
SKEL=/etc/skel        # 默认将 /etc/skel 下的所有文件拷贝到新用户的 home 目录下
CREATE_MAIL_SPOOL=yes # 默认创建用户的 mail spool
```

#### /etc/passwd
当一个用户尝试登录系统时，系统首先会查看 `/etc/passwd` 文件，该文件保存了当前系统中所有用户的信息。每当我们新创建一个新用户时，也会在该文件中追加一条记录。同样，当修改或删除某个用户时，也会更新该文件。因此，我们可以将文件 `/etc/passwd` 看做是系统中用户保存用户信息的数据库文件。

`/etc/passwd` 是一个文本文件，系统中的任何一个用户都可以查看它的内容，但只有 root 用户可以修改它的内容。可以通过 `cat` 命令直接查看该文件内容：

``` sh
[root@localhost ~]# cat /etc/passwd
...
luke7:x:1011:1011:Testing user:/home/luke7:/bin/bash
...
```
</br>

也可以借助 `getent` 命令的子命令 `passwd` 来获取全部或指定的某条用户记录信息，如：
``` sh
[root@localhost ~]# getent passwd luke7
luke7:x:1011:1011:Testing user:/home/luke7:/bin/bash
```
> 如果不指定 luke7，则打印出全部用户信息。
</br>

每条用户记录在文件中占用一行，并且由多个字段组成，各个字段之间使用冒号（:）分隔，其格式为：

![etc-passwd](/img/devops/linux-etc-passwd.png)
</br>

1. 用户名：用户的登录名。
2. Password：密码占位符 X，它并不是用户真正的密码。该字段是历史遗留下来的，真正的密码被保存在 `/etc/shadow` 文件中。
3. 用户 ID(UID)：每个用户在系统中都有一个唯一的标识 ID。其中 root ID 为0，1~99 为系统保留 ID。自定义用户起始 ID 为 1000，每创建一个新用户，其 UID 在上一个 UID 基础上依次累加 1。
4. 组 ID(GID)：用户所属的主组。
5. 用户注释：创建用户时通过 `-c` 选项为用户指定的注释信息。
6. Home 目录：用户的 home 目录。当使用一个 home 目录没有被创建的用户登录系统是，目录会被自动切换到系统根目录 `/` 下。
7. 当用户登录系统是自动执行的命令：它通常指向一个 shell。可以通过将该项指定为 `/bin/false` 来禁止用户进行登录操作。

当我们尝试修改该 `/etc/passwd` 内容时，最好是使用命令 `vipw` 来修改，而不是使用一般的编辑器工具。该命令可以在我们修改该文件时自动加入文件锁，防止多用户同时修改造成冲突。
</br>

另外，如果我们手动修改了这些文件，一定要保证修改后的文件和用户信息的正确性，任何一点小错误都可能导致用户无法正确登录到系统中。检查是否有错误最简单的办法是使用 `pwck` 命令。直接在命令行中输入 `pwck` 命令，可以打印出任何需要修复的问题。

#### /etc/shadow
`/etc/shadow` 是另一个比较重要的文件，它存储了所有用户的密码信息和密码过期时间等信息。

``` sh
[root@localhost ~]# cat /etc/shadow
...
luke1:$1$L936UA7E$03ZIw90xe.0f4cZO.MBiJ.:17586:0:99999:7:::
...
```

该文件只有 root 用户有查看权限，与 `/etc/passwd` 类似，文件中的每一行都是一条单独的记录，每条记录中又包含了多个字段。下面对各个字段进行了简单的描述：

1. 用户的登录名。
2. 密码字段。该字段可能有以下几种值：
   - 空值，表明当前用户登录密码为空；
   - 星号代表帐号被锁定；
   - 双叹号表示这个密码已经过期了；
   - `$1$` 表明是用MD5加密；
   - `$2$` 是用Blowfish加密；
   - `$5$` 是用 SHA-256加密；
   - `$6$` 开头的，表明是用SHA-512加密；
3. 密码最后修改时间，其值为距 1970.1.1 号到密码修改那天的天数。
4. 两次密码修改的最小天数间隔。0表示没有限制。
5. 密码最多可以使用的天数，即多少天后密码过期。
6. 密码过期前多少天开始提示警告信息。
7. 密码过期多少天后账号将被禁用
8. 距离 1970.1.1 号多少天后账号将被禁用
9. 最后一个字段为保留字段，没有被使用。

---

## 组管理

在 Linux 系统中，有两种类型的组：主组 和 其他组。每个用户都必须有且只能有一个主组，并且至少属于一个其他组。当新创建一个用户时，如果没有通过 `-g` 参数为这个用户指定一个主组，系统则会自动创建一个与用户名同名的组，并将新创建的组设置为该用户的主组。
</br>

主组与其他组最重要的却别在于，当用户创建一个新文件时，文件所属的组为用户的主组，并且，没有任何主组的用户，将无法登录到系统中；而对用用户的其他组来说，当用户操作一个不属于自己的文件，且文件所属组不是当前用户的主组时，但该用户属于该文件所属组下的成员，即该用户的其他组中包含文件所属的组，则该用户可以以组的权限来操作该文件。

### `groupadd` 创建组

虽然创建用户时，系统可以帮助我们同时创建对应的组，但总有些时候，我们需要手动创建一些组。
Linux 系统命令 `groupadd` 就是用来创建新组的，他的基本格式为：`groupadd [options] group`。
</br>

下面列出了一些常用的选项：
- `-g, --gid GID`： 将值 GID 做为新创建组的组 ID。
- `-f, --force`：当重复创建一个系统中已经存在的组时，`groupadd` 命令将直接退出，并且将命令的执行结果设置为失败。`-f` 选项将通知系统，即使创建一个已经存在的组时，命令也将返回成功。

#### 示例

**创建组时指定组 ID**
每个组都有一个系统唯一的标识符 组 ID（GID），当创建组时，系统将默认分给一个 ID 做为新创建组的组 ID。我们可以通过使用 `-g` 参数，为新创建的组指定一个自定义的组 ID。
下面示例展示了如何创建一个组 ID 为 11000 的新组 grouptesting：

``` sh
[root@localhost ~]# groupadd -g 1100 grouptesting
```
</br>

**强制创建新组**
在上面的命令中，我们创建了一个名为 grouptesting 的新组，如果再次尝试创建一个同名的组，则将提示错误，同时命令返回失败：
``` sh
[root@localhost ~]# groupadd grouptesting
groupadd: group 'grouptesting' already exists
[root@localhost ~]# echo $?
9
```
可以看到，`groupadd` 命令的返回值为 9，表示该组已经存在，命令执行失败。
</br>

使用 `-f` 参数：
``` sh
[root@localhost ~]# groupadd -f grouptesting
[root@localhost ~]# echo $?
0
```
当我们指定了 `-f` 参数后，`groupadd` 命令的返回值为0，表示执行成功。
</br>

### 查看组信息
`groups` 命令可以用来获取指定用户的组信息，如果没有指定登录用户，则获取当前用户组信息，如：

``` sh
[root@localhost ~]# groups
root
[root@localhost ~]#
[root@localhost ~]# getent group luke1
luke1:x:1002:luke1
```
</br>

可以使用 `getent group` 命令获取某个组的信息，如：

``` sh
[root@localhost ~]# getent group luke1
luke1:x:1002:luke1
```
如果没有指定组名，则获取当前系统中的所有组信息。

### `groupmod` 修改组信息

`groupmod` 命令可以用来修改一个已经存在的组，其格式为： `groupmod [options] GROUP`。
</br>

下面列出了一些常用的选项：
- `-g, --gid GID`：修改组 ID，
- `-n, --new-name NEW_GROUP`：更新组名

#### 示例
更新 grouptesting 组名为 grouptest，同时修改它的组 ID：

``` sh
[root@localhost ~]# groupmod -n 1200 -g grouptest
```

### `groupdel` 删除组
当某个组不在使用时，我们应当使用系统命令 `groupdel` 删除这个组，并将要删除的组名作为参数传递给该命令。
> 注意：我们无法删除某个仍然作为其他用户主组的组。
</br>

下面例子展示了如何删除我们刚刚创建的新组 grouptesting：
``` sh
[root@localhost ~]# groupdel grouptesting
```
</br>

> 注意：当删除某个组之后，任何所属组为被删除组的文件的组信息都将失效，同时显示为被删除组的组 ID。

### 组相关的系统文件

#### /etc/group
系统中所有组的信息全部保存在 `/etc/group` 文件中，与用户信息一样，每条组记录在文件中占用单独一行，记录一共有3个字段，分别为 组名、组密码占位符 `X` 组 ID 以及。可以使用 `cat` 命令直接查该文件内容：
``` sh
[root@localhost ~]# cat /etc/group
```
</br>

也可以借助 `getent` 命令的子命令 `group` 来获取全部或指定的某条组记录信息，如：
``` sh
[root@localhost ~]# getent group root
root:x:0:
```

[^1]:很多系统还提供了更加高级的 `adduser` 命令，而在 CentOS 7 中，`adduser` 则是以 `useradd` 命令的软连接的形式存在的。
