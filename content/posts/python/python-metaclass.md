---
title: "Python 中的 Metaclass"
date: 2018-01-29T13:13:44+08:00
tags:
  - Python
categories:
  - Python
---

Metaclass 作为 Python 中的一种高级用法，开发人员平时很少会直接使用到它。然而一旦我们真正掌握了 metaclass，不仅会让我们编写出更高效的代码，而且会对 Python 中的类会有更加深刻的理解。
</br>

在介绍 Metaclass 之前，先让我们看一下 Python 中的类。

## Python 中的类

相信大家对类的概念并不陌生，我们通常将类比作为蓝图，实例化类就指是根据这个蓝图，创建出一个个具体的实例来。也可以理解为，类就是用来创建类实例对象的：

{{< highlight python "linenos=table,linenostart=1" >}}
class MyClass():
    pass

my_obj = MyClass()
print(my_obj)
# >>> <__main__.MyClass object at 0x101baebe0>
{{< / highlight >}}

在这段代码中，我们创建了一个类的实例对象，并让变量 `my_obj` 指向这个新创建的实例对象，最终成功打印出了这个对象。类 `MyClass` 可以看做是创建实例对象 `my_obj` 的 **材料**。
</br>

### 类也是对象
**在 Python 中，类不仅仅可以用来创建对象的，同时，类本身也是一个对象**（这也符合 Python 中一切皆对象的说法）。
</br>

这意味着我们可以：

  - 将类赋值给一个变量
  - 拷贝类
  - 将类作为参数传递给其他类或方法
  - 为类添加属性

{{< highlight python "linenos=table,hl_lines=1 8 14,linenostart=1" >}}
my_class = MyClass
print(my_class)
# >>> <class '__main__.MyClass'>

def print_obj(obj):
    print(obj)

print_obj(MyClass)
# >>> <class '__main__.MyClass'>

print(hasattr(MyClass, 'new_attribute'))
# >>> False

MyClass.new_attribute = 'foo'
print(hasattr(MyClass, 'new_attribute'))
# >>> True
{{< / highlight >}}

代码解析：
- 第 1 行中我们将类赋值给变量 `my_class`, 并成功地打印出了这个类。
- 第 8 行中将类作为参数，传递给 `print_obj` 函数。
- 第 14 行中，动态为类添加新属性。

既然类本身也是作为一个对象存在的，那么它也一定是通过某些 **材料** 被创建出来的，那么创建类的材料又是什么呢？答案是 `type`。

---

## type 关键字

你一定不会对 Python 中的 `type` 关键字感到陌生，我们通常向它传递一个对象作为唯一的参数，来返回这个对象的类型，例如：

{{< highlight python "linenos=table,linenostart=1" >}}
>>> type(1)
<class 'int'>
>>> type('string')
<class 'str'>
>>> type(())
<class 'tuple'>
{{< / highlight >}}

如果我们继续对 Python 内置的类型进行 `type` 操作，会发生什么呢？

{{< highlight python "linenos=table,linenostart=1" >}}
>>> type(int)
<class 'type'>
>>> type(str)
<class 'type'>
>>> type(tuple)
<class 'type'>
{{< / highlight >}}

会发现他们的类型全部是 `type`。

对我们刚刚定义的类 `MyClass` 进行同样的 type 测试：
{{< highlight python "linenos=table,linenostart=1" >}}
>>> type(MyClass)
<class 'type'>
{{< / highlight >}}

其结果也是 `type`， 这说明这些内置类型，包括我们自定义的 `MyClass` 类，全部都是通过 `type` 创建出来的，这又是为什么呢？

### 使用 type 动态创建类

`type` 不仅仅可以用来判断某个对象的类型，它还有另一个鲜为人知的强大功能，就是用来创建类，其格式为：

``` py
type(name, bases, dict)
```

> 这是典型的多态性，根据不同的参数，其行为也随之不同。

它一共接受三个参数：

- `name`: 字符串类型，指定了我们要创建的类的名称。
- `base` 元组类型，指定了新创建类的所有父类，如果无需继承任何父类，则传递一个空元组。
- `attrs` 字典类型，指定了新创建类中的所有属性，如果不包含任何属性，则传递一个空字典。

下面，我们通过一个简单的例子，创建一个不包含任何属性的空类：

{{< highlight python "linenos=table,linenostart=1" >}}
MyClass = type('MyClass', (), {})
{{< / highlight >}}

我们使用 `type` 关键字创建了一个名为 `MyClass` 的类，这个类没有继承任何父类，也不包含任何属性和方法，并将这个类赋给变量 `MyClass`，使其这个变量指向我们刚刚创建的类。
> 注意：这里我们使用了相同的名字 `MyClass` 同时作为类名和变量名，这并不是必须的，但为了减少疑惑，提升代码可读性，尽量采用统一的名字。

上面的代码完全等价于我们使用 `class` 关键字创建的类：
``` py
class MyClass():
    pass
```

这就是为什么当我们使用 `type(MyClass)` 时，返回的结果为 `type` 类型，这也是 Python 创建类的默认方式。
</br>

现在，让我们看一个更复杂一点的例子:
{{< highlight python "linenos=table,hl_lines=1 4 7,linenostart=1" >}}
def get_name(self):
    return self.name

def init(self, name):
    self.name = name

MyClass = type('MyClass', (object,), {'get_name':get_name, '__init__':init})
my_obj = MyClass('zzl')
print(my_obj.get_name())
# >>> zzl
{{< / highlight >}}

在这个例子中，我们使用 `type` 关键字创建了一个包含有两个方法的类 `MyClass`：
</br>

- 第 1 行和第 4 行分别定义了两个函数 `get_name` 和 `init`， 这里需要注意的是，每个函数都至少需要接收一个名为 `self` 的参数作为第一个参数，因为这两个函数都将要作为类中的方法来被调用。
- 第 7 行中，指定它继承的父类为 `object` 对象，并将类中的属性名和对应的值， 通过字典的方式作为第三个参数传递给 `type`。

通过这段代码，我们创建了一个名为 `MyClass` 的类，类中含有两个方法，一个是构造方法 `__init__`，和一个普通方法 `get_name`。
> _细心的你可能已经发现了，我们为 `__init__` 变量赋予了一个不同的名的函数 `init`，这是完全可以的。_

Python 中的类正是通过这种方式被创建出来的。

---

## 元类（Metaclass）

前文中，我们提及过 `type` 是创建类的默认材料，更准确的来说，元类（Metaclass）才是创建类的材料，即类都是通过元类被创建出来的，而 Python 中默认的元类就是 `type`。

### 自定义元类

除了使用 Python 中默认的元类 `type` 外，我们还可以自己实现自定义的元类。事实上，任何可调用对象都可作为元类，它可以是一个函数，也可以是一个类，我们只需确保该可调用对象接收与 `type` 创建类时所使用的相同的三个参数，并最终返回一个类即可。
</br>

让我们分别看一下当函数和类作为元类时的情况。

#### 1.函数作为元类

考虑这样一种情况，当我们创建一个类时，无论是类中的属性名还是方法名，最终我们都想将它们转化为大写形式，这时，我们就可以使用 Metaclass 来创建我们的类，在 Metaclass 中获取到类中所有用户自定义的属性，并将它们的名字转换成大写即可。

{{< highlight python "linenos=table,hl_lines=1 5 10 14 16-18,linenostart=1" >}}
def upper_attr(future_class_name, future_class_parents, future_class_attr):
    uppercase_attr = {}
    for name, val in future_class_attr.items():
        if not name.startswith('__'):
            uppercase_attr[name.upper()] = val
        else:
            uppercase_attr[name] = val

    # 调用 type 来创建我们需要的类
    return type(future_class_name, future_class_parents, uppercase_attr)

#  通过 upper_attr 创建 MyClass 类
#  类中包含一个名为 foo 的属性
MyClass = upper_attr('MyClass', (), {'foo':'bar'})

print(hasattr(MyClass, 'foo'))  #  False
print(hasattr(MyClass, 'FOO'))  #  True
print(MyClass.FOO) #  bar
{{< / highlight >}}

</br>
代码解释：
</br>

- 第 1 行，我们首先定义了一个函数，该函数接收三个参数，分别作为要创建类的类名，父类及类中的属性传递给该函数。
- 第 2 行，定义一个全局字典，用于保存将属性名转换成大写后的所有类中的属性。
- 第 5 行，将用户自定义的属性名转换成大写，并保存到全局变量 `uppercase_attr` 中。
- 第 10 行，最终还是通过调用 `type` 来创建出我们的新类并返回给调用者。后面我们会看到其他不用 `type` 方式来返回类对象的方法。
- 第 14 行，与 `type` 用法一样，这里我们通过自定义的 Metaclass 来创建类，并为该类设定了 `foo` 属性。
- 第 18 行，能够正确访问类中的 `FOO` 属性，说明属性名已经被转换成大写形式了。

这是一个没有什么意义的例子，但是通过这个例子，可让让我们对元类有一个基本的理解。

#### 2.类作为元类

虽然可以将函数作为元类来创建类，但创建一个类作为元类来使用，这将更符合 OOP 思想，并且有更多的灵活性。需要注意的是，当使用类作为元类时，必须注意以下两点：
</br>

1. 类的最顶层必须继承自 type：虽然是元类，但它同时还是一个类，这就说明作为元类的类也可以继承，但就像是 `object` 类是所有类的最顶级父类一样，`type` 必须是元类的最顶级元类。
2. 按要求实现 `__new__` 方法：`__new__` 方法体内是用来实现真正创建类的代码块的，该方法除了第一个参数是类本身之外，同样还需额外的其他三个参数：`name`, `bases` 以及 `attrs` 来创建类。

现在让我们通过类作为元类来实现上面的例子，将类中所有的用户自定义属性的名字转换成大写：

{{< highlight python "linenos=table,hl_lines=1 4 11-15 17 18,linenostart=1" >}}
class UpperAttr(type):
    __uppercase_attr = {}

    def __new__(cls, future_class_name, future_class_parents, future_class_attr):
        for name, val in future_class_attr.items():
            if not name.startswith('__'):
                cls.__uppercase_attr[name.upper()] = val
            else:
                cls.__uppercase_attr[name] = val
        # 通过调用 super 返回类
        return super(UpperAttr, cls).__new__(
            cls,
            future_class_name,
            future_class_parents,cls.__uppercase_attr
        )

MyClass = UpperAttr('MyClass', (), {'foo':'bar'})
print(MyClass.FOO) #  bar
{{< / highlight >}}

</br>
代码解释：
</br>

- 第 1 行，创建一个继承自 `type` 的类，元类的最终父类必须要继承自 `type`。
- 第 2 行，定义私有类变量，用于保存属性名转换为大写之后的所有属性
- 第 4 行，实现了 `__new__` 方法，它一共接收 4 个参数：由 Python 自动传递类自身参数 `cls`，以及其他三个用来创建类的参数，该方法最终必须返回一个类对象。
- 第 10-15 行，这里使用 `super` 方法，而不是直接调用 `type`，虽然 Python 最终还是通过调用 `type` 来生成类的，但这种写法更加符合 OOP 编程思想，也更加灵活，比如下面将会看到的，自动调用 `__init__` 方法等。
- 第 17 行，使用元类 `UpperAttr` 来创建类我们的类，其调用方法与调用函数元类和 `type` 类似。
- 第 18 行，访问 `MyClass` 类中的 `FOO` 属性。

##### 元类中的 **`__init__`** 和 **`__call__`**

通过类实现的元类，本身又是一个类，因此类中的其他魔术方法，同样可以应用在我们的这个元类中，下面让我们看一下两个常用的魔术方法在元类中的应用：
</br>

**`__init`__**：与正常类中的使用方式一样，如果在元类中定义了该方法，当 `__new__` 返回后，会自动调用该方法。
</br>

**`__call__`**：若在元类中定义了 `__call__` 方法，那么该方法会在被创建的类 **被实例化** 时自动调用，我们通常将它应用到单例模式的创建中去，考虑如下实例：

{{< highlight python "linenos=table,hl_lines=1 6 10 16 19 20,linenostart=1" >}}
class MetaSingleton(type):
    # 类属性，用来保存实例对象
    # 设置为类私有属性，防止被意外修改
    __instance = None

    def __call__(cls, *args, **kvargs):
        # 如果类属性 __instance 不为空，说明已经实例化过某个类，直接返回那个类实例即可
        # 如果为 None，则创建一个新的实例对象，并保存到 __instance 变量中
        if cls.__instance is None:
            cls.__instance = super(MetaSingleton, cls).__call__(*args, **kvargs)

        # 总是返回类属性 __instance
        return cls.__instance

#  通过 MetaSingleton 元类创建类
SingletonKls = MetaSingleton('SingletonKls', (), {})

#  创建类实例
my_obj1 = SingletonKls()
my_obj2 = SingletonKls()

#  打印出实例 ID， 两次返回值一样
print(id(my_obj1))
print(id(my_obj2))
{{< / highlight >}}

</br>
代码解释：
</br>

- 第 1 行：定义元类 `MetaSingleton`，并继承自 `type`。
- 第 6 行：定义 `__call__` 方法，该方法会在实例化类时被调用。
- 第 10 行：如果类属性 `__instance` 为 None，才创建新的类实例，否则返回之前已经创建过的类实例。
- 第 16 行：通过元类 `MetaSingleton` 创建我们的类。
- 第 19 行：由于实例是第一次被实例化，调用第 10 行创建新的实例，并将实例保存在了元类中的 `__instance` 属性中。
- 第 20 行：由于此时元类的类属性 `__instance` 已经保存了刚刚生成的实例对象，所以直接将上次创建的实例返回回来。

---

### 正确使用元类的姿势

虽然我们可以使用 `kls = Metaclass(name, bases, attrs)` 的方式使用元类来生成我们的类，但这种方式不仅丑陋难用，而且非常不符合 OOP 标准，正确的使用方式是：在我们使用 `class` 关键字定义类时，明确指定我们要使用的 Metaclass。
</br>

在 Python2 和 Python3 中，指定 Metaclass 的方式是不同的，让我们分别看一下如何在两个版本中分别使用 Metaclass。
#### Python2
在 Python2 中，通过在类中设定 `__metaclass__` 属性来指定我们要使用的元类，如：

{{< highlight python "linenos=table,linenostart=1" >}}
class MyClass(object):
    __metaclass__ = MetaSingleton
{{< / highlight >}}

#### Python3

在 Python3 中，声明 Metaclass 是在类名后面的括号中，通过关键字 `metaclass` 来指定的：
{{< highlight python "linenos=table,linenostart=1" >}}
class MyClass(metaclass=MetaSingleton): pass
{{< / highlight >}}

如果类同时还继承自其他类，则 `metaclass` 放在继承类的后面，并用逗号 `,` 分隔，如：
{{< highlight python "linenos=table,linenostart=1" >}}
class MyClass(ParentClass, metaclass=MetaSingleton):
    pass
{{< / highlight >}}

{{<admonition title="tip" type="tip">}}
Python2 与 Python3 中的声明语法是不同的，并且互不兼容，如果想编写跨平台的代码，可以引用第三方 Pyhton 库 [six](https://pypi.python.org/pypi/six)
{{</admonition>}}

### 元类的继承性

当我们继承一个指明了元类的类，而自身并没有指明任何元类，会发生什么呢？

{{< highlight python "linenos=table,hl_lines=1 2,linenostart=1" >}}
class Animal(metaclass=MetaSingleton): pass
class Dog(Animal): pass

# 实例化两个 Dog 类
dog1 = Dog()
dog2 = Dog()

print(id(dog1)) #  4370179968
print(id(dog2)) #  4370179968
{{< / highlight >}}
这是一个不太恰当的例子，但是足以说明问题了：
</br>

- 第 1 行，首先我们创建了一个 Animal 的类，并为该类指定了我们的元类 MetaSingleton。
- 第 2 行，声明一个 Dog 类，继承自 Animal 类。
- 实例化两个 Dog 类，最终打印出这两个实例的 ID

从结果中可以看出，他们是同一个实例对象，虽然 Dog 并没有指明元类，但是由于它的父类 `Animal` 指明了 `MetaSingleton` 元类，对于子类 `Dog` 来说，该属性被继承了下来，也就是说，此时 `Dog` 的元类也是 `MetaSingleton`。

{{<admonition title="tip" type="tip">}}
在定义类时，每个类只能声明一次 metaclass，而无论 metaclass 是在父类中声明的，还是在自身类定义时声明的，否则 Python 解释器会抛出 `TypeError` 异常，提示 metaclass 冲突错误。
{{</admonition>}}

### Metaclass 是如何工作的？

当我们通过直接调用元类的方式创建类时，意图很明确，我们将所有创建类所需要的数据通过参数的方式传递给元类。而通过 `class` 方式声明的类，Python 有时如何解释的呢？
</br>

当 Python 解释器遇到 `class` 关键字时，首先扫描类的内部定义，包括类变量和内部定义的所有方法，并将扫描的信息保存到 `__dict__` 字典中，此刻，在内存中，类还没有被创建；解释器接着会查看类的定义中是否声明了 metaclass，如果存在 metaclass 的声明，则调用我们声明的 metaclass ，并将类名、父类以及 `__dict__` 传递给它来创建类，否则将这些信息传递给 `type` 来创建类，并最终保将类保存到内存中。

## 结束语

通过 Metaclass 能够实现的大部分功能，其实通过其他方法一般也可以实现。何时需要使用 Metaclass，需要视具体情况而定，为了代码的可读性和维护性，在非必要的情况下，能避免使用 Metaclass 则尽量避免使用。

</br>
[参考: stack overflow 中的神级回答](https://stackoverflow.com/a/6581949/2101728)