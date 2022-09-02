# Python GUI 编程（tkinter）

【资源】

- 中文API [Tk图形用户界面(GUI)](https://docs.python.org/zh-cn/3/library/tk.html)
- [GeeksforGeeks](https://www.geeksforgeeks.org/python-tkinter-tutorial/) 系列教程
- 简明教程 [Python GUI之tkinter窗口视窗教程大集合（看这篇就够了）](https://www.cnblogs.com/shwee/p/9427975.html)

初学参考了廖雪峰教程中的 [图形界面部分](https://www.liaoxuefeng.com/wiki/1016959663602400/1017786914566560) 和 [菜鸟教程](https://www.runoob.com/python/python-gui-tkinter.html)。比较简略

创建一个GUI程序

- 1、导入 Tkinter 模块
- 2、创建控件
- 3、指定这个控件的 master， 即这个控件属于哪一个
- 4、告诉 GM(geometry manager) 有一个控件产生了。

一个例子如下

```python
from tkinter import *
root=Tk()
a = Label(root, text="Hello, world!")
a.pack()
root.mainloop()
```

导入之后，创建 Tk 的一个实例，Label 是显示文字的 Wedge，**第一个参数用来指定父节点**，使用 a.pack() 方法将其显示到屏幕上；最后用 root.mainloop() 方法显示 Tk 实例。

另一个例子，这里创建了 Frame 的一个继承类 Application

```python
from tkinter import *
from tkinter import messagebox

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.helloLabel = Label(self, text='Hello, world!')
        self.helloLabel.pack()
        self.nameInput = Entry(self)
        self.nameInput.pack()
        self.alertButton = Button(self, text='Hello', command=self.hello)
        self.alertButton.pack()
        self.quitButton = Button(self, text='Quit', command=self.quit)
        self.quitButton.pack()

    def hello(self):
        name = self.nameInput.get() or 'world'
        messagebox.showinfo('Message', 'Hello, {}'.format(name))

app = Application()
app.master.title('Hello world')
app.mainloop()
```

从`Frame`派生一个`Application`类，这是所有Widget的父容器。
在GUI中，每个Button、Label、输入框等，都是一个Widget。Frame则是可以容纳其他Widget的Widget，所有的Widget组合起来就是一棵树。
`pack()`方法把Widget加入到父容器中，并实现布局。`pack()`是最简单的布局，`grid()`可以实现更复杂的布局。
最后实例化Application，并启动消息循环。

## 功能实现

### 关闭窗口时的操作

参见 <https://stackoverflow.com/questions/111155/how-do-i-handle-the-window-close-event-in-tkinter>，在窗口上配置 `root.protocol("WM_DELETE_WINDOW", on_closing)` ，其中第二个参数是函数。

```python
import tkinter as tk
from tkinter import messagebox

root = tk.Tk()

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
```

### 简单输入 askinteger，askfloat，askstring （子模块 simpledialog.py）

参见 [askinteger，askfloat，askstring的使用](https://www.pynote.net/archives/990)

```python
from tkinter.simpledialog import askinteger,askfloat,askstring
askinteger('askinteger','please give me an integer:', 
                initialvalue=12345, minvalue=100, maxvalue=20000)
```

### 下拉菜单 OptionMenu

[如何在 Tkinter 中创建下拉菜单](https://www.delftstack.com/zh/howto/python-tkinter/how-to-create-dropdown-menu-in-tkinter/)

### 布局 pack grid place

参见 [Tkinter 教程 - 布局管理](https://www.delftstack.com/zh/tutorial/tkinter-tutorial/tkinter-geometry-managers/)，感觉 pack 和 grid 简单实用即可。
