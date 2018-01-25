---
title: "Lamp"
date: 2018-01-24T16:23:44+08:00
tags:
  - 
categories:
  - 
draft: true
---

## Title

{{<admonition type="warning">}}

Warning message

{{</admonition>}}
<!--more-->

### subtitle

[Google](https://www.google.com)

- [ ] 1
- [x] 2
- [ ] 3

5/12

> dfa gdas gds g

有两类动态伪类：链接 和用户行为。链接就是:link 和:visited，而用户行为包括:hover、:active 和:focus</br>
在本文中提到的css选择器中，这几个应该是最常用到的。

`:link` 伪类用于链接尚未被用户访问的时候，而:visited 伪类用于用户访问过的链接，也就是说它们是相反的。  

`:hover` 伪类用于用户移动他们的鼠标在元素上，而尚未触发或点击它的时候。:active伪类应用于用户点击元素的情况。最后，:focus伪类用于元素成为焦点的时候——最常用于表单元素。

你可以在你的样式表中使用多种用户行为动态伪类，这样你就可以，比如，根据用户的鼠标只是滑过或悬停的时候，为一个输入框定义不同的背景色:

   Name | Age
--------|------
    Bob | 27
  Alice | 23

Cat
: Fluffy animal everyone likes
: Fluffy animal everyone likes

Internet
: Vector of transmission for pictures of cats

This is a footnote.[^1]

[^1]: the footnote text.

``` sh
cd /
pwd

function test()
{
    echo 'function test'
}

```

{{< highlight bash "linenos=table,hl_lines=1 5-7, linenostart=1" >}}

cd /
pwd

function test()
{
    echo 'function test'
}

{{< / highlight >}}

```html
<section id="main">
  <div>
    <h1 id="title">{{ .Title }}</h1>
    {{ range .Data.Pages }}
      {{ .Render "summary"}}
    {{ end }}
  </div>
</section>
```
