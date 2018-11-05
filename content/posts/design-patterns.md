---
title: "Python设计模式之 - 单例模式"
date: 2018-01-25T22:52:27+08:00
keywords:
  - Python
  - 设计模式
  - singleton
  - 单例模式
tags:
  - Python
  - Design Patterns
categories:
  - Programming
---

代码写的越多，就愈发对代码的结构要求更多，常常会因为如何实现一个类或是方法而纠结几个小时。编码，不仅仅是为了完成某个功能，它更像是一种艺术，结构设计良好的代码，不仅可以大大地提高可读性和维护性，还能令人赏心悦目，心旷神怡。
</br>

设计模式，就是为了解决某些开发过程中的实际问题而提供的一些编码解决方案，这些方案是由很多开发人员通过在平时的开发中总结出来的一套比较成熟的解决办法，设计模式不依赖于编程语言本身，任何面向对象编程语言都可以套用这些通用的设计模式，虽然不同的语言之间在实现的过程中会有一些差异，但总的思想是一样的。学习设计模式，将会受益终身！
</br>

从本文开始，我将一一记录下我所学到的设计模式，那么，开始吧！

## 单例模式

每种设计模式都尝试解决一种问题

第一个设计模式-单例模式：单例模式应该是所有设计模式之中最简单，也是应用最广泛的一种设计模式了。单例模式，顾名思义，就是在整个代码的生命周期内，只有一个类的实例存在，或者说，对于一个单例模式的类来说，无论实例化它多少次，最终都只会返回同一个实例对象。
</br>

这通常是很有用的，比如在我们的项目中，用于访问数据库的 DB 类，在任意时刻，我们都希望只有一个对象来访问我们的数据库资源，这样，在同一时刻，对数据库发起多个操作请求时，才不会对资源的访问造成冲突； 在比如，用于记录日志信息的 log 类，如果不能保证同时只有一个日志类的实例，势必会造成日志的混乱，因为多个不同的日志实例同时向同一个日志文件中写入信息时，所有信息将会穿插在一起被保存到日志文件中，显然这并不是我们所期望的。
</br>

单例模式 UML 图：

![This is an image](/img/python/SingletonPattern.png)
</br>

下面将详细介绍在 Python 中实现单例模式的各种方法。

---

### 通过 `__new__` 来实现的单例模式

在 Python 中，最简单的实现方法，就是通过 Python 中的 `__new__` 方法，来返回我们所需的实例。

{{< highlight python "linenos=table,hl_lines=2 4,linenostart=1" >}}
class Singleton(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance

s1 = Singleton()
print("Object created", s1)

s2 = Singleton()
print("Object created", s2)
{{< / highlight >}}

输出结果：

```
Object created <__main__.Singleton object at 0x10e054d68>
Object created <__main__.Singleton object at 0x10e054d68>
```

可以看到，虽然代码中实例化了两次 `Singleton` 类 `s1` 和 `s2`， 但他们返回的确是同一个对象。

__代码解析__:
- 第 2 行：实现 `__new__` 方法，注意， Python 会自动将 `Singleton` 类本身作为第一个参数传递个该方法。
- 第 4 行：创建一个类属性 `instance`，并将新创建的对象赋给该属性。

### 通过类方法实现单例模式

另一种常用的方法是，创建一个类方法和一个类属性，在类方法中通过对类属性的判断来创建一个新的类实例或直接返回已有的类实例。
{{< highlight python "linenos=table,hl_lines=2 10-14 18,linenostart=1" >}}
class Singleton(object):
    __instance = None

    def __init__(self):
        if not Singleton._instance:
            print("initializing...")
        else:
            print("Instance already created:", self.getInstance())

    @classmethod
    def getInstance(cls):
        if not cls._instance:
            cls.__instance = Singleton()
        return cls.__instance

s1 = Singleton()

s2 = Singleton.getInstance()
print("Object created", s2)

s2 = Singleton()
{{< / highlight >}}

输出：

```
initializing...
initializing...
Object created <__main__.Singleton object at 0x10b717c50>
Instance already created: <__main__.Singleton object at 0x10b717c50>
```

通过这种方式方法实现的单例模式，只有在我们真正需要创建单例实例时，通过明确调用类方法 `getInstance()` 才会返回这个单例实例，而并不像第一个例子中那样，实例化类后就会自动返回实例，因此通过这种方式实现的单例模式，也尝尝被称作 **懒汉模式**。

#### Python 中懒汉模式的问题
由于 Python 中并没有实现面向对象中的封装，类似 Java 中的 `public`，`protect` 以及 `private` 等关键字在 Python 中也没有得到实现，因此懒汉模式并不能像在 Java 中那样发挥到极致，因为我们无法将 `Singleton` 类的构造方法定义为私有属性，这使得我们仍然可以使通过 `s = Singleton()` 的方式来实例化出许多不同的类实例来，而这些实例又不属于同一个实例：

``` py
s1 = Singleton()
print(id(s1))
s2 = Singleton()
print(id(s2))
s3 = Singleton()
print(id(s3))
```

输出结果：

```
initializing...
4385455352
initializing...
4385455240
initializing...
4385455072
```

从输出结果看来，每个实例化出来的实例仍然是不同的实例, 因此，在 Python 中，使用懒汉模式实现的单例模式时，开发人员必须确保实例时通过调用正确的类方法来获得的。

[metaclass]({{< relref "python-metaclass.md" >}})

