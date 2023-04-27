# Python 文件之间共享变量

参见 Stack Overflow 上的 <https://stackoverflow.com/questions/13034496/using-global-variables-between-files>

## 将共享数据保存在特定的文件中

这里给出的一个方案是新建一个名为 `settings.py` 的文件，将 global 变量存放其中。

注意，这里定义了一个 init() 方法显式地初始化了变量（当然也可以直接使用，或者新建一个 class 等，形式不一而足，但取得的效果时一样的，但似乎下面这样写比较规范）。

```python
# settings.py

def init():
    global myList
    myList = []
```

下面展示了用不同的文件调用 myList 的形式。

```python
# subfile.py

import settings

def stuff():
    settings.myList.append('hey')
    
# main.py

import settings
import subfile

settings.init()          # Call only once
subfile.stuff()         # Do stuff with global var
print settings.myList[0] # Check the result
```
