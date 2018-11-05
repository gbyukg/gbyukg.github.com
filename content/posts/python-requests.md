---
title: "Python Requests 库"
date: 2018-03-07T17:43:20+08:00
tags:
  - Python
categories:
  - Programming
keywords:
  - requests
draft: false
---

requests 是一个款基于 urllib3 开发的 HTTP 开源库，该库为我们提供了丰富的 HTTP 请求相关函数，主要功能包括：
- 支持发送多种类型的请求，包括 GET、POST、PUT、DELETE、OPTIONS、HEAD、PATCH。
- 支持连接池，提升效率。
- 其提供的 session 模块能够自动保存并处理 cookies 等信息，大大节约开发成本。
- 支持基本的 HTTP 认证功能。
- 支持文件上传下载等功能。
- 支持 SSL
- 支持 HTTP 代理

由于该库简单，高效，功能齐全等特性，被众多大厂商所青睐。本文意在向读者简单介绍该库的一些基本用法，在阅读本文时，推荐读者参考该库的[官方文档](http://docs.python-requests.org/en/master/user/install/)一起学习。

## 安装

requests 库并不属于 Python 的内置库，因此在使用前，需要手动安装，可以使用 `pip` 命令直接安装：
``` sh
pip install requests
```
</br>

当安装成功后，就可以在代码中引用该库了：
``` py
import requests
```

## 发送请求
对于 HTTP 库来说，最基本的功能就是发送 HTTP 请求，requests 库提供了多种发送请求的方法，分别用于支持 HTTP 协议中定义的不同 请求类型[^1]，这些请求类型包括：GET、POST、PUT、DELETE、HEAD、OPTIONS、PATCH等，下面让我们依次介绍如何使用 requests 库来发送这些请求。

### GET 请求
首先，让我们看一下 GET 请求。HTTP GET 方法被设计成用于获取某个特定资源信息的，通常用于检索数据。requests 库中提供的 `get` 方法可以用来向某个服务器发送一个 GET 请求。其方法原型为：`get(url, params=None, **kwargs)`。
其中：

- `url` 为必选参数，接收一个字符串类型的值，指明要发送请求的 URL 地址。
- `params` 为可选参数，指定发送请求时的附加数据。
- `**kwargs` 为一些其他可选参数，在后面的讲解中会依次引入介绍。

该方法返回一个 [`Response`]({{< relref "#response-对象" >}}) 对象。
</br>

接下来让我们看一个具体的示例，通过 Github API 来获取某个特定用户的信息：

``` python
>>> r = requests.get('https://api.github.com/users/gbyukg')
```

在这个示例，我们使用了 `get` 方法向 `https://api.github.com/users/gbyukg` 地址发送了一个 GET 请求，并将返回的 Response 对象保存到了变量 `r` 中，通过调用 Response 对象提供的 `text` 方法，可以获取到 HTTP 请求响应体中的内容：

``` python
>>> r.text
>>> '{"login":"gbyukg","id":36716,...}'
```

> 注意：`text` 被定义成了属性函数，因此调用时没有在该方法结尾添加 `()`。

#### 向 GET 请求中发送数据

很大一部分情况，当我们向某个服务器发送一个 GET 请求的同时，还需要向服务器传递一些附加的数据信息。`get` 方法支持两种方式来发送这些附加数据：在 URL 中指定附加数据 和 通过 `params` 参数传递。下面让我们依次了解这两种发送数据的方式。

##### 通过 URL 发送数据

当我们在浏览器中访问某个需要传送附加数据的请求时，需要将这些附加数据追加到服务器 URL 地址中去，例如访问 `http://httpbin.org/get?key1=value1&key2=value2` 时，会同时将附加数据 key1=value1 和 key2=value2 传送到服务器中。
</br>

下面是当我们在浏览器中打开该地址时的返回结果：
``` json
{
  "args": {
    "key1": "value1",
    "key2": "value2"
  },
  ...
}
```
</br>

通过将数据附加到 URL 地址中的方式，同样适用于 `get` 方法，如：

``` py
>>> r = requests.get('http://httpbin.org/get?key1=value1&key2=value2')

>>> r.text
>>> '{\n  "args": {\n    "key1": "value1", \n    "key2": "value2"\n  },... }
```

可以看到，在 `args` 中同样返回来这两个附加参数。
</br>

##### 使用 `params` 参数传递请求数据

除了将所要传递的参数附加到 URL 地址中外，我们还可以将这些参数以字典的方式传递给 `get` 方法的 `params` 参数，如：

``` python
>>> payload = {'key1': 'value1', 'key2': 'value2'}
>>> r = requests.get('http://httpbin.org/get', params=payload)

>>> r.text
>>> '{\n  "args": {\n    "key1": "value1", \n    "key2": "value2"\n  },... }
```

获取到的响应体与上面例子完全相同。
</br>

查看 Response 对象的 `url` 属性来获取最终发送请求的 URL 地址：

``` py
>>> r.url
>>> http://httpbin.org/get?key2=value2&key1=value1
```

可以发现，`get` 方法实际上就是将这些参数解析后保存到了 URL 地址中，并最终以第一个示例中的方式发送给服务器。
</br>

有些时候，在要发送的数据中，可能一个键值对应多个要传递的值，如在 URL `http://httpbin.org/get?key1=value1&key2=value2&key2=value3` 中，key2 分别对应 value2 和 value3 两个值，当以字典的方式传递给 `params` 参数，可以将这两个值保存到一个可迭代对象中传递给 key2 键，requests 库会自动为我们处理这种含有多个值的情况，如：

``` py
>>> # key2 的值是一个元组
>>> payload = {'key1': 'value1', 'key2': ('value2', 'value3')}
>>> r = requests.get('http://httpbin.org/get', params=payload)

>>> r.text
>>> # key2 中此时包含了两个值
>>> '{\n  "args": {\n    "key1": "value1", \n    "key2": [\n      "value2", \n      "value3"\n    ]\n  } ... }

>>> r.url
>>> 'http://httpbin.org/get?key1=value1&key2=value2&key2=value3'
```

> 其中，key2的值也可以使用列表代替。

---

### POST 请求

HTTP POST 方法被设计成用于向服务器特定资源发送数据的，通常用于创建或更新服务器中的资源。requests 库中提供的 `post` 方法可以用来向某个服务器发送一个 POST 请求。其方法原型为：`post(url, data=None, json=None, **kwargs)`。
其中：

- `url` 为必选参数，字符串类型，指明要发送请求的 URL 地址。
- `data` 为可选参数，指定发送请求时的附加数据，该值可以是以下类型：
  - 字典类型：字典中每个元素都将作为一个参数传递给服务器，其中每个元素的键作为要发送数据的 key，值作为要发送数据的值；
  - 元组类型：如果是元组类型，则元组中的每个元素必须是一个包含有两个元素的元组，每个元组中的两个元素分别作为要传递数据的键和值；
  - 字符串型：如果是字符串类型，则必须是能够被正确转换成 JSON 格式的字符串；
- `json` 为可选参数，JSON 格式的字符串类型，指定发送请求时的附加数据。
- `**kwargs` 为一些其他可选参数，在后面的讲解中会依次引入介绍。

与 `get` 方法一样，该方法返回一个 Response 对象。
</br>

虽然 GET 请求可以向服务器端发送数据，但 POST 是专门被设计成用来向服务器发送附加数据的请求的，`post` 方法支持两个传送附加数据的参数，下面让我们看一下如何使用这两个参数。

#### `data` 参数
`post` 方法可以将我们传递给 `data` 参数的值作为附加值发送给我们所请求的服务器。该参数可以接收 3 种不同类型的值，分别是：字典类型、元组类型和字符串类型。
</br>

##### 字典类型

当传递给 `data` 参数一个字典时，字典的键和值将分别作为被发送数据的名称和所对应的值，如：

``` py
>>> r = requests.post('http://httpbin.org/post', data = {'key':'value'})
>>> r.json()
>>>
{
  'args': {},
  'data': '',
  'files': {},
  'form': {
    'key': 'value' # 以字典的方式传递给 data 参数的数据
  },
  ...
}
```

在这个例子中，我们使用了 response 对象的 [`json`]({{< relref "#json-参数" >}}) 方法来获取消息体中的内容，该方法会将返回的数据转换成 Python 对应的数据类型，这里使用 `json` 方法，主要是其输出格式方便我们观察。
在返回的数据中，可以看到，我们传送的数据被保存到了 `form` 字段中。
</br>

与 `get` 方法类似，也可以将一个除字符串之外的可迭代对象作为字典中某个元素的值，为要发送的某个数据提供多个值：

``` py
payload = {'key1': 'value1', 'key2': ('value2', 'value3')}
r = requests.post('http://httpbin.org/post', data=payload)
r.json()
{
  'args': {},
  'data': '',
  'files': {},
  'form': {
    'key1': 'value1',
    'key2': [ # 同时传递多个值给 key2
      'value2',
      'value3'
      ]
    },
  ...
}
```
</br>

#####  元组/列表等可迭代对象类型

我们还可以将一个元组或列表等可迭代对象传递给 `data` 参数，其中该对象中的每个元素又是一个含有两个元素的元组或列表对象，这两个元素分别作为附加数据的名称和值，如：

``` py
>>> # payload = [['key1', 'value1'], ['key1', 'value2']]
>>> # payload = [('key1', 'value1'), ('key1', 'value2')]
>>> # payload = (['key1', 'value1'], ['key1', 'value2'])
>>> # payload = (('key1', 'value1'), ('key1', 'value2'))
>>> # 通过这 4 种方式传递的数据效果完全相同
>>> payload = (('key1', 'value1'), ('key1', 'value2'))
>>> r = requests.post('http://httpbin.org/post', data=payload)
>>> r.text
{
  ...
  "form": {
    "key1": [
      "value1",
      "value2"
    ]
  },
  ...
}
```
</br>

##### 字符串类型

最后一种方式是直接将一个字符串传递给 `data` 参数：

``` py
>>> r = requests.post('http://httpbin.org/post', data="{key1: 'value1'}")
```

或是通过 json 模块将 Python 对象转换成字符串对象：

``` py
>>> import json
>>> r = requests.post('http://httpbin.org/post', data=json.dumps({'key1': 'value1'}))
```

获取 HTTP 响应内容：

``` py
>>> r.json()
>>>
{
  'args': {},
  'data': "{key1: 'value1'}",
  ...
  'form': {},
  ...
}
```
</br>

细心的你可以已经发现了，当我们通过字典和元组传递参数时，在返回的 HTTP 响应体中，这些参数被保存到了 `form` 字段中，而当我们使用字符串类型传递参数时，数据被保存到了 `data` 字典中。虽然这是 `httpbin` 服务器有意而为之，但这也真实地反映出了服务器端在接收到请求时这些附加参数被保存的位置信息，为什么这些附加数据会保存在不同的位置呢？
</br>

这是因为当传递给 `data` 一个字典或是元组时，request 会自动向请求头中添加 `Content-Type:application/x-www-form-urlencoded` 头信息，这样会将我们传递的数据自动转换成 form 表单编码数据（即就像是通过提交 form 表单时发送的请求那样）; 而当我们直接传递一个字符串类型时，request 不会做任何转换。我们可以通过返回的 response 对象的 `request.headers` 来获取发送的 HTTP 请求头信息，如：

``` py
>>> # 首先发送一个字典作为 data 参数值的 POST 请求
>>> r = requests.post('http://httpbin.org/post', data = {'key':'value'})
>>> # 获取请求头信息
>>> r.request.headers
>>> # 默认为我们添加了 'Content-Type': 'application/x-www-form-urlencoded' 头
>>> {'User-Agent': 'python-requests/2.18.4', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive', 'Content-Length': '9', 'Content-Type': 'application/x-www-form-urlencoded'}

>>> # 接着发送一个以字符串作为 data 参数值的 POST 请求
>>> r = requests.post('http://httpbin.org/post', data="{key1: 'value1'}")
>>> r.request.headers
>>> {'User-Agent': 'python-requests/2.18.4', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive', 'Content-Length': '16'}
```

#### `json` 参数

除了使用 `data` 传递数据之外，`post` 方法还提供了另外一个参数 `json` 来传递数据，如：

``` python
>>> url = 'http://httpbin.org/post'
>>> payload = {'some': 'data'}
>>> r = requests.post(url, json=payload)
>>> r.json()
>>>
{'args': {},
  'data': "{some: 'data'}",
  ...
  'form': {},
  ...
  }
```
</br>

使用 `json` 参数来向服务器发送数据时，requests 库会自动将头信息 `Content-Type:application/json` 添加到 HTTP 请求头中，通常我们在返回的消息体中是 JSON 格式的字符串时使用这种头信息，如访问 Github API 服务器。

``` python
>>> r.request.headers
>>> {'User-Agent': 'python-requests/2.18.4', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive', 'Content-Length': '16', 'Content-Type': 'application/json'}
```

> 注意：如果同时指定了 `data` 和 `json` 参数，则 `json` 参数将被忽略。

### PUT 请求

HTTP 的 PUT 方法被设计成用来替换当前服务器中已有资源的，通常用于将新的资源来替换某个已有的资源。requests 库中提供的 `put` 方法用来发送一个 PUT 请求。其方法原型为 `put(url, data=None, **kwargs)`。除了不接受 `json` 参数外，该方法与 `post` 方法完全一样。
</br>

下面示例展示了通过 `put` 方法发送 PUT 请求：

``` py
>>> # 使用字典作为参数
>>> r = requests.put('http://httpbin.org/put', data = {'key':'value'})
>>> r.json()
>>>
{
  'args': {},
  'data': '',
  'files': {},
  'form': {
    'key': 'value' # 以字典的方式传递给 data 参数的数据
  },
  ...
}

>>> # 使用字符串作为参数
>>> r = requests.put('http://httpbin.org/put', data = "{'key':'value'}")
>>> r.json()
>>>
{
  'args': {},
  'data': "{key1: 'value1'}",
  ...
  'form': {},
  ...
}
```

### PATCH 请求

HTTP PATCH 方法被设计成用于更新服务器某个资源的部分信息。requests 库中的 `patch` 方法可用于向服务器发送一个 PATCH 请求。其方法原型为： `patch(url, data=None, **kwargs)`。除了不接受 `json` 参数外，该方法与 `post` 方法完全一样。
</br>

示例：

``` py
>>> r = requests.patch('http://httpbin.org/patch', data = {'key':'value'})
>>> r.json()
>>>
{
  'args': {},
  'data': '',
  'files': {},
  'form': {
    'key': 'value'
  },
  ...
}
```

### DELETE 请求

HTTP DELETE 方法被设计成用于从服务器端删除某个资源。requests 库中的 `delete` 方法用于向服务器发送一个 DELETE 请求。 其方法原型为：`delete(url, **kwargs)`。
</br>

示例：
``` py
>>> r = requests.delete('http://httpbin.org/delete')
```

### HEAD 请求

HTTP HEAD 方法被用来设计成获取查询 HTTP 响应头信息的，HEAD 方法不会返回任何响应体信息。requests 库中的 `head` 方法用来向某个服务器发送一个 HEAD 请求。其方法原型为：`head(url, **kwargs)`。
</br>

示例：
``` python
>>> r = requests.head('http://httpbin.org/get')
>>> r.headers
>>> 当我们尝试去读
>>> r.json()
```

### OPTIONS 请求

除了可以发送 GET 请求和 POST 请求外，requests 库还提供了发送其他请求类型的方法，包括 PUT，DELETE，HEAD 和 OPTIONS 等请求，如：

{{< highlight python "linenos=table,linenostart=1" >}}
r = requests.put('http://httpbin.org/put', data = {'key':'value'})
r = requests.delete('http://httpbin.org/delete')
r = requests.head('http://httpbin.org/get')
r = requests.options('http://httpbin.org/get')
{{< / highlight >}}

### `request` 方法
`request` 方法是上述所有发送请求方法的根基方法，即所有方法最终都是通过调用 `request` 方法来实现的。其方法原型为：`request(method, url, **kwargs)`，该方法可以接收多个参数，下面列出了所有可用参数：
- `method`：指明要发送请求的类型，其值可以是 `get`、`post`、`put`、`delete`、`head`、`options`。
- `url`：发送请求的 URL 地址
- `params`：当 method 参数指定为 get 时使用
- `data`：
- `json`：
- `header`：
- `cookies`：
- `files`：
- `auth`：
- `timeout`：
- `allow_redirects`：
- `proxies`：
- `verify`：
- `stream`：默认情况下，当一个请求结束后，requests 会读取所有 HTTP 响应体中的信息到内存中，如果指定该选项值为 True，则返回一个 socket 流，只有在需要时，才真正读取响应体中的内容。对于处理返回结果中包含了大量数据的情况，会节省更多内存和时间。
- `cert`：

## Response 对象
无论使用那种方法发送请求，最终都将返回一个 response 对象。response 对象是 requests 内置类 `Response` 的一个实例，response 对象里包含了所有的 HTTP 响应信息，包括获取响应体，响应头信息，HTTP 状态码，cookies 信息等，我们将依次对这些属性进行讲解。
</br>

### 获取响应体内容
在上面的例子中，我们已经使用过了 response 的 `text` 方法来获取 HTTP 响应信息体，其实，request 不止是提供了这一个方法来获取获取响应体信息，下面让我们一次了解一下这些方法。
</br>

**`text`方法**
`text` 是一个属性函数，当我们尝试使用该方法来读取 HTTP 响应体时，requests 库首先会使用 respone 的 `encoding` 属性对其进行编码，最终将编码后的结果返回回来。如果在调用 `text` 方法前，没有明确指定 response 的 `encoding` 属性，respone 将尝试按照下列顺序获取默认的编码规则：
1. 如果响应头 `Content-Type` 中指定了编码规则，则将 `encoding` 设置为该指定的编码规则并对消息体进行编码。
  > 例如，如果响应头中包含：`Content-Type: application/json; charset=utf-8` 头信息，则 requests 使用 `utf-8` 对响应体进行编码；

2. 如果响应头 `Content-Type` 的值为 `text/*`，即包含 `text` 信息，则将 `encoding` 属性这是为 `ISO-8859-1` 并对消息体进行编码。
  > 例如，如果响应头中包含：`Content-Type: text/html` 头信息，则 requests 使用 `ISO-8859-1` 对响应体进行编码；

3. 尝试使用 `chardet` 库对内容进行分析后获取一个最合适的编码规则对消息体进行编码。
  > 注意，这种方式获取到的编码规则并不会赋值给 `encoding` 属性，因此无法通过 `r.encoding` 方式来获取当前的编码规则。

{{< highlight python "linenos=table,linenostart=1" >}}
r = requests.get('http://httpbin.org/get')
r.encoding
>>>
r.text
>>> '{\n  "args": {}, ... }
{{< / highlight >}}

我们也可以在调用 `text` 方法前，明确指定一个编码规则对返回的内容进行编码，如：

{{< highlight python "linenos=table,linenostart=1" >}}
r = requests.get('http://httpbin.org/get')

r.encoding = 'ISO-8859-1'
r.encoding
>>> ISO-8859-1

r.text
>>> '{\n  "args": {}, ... }'
{{< / highlight >}}
</br>

**`content`方法**
`content` 是一个属性函数，通过该方法获取到的消息体为 bytes 类型。当我们尝试获取二进制文件时通常使用这种方式，比如下面的例子展示了 如何下载一个图片：

{{< highlight python "linenos=table,linenostart=1" >}}
r = requests.get('https://httpbin.org/image/png')
with open('/tmp/httpbin-image.png', 'bw+') as f:
    f.write(r.content)
{{< / highlight >}}
</br>

**`json`方法**
如果 HTTP 请求返回的消息体是 JSON 格式的字符串，则我们可以使用 `json` 方法，将返回的字符串转换成 Python 对象，如果返回的对象无法被正确转换，则抛出 `ValueError: No JSON object could be decoded.` 异常。

{{< highlight python "linenos=table,linenostart=1" >}}
r = requests.get('https://api.github.com/users/gbyukg')
r.json()
>>>
{
  'avatar_url': 'https://avatars3.githubusercontent.com/u/36716?v=4',
  'bio': None,
  'blog': 'http://www.cnblogs.com/gbyukg/',
  'company': 'soft',
  ...
}

# 获取某个属性
r.json()['avatar_url']
>>> 'https://avatars3.githubusercontent.com/u/36716?v=4'
{{< / highlight >}}

> 注意，`json` 方法并没有被设计成属性函数，因此在调用该方法时需要加上括号`()`。
</br>

**`raw`属性**
`raw` 是 response 对象中的一个属性，而不是方法，它指向了原始 socket 响应对象，该响应对象包含了一系列方法，我们可以向访问文件流那样访问它里面的内容。
当我们尝试使用 `raw` 属性获取响应体内容时，在请求方法中，必须同时指定 `stream=Tre` 参数，来防止 requests 库自动读取获取响应体中的内容到内存中，当读取响应体内容比较多的请求时会节省很多内存和时间，如：

{{< highlight python "linenos=table,linenostart=1" >}}
r = requests.get('https://www.python.org//static/img/python-logo.png', stream=True)
r.raw
>>> <urllib3.response.HTTPResponse at 0x1043c70f0>

# 获取当前流中的剩余未读字节数
r.raw.length_remaining
>>> 10102

# 获取当前流指针索引
r.raw.tell()
>>> 0

# 读取 10 个字节
r.raw.read(10)
>>> b'\x89PNG\r\n\x1a\n\x00\x00'

# 再次去读剩余字节数
r.raw.length_remaining
>>> 10092

# 当前流指针向前移动10个字节，因为我们已经读取了 10 个字节
r.raw.tell()
>>> 10
{{< / highlight >}}
更多关于 raw 对象的使用方法，请参考 [urllib3.response module](http://urllib3.readthedocs.io/en/latest/reference/#module-urllib3.response)
</br>

**`iter_content`方法**
虽然使用 response 的 `raw` 属性读取响应体内容时可以让我们在真正需要的时候手动获取这些内容，response 对象提供了更加方便的方法 `iter_content`，该方法实际上就是通过读取 `raw.stream` 文件流来获取内容，它可以接收两个参数：
- `chunk_size`：整数型参数，表示每次读取多少个字节数，默认为 1
- `decode_unicode`：布尔型参数，如果指定为 True， 则对读取的内容使用 r.encoding 进行编码，默认为 False。

{{< highlight python "linenos=table,linenostart=1" >}}
with open(filename, 'wb') as fd:
    for chunk in r.iter_content(chunk_size=128):
        fd.write(chunk)
{{< / highlight >}}

**`iter_lines`方法**

{{< highlight python "linenos=table,linenostart=1" >}}
r.request
{{< / highlight >}}
</br>

## `request` 对象

**`方法`**

### `ok`

## 属性
status_code, headers, 

## 自定义请求头

## 上传下载文件

## cookies

## session

## 重定向

## 历史记录

## certificat

## 错误和异常

---

DEFAULT_CA_BUNDLE_PATH：/usr/local/lib/python2.7/site-packages/certifi/cacert.pem

[^1]: 更多详细信息，请参考 [HTTP request methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)