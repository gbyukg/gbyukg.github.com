---
title: "Vim"
date: 2019-04-05T15:46:31+08:00
type: cheatsheet
categories:
  - cheatsheet
---

## VIM

### Motion

| Key Bindings | Descriptions
| ---          | ---                                                          |
| `0`          | Moves cursor to the start of the line
| `$`          | Moves cursor to the end of the line (inclusive of newline)
| `g_`         | Moves cursor to the end of the line (exclusive of newline)
| `b`          | Moves cursor backward through each word
| `e`          | Moves cursor to the end of the word
| `w`          | Moves cursor to the start of the next word
| `gg`         | Moves cursor to the start of the buffer
| `G`          | Moves cursor to the end of the buffer
| `%`          | Moves cursor to the next bracket (or parenthesis)
| `(`          | Moves cursor to the previous sentence
| `)`          | Moves cursor to the next sentence
| `{`          | Moves cursor to the start of a paragraph
| `}`          | Moves cursor to the end of a paragraph
| `[(`         | Moves cursor to previous available parenthesis
| `])`         | Moves cursor to next available parenthesis
| `[{`         | Moves cursor to previous available bracket
| `]}`         | Moves cursor to next available bracket
| `Ctrl-f`     | Normal	Smart page forward (Ctrl-f / Ctrl-d)
| `Ctrl-b`     | Normal	Smart page backwards (C-b / C-u)
| `Ctrl-e`     | Normal	Smart scroll down (3 Ctrl-e/j)
| `Ctrl-y`     | Normal	Smart scroll up (3Ctrl-y/k)
| `Ctrl-q`     | Normal	Ctrl-w
| `SPC j w`    | jump to a word in the current buffer (easymotion)
| `SPC j l`    | jump to a line with avy (easymotion)
| `SPC j j`    | jump to a character in the buffer (easymotion)
| `SPC j J`    | jump to a suite of two characters in the buffer (easymotion)


### Operators

| Key Bindings | Descriptions
| ---          | ---                                                               |
| `i`          | Puts you into INSERT mode before the current cursor position
| `I`          | Puts you into INSERT module at the beginning of the line
| `a`          | Puts you into INSERT mode after the current cursor position
| `A`          | Puts you into INSERT mode at the end of the line
| `o`          | Moves cursor to the next line and enters INSERT mode
| `O`          | Moves cursor to the previous line and enters INSERT mode
| `x`          | Cuts the character (or the selection of characters)
| `X`          | Cuts the previous character
| `s`          | Substitutes the character (or the selection of characters)
| `S`          | Substitutes the entire line
| `yy`         | Yanks (i.e., copies) the entire line
| `p`          | Pastes content after the current cursor position
| `P`          | Pastes content before the current cursor position
| `u`          | Undoes the last edit
| `~`          | Swaps character casing (e.g., converts a to A)
| `.`          | Repeats the last INSERT edit
| `dd`         | Deletes the current line
| `D`          | Deletes from the cursor until the end of the line (same as d$)
| `, <Space>`  | 移除所有行后的空白格
| `Ctrl-r`     | 替换选定的文字
| `*`          | 向前搜索当前光标下的单词
| `#`          | 向后搜索当前光标下的单词
| `f`          | Finds specified character to the right of current cursor position
| `F`          | Finds specified character to the left of current cursor position
| `;`          | repeat f/F
| `t`          | Same as f but searches until the specified character
| `T`          | Same as F but searched until the specified character
| `gf`         | open the file under your cusor in the same window
| `[ SPC`      | Insert space above
| `] SPC`      | Insert space below
| `[ e`        | Move line up
| `] e`        | Move line down
| `c s '`      |
| `c s t`      | to go full circle
| `d s '`      | remove the delimiters entirely
| `c s w`      |
| `g u w`      |
| `g U w`      |

### Windows

`SPC w`：窗口管理

```
[options]
    windows_leader = "s"
```

快捷键              | 功能描述
 :--                | :--
`WIN v`             | 水平分屏
`WIN V`             | 水平分屏，并编辑上一个文件
`SPC w s / SPC w -` | horizontal split
`SPC w S`           | horizontal split and focus new window
`WIN g`             | 垂直分屏
`WIN G`             | 垂直分屏，并编辑上一个文件
`SPC w v / SPC w /` | vertical split
`SPC w V`           | vertical split and focus new window
`<Tab>`             | 跳至下一个窗口
`Shift-<Tab>`       | 跳至上一个窗口
`SPC w W`           | 标记窗口并根据标记选择指定的窗口
`SPC 1~9`           | 跳转到指定序列号的窗口
`g`                 | 智能关闭当前窗口
`WIN o`             | 关闭其他窗口
`SPC w D`           | 标记窗口并删除指定标记的窗口
`SPC w =`           | 重置窗口大小
`WIN t`             | 新建新的标签页
`WIN c`             | 清除所有其余 buffer


### Buffers


| `<C-w>f` | open the file under your cusor in a new window
| `<C-w>gf` | open the file under your cusor in a new tab

| `gx` | Opens the URL under your cursor in a web browser


| `[ l` | Go to the previous error
| `] l` | Go to the next error

## Layers

### Edit Layers

#### [tpope/vim-surround](https://github.com/tpope/vim-surround)
``` sh
"Hello world!"

【cs'"】 将双引号替换成单引号
'Hello world!'

【cs'<p>】 将单引号替换成 <p>与</p>
<p>Hello world</p>

【cst"】将标签替换成 "
"Hello world!"

【ds"】删除双引号
Hello world!

【ysiw]】iw 为文本对象
[Hello] world!

【ys3iw】
```

#### [junegunn/vim-emoji](https://github.com/junegunn/vim-emoji)
为 VIM 提供表情符号。

#### [terryma/vim-expand-region](https://github.com/terryma/vim-expand-region)
选择模式下方便增加或减少选择的范围，可根据语言不同选择不同的策略。

#### [kana/vim-textobj-user](https://github.com/kana/vim-textobj-user)
自定义文本对象，通过自定义快捷键来快速选择区域文本。
[扩展插件列表](https://github.com/kana/vim-textobj-user/wiki)

##### [bps/vim-textobj-python](https://github.com/bps/vim-textobj-python)
基于 vim-textobj-user 插件为 Python 创建的自定义选择文本区域快捷键，如 `vif` 选择当前光标所在方法的方法体，`dif` 删除当前光标所在的方法体。

- `af`：快速选择光标所在方法的整个方法定义。
- `if`：快速选择光标所在方法的方法体区域。
- `ac`：快速选择光标所在类的整个类定义。
- `ic`：快速选择光标所在类的类体部分。

##### [whatyouhide/vim-textobj-xmlattr](https://github.com/whatyouhide/vim-textobj-xmlattr)
为 HTML 文件提供自定义文本对象。

- `ax`：HTML 标签的属性，包括属性名前的空格。
- `ix`：HTML 标签的属性，不包括属性名前的空格。

##### [idbrii/textobj-word-column.vim](https://github.com/idbrii/textobj-word-column.vim/)
快速选择相同列的文本段。

- `ic`：所有与当前鼠标下单词所在相同列的所有单词，计算列时不包括单词结尾的空格。
- `ac`：所有与当前鼠标下单词所在相同列的所有单词，计算列时包括单词结尾的空格。

如：`vic` 选择当前列下的所有文字；`dic` 删除所有处在当前列下的所有文字；`cic` 删除所有处在当前列下的所有信息，并同时进入到输入模式，输入的内容对所有列都有效。

##### [mattn/vim-textobj-url](https://github.com/mattn/vim-textobj-url)

- `au`：选择 URL。
- `iu`：选择 URL，不包括多余的空格信息。

#### [vim-expand-region](https://github.com/kana/vim-textobj-indent/blob/master/doc/textobj-indent.txt)
相同缩进的段落

- `ai`：选择段落，包括使用空行分隔的段落。
- `ii`：选择段落，不包括使用空行分隔的段落。

#### [kana/vim-textobj-line](https://github.com/kana/vim-textobj-line)
- `al`：选择当前行，不包括行两边的空格。
- `il`：选择当前行，包括行两边的空格。

#### [kana/vim-textobj-entire](https://github.com/kana/vim-textobj-entire)
- `ae`：选择当前 buffer 所有文本信息。
- `ie`：选择当前 buffer 所有文本信息，但是不包括开头和结尾的空行。

#### [gcmt/wildfire.vim](https://github.com/gcmt/wildfire.vim)
`vi'` 快速选择单引号中的内容，`di(`：删除括号中的内容，`ci[`：删除中括号中的内容，并进入插入模式。
- `i'`
- `i"`
- `i(`
- `i[`
- `i{`
- `ip`
- `it`

#### [easymotion/vim-easymotion](https://github.com/easymotion/vim-easymotion)
#### [haya14busa/vim-easyoperator-line](https://github.com/haya14busa/vim-easyoperator-line)
在当前 buffer 中快速跳转。
- `SPAC j w`：快速跳转到当前 buffer 标记点。
- `SPAC j j`：输入要跳转处的首字母后，根据当前 buffer 中的标记跳转到指定位置处。
- `SPAC j J`：输入要跳转处的前两个字母后，根据当前 buffer 中的标记跳转到指定位置处。
- `SPAC j l`：快速跳转到指定行。
- `SPAC j u`：快速跳转到某个 URL 处。

> 快捷键定义在 core layer 中。

#### [editorconfig/editorconfig-vim](https://github.com/editorconfig/editorconfig-vim)

[EditorConfig](https://editorconfig.org/) 的 VIM 插件。可将默认配置文件放到 `~/.editorconfig` 中。

使用 editorconfig 的[项目列表](https://github.com/editorconfig/editorconfig/wiki/Projects-Using-EditorConfig)

#### [godlygeek/tabular](https://github.com/godlygeek/tabular)
文本快速对齐，使用 `:Tabularize /` 后跟要对齐的字符，如 `Tabularize /=` 对 `=`
 进行对齐。
 
- `Tabularize /|`：对 | 进行对齐。

SpaceVim 快捷键

- `SPAC x a &`
- `SPAC x a (`
- `SPAC x a )`
- `SPAC x a [`
- `SPAC x a ]`
- `SPAC x a {`
- `SPAC x a }`
- `SPAC x a ,`
- `SPAC x a .`
- `SPAC x a :`
- `SPAC x a ;`
- `SPAC x a =`
- `SPAC x a |`
- `SPAC x a o`
- `SPAC x a [SPC]`
- `SPAC x a <Bar>`

#### [ntpeters/vim-better-whitespace](https://github.com/ntpeters/vim-better-whitespace)

高亮行未空白符或是空行。

- `ToggleWhitespace`：
- `EnableWhitespace`：
- `DisableWhitespace`：

#### SpaceVim
- `SPC x d w`：删除所有行尾空白符（包括空行中的空白符）。

#### [lilydjwg/fcitx.vim](https://github.com/lilydjwg/fcitx.vim)
[Fcitx](https://fcitx-im.org/wiki/Fcitx/zh-hans) 输入法插件。在不同模式中切换时，自动恢复在各个模式中输入法的状态，避免来回切换中英文输入法。

### Ctrl

快捷键         | 功能描述
:--            | :--
`SPC p f`      | 在当前文件所在的项目项目目录下查找文件
`SPC f f`      | 在当前文件所在的目录下查找文件
`<Leader> f e` | 模糊搜索寄存器
`<Leader> f h` | 模糊搜索 history/yank
`<Leader> f j` | 模糊搜索 jump, change
`<Leader> f l` | 模糊搜索 location list
`<Leader> f m` | 模糊搜索 output messages
`<Leader> f o` | 模糊搜索函数列表
`<Leader> f q` | 模糊搜索 quickfix list
`<Leader> f r` | 重置上次搜索窗口

#### Ctrl 搜索窗口快捷键

快捷键                 | 功能描述
:--                    | :--
`<Tab> / Ctrl-j`       | 选择上一行
`Shift-<Tab> / Ctrl-k` | 选择下一行
`Ctrl-s`               | Open in a split
`Ctrl-v`               | Open in a vertical split
`Ctrl-t`               | Open in a new tab
`Ctrl-g`               | Exit unite

### Tools
快捷键            | 功能描述
:--               | :--
`:SourceCounter`  | 在 VIM 中展示代码统计。[wsdjeg/SourceCounter.vim](https://github.com/wsdjeg/SourceCounter.vim)
`<F7>`            | 打开/关闭文件编辑历史树。[simnalamburt/vim-mundo](https://github.com/simnalamburt/vim-mundo)
`:Cheat`          | 查阅工具表
`:Calc`           | 打开数学计算窗口。
`:Calendar`       | 打开日历窗口，`?` 查看帮助文档 [itchyny/calendar.vim](https://github.com/itchyny/calendar.vim)]
`:FencAutoDetect` | 若 VIM 没有使用正确的编码打开文件，该命令将尝试使用适当的编码格式来打开文件。[mbbill/fencview](https://github.com/mbbill/fencview)
`:Limelight`      | 高亮当前光标所在的自然段。
