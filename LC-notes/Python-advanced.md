





- [pypy真的能让python比c还快？](https://juejin.cn/post/6961053856104972325) 介绍了 强/弱类型, 静态/动态语言 等的区别, 介绍了 PyPy 与 CPython 在性能上的差异, 几个代码测试实例很赞.
    - 参见 PyPy: <https://doc.pypy.org/en/latest/introduction.html>

## Python 解释器 (interpreter)

python是一门动态编程语言，由特定的解释器解释执行。下面是一些解释器实现:

- CPython 使用c语言实现的解释器
- PyPy 使用python语言的子集RPython实现的解释器，一般情况下PyPy比CPython快4.2倍
- Stackless Python 带有协程实现的解释器
- Jython Java实现的解释器
- IronPython .net实现的解释器
- Pyston 一个较新的实现，是CPython 3.8.8的一个分支，具有其他针对性能的优化。它针对大型现实应用程序（例如Web服务），无需进行开发工作即可提供高达30％的加速。
- ...

还有几个相关概念:

- IPython && Jupyter ipython是使用python构建的交互式shell, Jupyter是其web化的包装。
- Anaconda 是一个python虚拟环境，Python数据科学常用。
- mypyc 一个新的项目，将python编译成c代码库，以期提高python的运行效率。
- py文件和pyc文件 pyc文件是python编译后的字节码，也可以由python解释器执行。
- wheel文件和egg文件 都是项目版本发布的打包文件，wheel是最新标准。
- ...

### PyPy 为什么比 CPython 快?

主要原因是用了 [JIC](https://zh.wikipedia.org/wiki/%E5%8D%B3%E6%99%82%E7%B7%A8%E8%AD%AF), 也即由解释器在执行时 (而非编译器在程序执行之前) 进行编译再去执行.

具体而言, 进行了:

1. 标识代码中最常用的组件，例如循环中的函数。
2. 在运行时将这些零件转换为机器码。
3. 优化生成的机器码。
4. 用优化的机器码版本交换以前的实现。
