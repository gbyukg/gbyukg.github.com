---
title: "Kubernetes"
date: 2018-03-13T21:01:25+08:00
keywords:
  -
tags:
  - Docker
  - Kubernetes
categories:
  - DevOps
draft: true
---

## kubectl

`kubectl` 是 Kubernetes 的官方客户端，它实际上是一个用来与 Kubernetes API 进行交互的命令行工具。

``` sh
# 查看集群健康状态
kubectl get componentstatus
```

输出结果：
```
NAME                 STATUS    MESSAGE              ERROR
controller-manager   Healthy   ok
scheduler            Healthy   ok
etcd-0               Healthy   {"health": "true"}
```

其中，`controller-manager` 用于运行管理集群行为的各种控制器：例如，确保所有服务的副本正常运行。`scheduler` 确保寄存中不同的 pods 被放到了不同的节点中。最后，`etcd` 是一个用于存储所有 API 对象的存储服务。

## 列出所有节点

``` sh
kubectl get nodes
```

Kubernetes 节点有两类：用于管理节点的 `master` 节点，在 master 节点中运行着一些类似于 API 服务，scheduler 等容器， 和用于运行我们所有应用程序容器的 `worker` 节点。一般情况下，Kubernetes 是不会为 master 节点分配任何任务。

获取某个节点的详细信息

``` sh
kubectl describe node devdocker01
```

## Cluster Components

### Kubernetes Proxy

Kubernetes 代理主要用于将集群中的网络请求转发到 load-balanced 服务中，因此，Kubernetes 中的每个节点都需要有一个代理。集群节点中都是通过 Kubernetes API 中的 `DaemonSet` 对象实现的。如果集群节点中的代理是通过 `DeamonSet` 来实现的，则可以使用下面命令查看代理信息：

``` sh
kubectl get daemonSets --namespace=kube-system kube-proxy
```

### Kubernetes DNS
Kubernetes DNS 服务运行在 master 节点上，该服务为集群中定义的服务提供命名和发现功能。作为一个 Kubernetes 的 deployment，根据集群的大小，我们也可以自定义 DNS 服务的数量。通过下面命令查看 DNS 信息

``` sh
kubectl get deployments --namespace=kube-system kube-dns
```

还有一个服务为 DNS 提供了 load-balancing 功能。

``` sh
kubectl get services --namespace=kube-system kube-dns
```

### Kubernetes UI

``` sh
# 启动 UI
kubectl proxy

# 获取 UI deployment
kubectl get deployments --namespace=kube-system kubernetes-dashboard

# 获取 UI service
kubectl get services --namespace=kube-system kubernetes-dashboard
```

## kubectl 命令

### Namespaces

Kubernetes 使用 namespaces 来组织节点中的对象。我们可以将 namespaces 看做是文件夹，每个文件夹下面都保存了一系列对象。默认情况下，`kubectl` 命令使用默认的命名空间。如果想要指定不同的命名空间，可以通过 `kubectl` 的 `--namespace` 参数来指定，如：`kubectl --name-space=mystuff`

### Contexts
`context` 可以帮助我们永久更改 namespace 等属性。它是从 `kubectl` 配置文件中获取信息的，配置文件一般默认在 `/$HOME/.kube/config`。该配置文件同时也存储了如何查找和认证节点信息。例如，创建一个不同命名空间的 kubectl 命令：

``` sh
kubectl config set-context my-context --namespace=mystuff
```

当创建完以后，我们还要手动指定使其生效

``` sh
kubectl config use-context my-context
```

通过 `set-context` 的 `--users` 或 `--clusters` 参数，我们还可以为不同的节点或不同的用户管理授权方式。

### 查看 Kubernetes API 对象

Kubernetes 中的一切资源都被看做是一个 RESTful 资源。这些资源被看做为 Kubernetes 的对象。每个对象都有一个唯一的 HTTP 路径；例如，`https://your-k8s.com/api/v1/namespaces/default/pods/my-pod` 指向了默认的 namespace 下的名为 `my-pod` 的 pod。`kubectl` 命令就是通过访问这些 HTTP 地址来获取 Kubernetes 对象的。
</br>

`kubectl` 的 `get` 自命令是查看 Kubernetes 对象的基本命令。`kubectl get <resource-name>` 用来列出当前 namespace 中的所有资源。还可以通过 `kubectl get <resource-name> <object-name>` 来获取某个特定的资源。
</br>

默认情况下，`kubectl` 返回一个对用户友好的输出信息。但是在该信息中，kubernetes 隐藏了很多对象的详细信息。可以通过追加 `-o wide` 参数来获取更详细的信息。我们还可以通过使用 `-o json` 或是 `-o yaml` 参数将输出转换成 JSON 或 yaml 格式来获取完整的输出信息。
</br>

默认情况下，当使用 `kubectl get` 命令获取对用户友好的输出信息时，会同时打印出各列的标题信息，可以使用 `--no-headers` 参数来禁止输出这些信息，这在将输出使用到管道中时非常有用。
</br>

从 object 中获取指定字段

``` sh
kubectl get pods my-pod -o jsonpath --template={.status.podIP}
```
</br>

获取某个对象的详细描述信息

``` sh
kubectl describe <resource-name> <obj-name>
```

### 创建、更新及销毁对象
Kubernetes API 中的对象都以 JSON 或是 YAML 文件来表现的。这些文件既可以通过 API 服务器返回回来，也可以作为请求的一部分发送给API 服务器。因此我们可以使用 JSON 或是 YAML 文件来更新，修改或是删除 Kubernetes 中的对象。
</br>

创建对象
``` sh
kubectl apply -f obj.yaml
```
> 在命令行中我们并没有指定要创建对象的类型，这是因为类型已经定义在了 obj.yaml 文件内。

如果在调用该命令时，对象已经存在，则该操作将被看做更新操作。
</br>

``` sh
kubectl edit <resource-name> <obj-name>
```

如果使用 `edit` 子命令，则系统会自动通过系统默认编辑器打开当前 <obj-name> 对象文件，当我们保存该文件后，Kubenetes 会自动为我们更新该对象。
</br>

删除某个对象：

``` sh
kubectl delete -f obj.yaml

# 或是
kubectl delete <resource-name> <obj-name>
```

### 为对象添加标签和注释

我们可以使用 `label` 和 `annote` 子命令为一个对象添加标签和注释，如，为一个名为 bar 的 pod 添加一个 color 标签，其标签值为 red。

``` sh
kubectl label pods bar color=red
```

默认情况下，kubenetes 不允许我们重写 label 和 annotate，如果想要修改这两个属性，需要在命令行同时指定 `--overwrite` 参数
</br>

可以使用 `-<label-name>` 参数来删除 label，如：
``` sh
# 将 bar pod 的标签 color 删除。
kubectl label pods bar color-
```

### Debugging

查看某个正在执行中的 container 的日志信息，可以使用 `-c` 参数指定某个特定的容器。：

``` sh
kubectl logs <pod-name>

# 以交互式的方式显示日志信息
kubectl exec -it <pod-name> -- bash
```

还可以使用 `cp` 命令在容器中复制文件，如：

``` sh
kubectl cp <pod-name>:/path/to/remote/file /path/to/local/file
```

## Pods

Pods 用于将一组应用程序的 containers 和 volumes 封装在同一个执行环境下。Pods 是 Kubernetes 中的最小部署单位。这以为这，在同一个 Pods 下的容器，总是运行在同一台机器上。
</br>

Pod 中的每个容器都有自己独立的 `cgroup`，但是他们共享一系列 Linux 中的 namespaces。
</br>

同一 Pod 中的容器公用同一 IP 地址和端口（network name-space），拥有同样的主机名（hostname，UTS namespace），并且各个容器之间互相能够通过 Linux 系统的 System V IPC 或 POSIX message queues 进行通信，同一 Pod 中的所有容器都可以使用 `localhost` 互相访问，这些容器对于外部来说，是通过端口区分的。然而，不同 Pod 中的应用程序是相互独立的；他们拥有不同的 IP 地址，不同的主机名等。

### 创建 pod

``` sh
kubectl run kuard --image=gcr.io/kuar-demo/kuard-amd64:1

# 获取当前 pods
kubectl get pods
```

通过 YAML 文件部署 pod：
``` yaml
apiVersion: v1
kind: Pod
metadata:
  name: kuard
spec:
  containers:
    - image: gcr.io/kuar-demo/kuard-amd64:1
      name: kuard
      ports:
        - containerPort: 8080
          name: http
          protocol: TCP
```

``` sh
kubectl apply -f kuard-pod.yaml

# 查看某个 pods 详细信息
kubectl describe pods kuard

# 删除 pod
kubectl delete deployments/kuard
# 或
kubectl delete -f kuard-pod.yaml
```