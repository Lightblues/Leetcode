# Python

## Packages

### import

目前使用直接通过sys添加目录到搜索路径，然后绝对导入最方便；相对导入有很多局限不好搞。

```python
import sys
sys.path.append(path)   # 将目录或路径加入搜索路径
import package_name
```

- 关于绝对和相对导入参见 [Python：相对导入与绝对导入（import）、os.path、__file__](https://www.cnblogs.com/qi-yuan-008/p/12833189.html)
- [Python：__init__.py文件和、__all__、import、__name__、__doc__](https://www.cnblogs.com/qi-yuan-008/p/12827918.html)

### 文件处理

- Word | python-docx [python-docx处理word文档](https://zhuanlan.zhihu.com/p/61340025)

### debug

#### logging

```python
import logging

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.DEBUG
)
logging.basicConfig(level=logging.DEBUG,
 format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
```

### 多进程 multiprocessing

### 异步写入同一个文件

```python
from multiprocessing import Pool
def callback_writeout(x):
    with open('output_fn', 'a+') as f:
        for l in x:
            line = ','.join(l) + "\n"
            f.write(line)
pool = Pool(processes=process_num)
for i in range(process_num):
    pool.apply_async(
        mine_paris_from_ugc, 
        args=(ugc_fn, patterns, i*limit, limit, 100),
        callback=callback_writeout      # 异步写入
    )
pool.close()
pool.join()
```

### Network 网络编程

阅读《Python 网络编程》中，不过进度有点慢，于是在网上找了两份简要的教程，下面做简单纪要。

一份是菜鸟教程的 Python [网络编程](https://www.runoob.com/python/python-socket.html) 部分，还有廖雪峰的 Python 教程 [网络部分](https://www.liaoxuefeng.com/wiki/1016959663602400/1017787560490144)。

另外，非常推荐这个教程 [Python 中的 Socket 编程](https://keelii.gitbooks.io/socket-programming-in-python-cn/content/)，其中第四部分讲了网络的检测，思路都是比较宏观的，所以其实阅读起来有一定的难度。

### Spyder

- bf4
    - Docs <https://www.crummy.com/software/BeautifulSoup/bs4/doc/>
    - 实践 [爬虫实战-手把手教你爬豆瓣电影](https://www.douban.com/note/745693795/)

### GUI

#### TKinter

- 中文API [Tk图形用户界面(GUI)](https://docs.python.org/zh-cn/3/library/tk.html)

- [GeeksforGeeks](https://www.geeksforgeeks.org/python-tkinter-tutorial/) 系列教程

初学参考了廖雪峰教程中的 [图形界面部分](https://www.liaoxuefeng.com/wiki/1016959663602400/1017786914566560) 和 [菜鸟教程](https://www.runoob.com/python/python-gui-tkinter.html)。比较简略

创建一个GUI程序

- 1、导入 Tkinter 模块
- 2、创建控件
- 3、指定这个控件的 master， 即这个控件属于哪一个
- 4、告诉 GM(geometry manager) 有一个控件产生了。

## 技巧

#### 字典2类属性

```python
d = {'a': 1, 'b': 2}
dc = type('allMyFiled', (object,), d)
d.a  # 可以直接用属性来使用了！
```

## Tools

### VS Code

VSCode 的话，或许可参考 [配置基于VS Code的Python远程调试环境](https://zhuanlan.zhihu.com/p/43656542)

### Pycharm

#### 远程调试

简洁版 [https://zhuanlan.zhihu.com/p/38330654](https://zhuanlan.zhihu.com/p/38330654) 基本的用法都总结到了。

PyCharm 远程调试：主要参考 [Pycharm远程调试服务器代码](https://cloud.tencent.com/developer/article/1574909)；另外，还可参看 [Python远程调试图文教程（一）之Pycharm Remote Debug](https://juejin.cn/post/6844903612942909453)。

纪要：[Pycharm 配置remote 进行tensorflow远程开发调试](https://www.shangmayuan.com/a/7b6b55e9fe654f1d8950144d.html) 摘录部分：

##### 文件同步配置

- 打开面板 `Tools -> Deployment -> Configuration`

- 点击 `+` 号新建一个配置，输入配置名 `Name`，随便起，`Type` 选择 `SFTP`，而后点击确认。

- 配置服务器的 IP和端口，验证方式能够选择用户名和密码或者是使用私钥文件，putty的.ppk也支持

- 配置根目录，`Root Path` 是项目文件在远程服务器中的根目录，根据需求配置，例如 `/home/zhangsan/workplace`

- 路径映射 `Mappings`， `Local Path` 设置为 Windows 下的工程目录， `Deployment path on server` 设置为远程服务器的目录，根据本身的须要设置

- `Excluded Paths` 设置不须要同步的目录，如配置文件，数据集，checkpoint等。

- `Tools -> Deployment -> Options`，将 `Create Empty directories` 打上勾，要是指定的文件夹不存在，会自动建立。

##### 设置远程的python解释器

- 菜单栏 `File -> Settings`，进入设置面板后选择 `Project -> Project Interpreter`，而后在右边，点击那个小齿轮进行设置。

- 点击 `Add Remote`，选择 `SSH Credentials`，`Python interpreter path` 选择本身须要的远程服务器的解释器。

- 在运行程序的时候，配置 `Run` 的时候选择刚刚配置的解释器就能远程调试了，跟使用本地解释器相似，可是还须要设置环境变量。

- `Run -> Edit Configurations`
