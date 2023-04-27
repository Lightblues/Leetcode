# Python 教程-廖雪峰

## Python 基础

## 函数

- 调用函数
- 定义函数
- 函数的参数
    - 默认参数
    - 可变参数 *args
    - 关键字参数 **kw
    - 命名关键字参数
- 递归函数

## 高级特性

- 切片
    - 例如间隔为 2 的切片可以是 [::2]
- 迭代
- 列表生成式
    - if 语法，实际上是过滤语法
    - 两层循环
    - if else 语法，前面的 else 不能省略
- 生成器 Generator
    - 可以被 next() 调用，最后抛出 StopIteration 错误，但一般都是 for 循环遍历
    - Yield 语法：generator function
- 迭代器 Iterator
    - 可以使用 for 循环的都叫做 Iterable，有集合数据类型和上面的生成器
    - 而可以被 next() 调用的都是 Iterator，生成器都是 Iterator 对象

## 面向对象高级编程

- 使用 **slots**
- 使用 @property
- 多重继承
- 定制类
    - 注意下面的这些都是类方法
    - **str**
        - **repr**
    - **iter**
        - **next**
    - **getitem**
        - **setitem**
        - **delitem**
    - **getattr**
    - **call**
        - 可以通过内置函数 callable() 检查是否可以调用
- 使用枚举类
- 使用元类

## 错误、调试和测试

- 错误处理
    - try...except...finally 结构
    - 错误类型，继承关系参见 [https://docs.python.org/3/library/exceptions.html#exception-hierarchy](https://docs.python.org/3/library/exceptions.html#exception-hierarchy)
- 测试
    - print 出来
    - assert 语法：断言
        - 参数 -O 来关闭 assert
    - logging
        - DEBUG, INFO, WARNING, ERROR 四种模式
        - 最好用的还是 logging
    - pdb
    - pdb.set_trace()
    - IDE
- 单元测试
- 文档测试

## 默认函数

- isinstance()
- iter()
    - 可以将 list 等转化为 Iterator

## 内建模块

- collections
    - Subtopic
- logging
