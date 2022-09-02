# Python 保存控制台输出到文件（重定向）

参考 [python将控制台输出保存到文件](https://www.jianshu.com/p/9c5c9d36eb31)。给出了几种方案

另外，关于关于 Python 的 IO，[参考 Python IO - 输出重定向](https://edenxio.github.io/2018/12/12/Python%20IO%20-%20%E8%BE%93%E5%87%BA%E9%87%8D%E5%AE%9A%E5%90%91/)

## 直接在控制台重定向

```bash
python myprint.py > myprint.txt #将控制台输出覆盖写入到文件
myprint.py >> myprint.txt #将控制台输出追加写入到文件python
```

## 利用print函数中的file参数

```python
import sys
import time
f=open("myprint.txt","w+")
for i in range(100):
   print("--{}--".format(i**2),file=f, flush=True)
   print("--{}--".format(i ** 2),file=sys.stdout)
   time.sleep(0.5)
```

`print`函数中的`file`参数，`file=f`，输出到文件；`file=sys.stdout`，输出到终端；`flush=True`，即时刷新

## 将sys.stdout输出到文件

若只需要输出到文件，则可直接重定向输出到文件

```python
import sys
f=open("print.txt","w+")
sys.stdout=f
for i in range(1000):
    print(i*9)
```

若需要同时输出到文件和控制台，则可像下面一样实现一个类

```python
import sys
class Logger(object):
    def __init__(self, filename='default.log', stream=sys.stdout):
        self.terminal = stream
        self.log = open(filename, 'a')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass

sys.stdout = Logger(stream=sys.stdout)

# now it works
print('print something')
```

## logging模块重定向

> 对于代码量较大的工程，建议使用logging模块进行输出。该模块是线程安全的，可将日志信息输出到控制台、写入文件、使用TCP/UDP协议发送到网络等等。
>
> 默认情况下logging模块将日志输出到控制台(标准出错)，且只显示大于或等于设置的日志级别的日志。日志级别由高到低为CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET，默认级别为WARNING。

参考 <https://www.cnblogs.com/clover-toeic/p/5491073.html>
