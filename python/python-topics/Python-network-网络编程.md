# Python 网络编程

阅读《Python 网络编程》中，不过进度有点慢，于是在网上找了两份简要的教程，下面做简单纪要。

一份是菜鸟教程的 Python [网络编程](https://www.runoob.com/python/python-socket.html) 部分，还有廖雪峰的 Python 教程 [网络部分](https://www.liaoxuefeng.com/wiki/1016959663602400/1017787560490144)。

另外，非常推荐这个教程 [Python 中的 Socket 编程](https://keelii.gitbooks.io/socket-programming-in-python-cn/content/)，其中第四部分讲了网络的检测，思路都是比较宏观的，所以其实阅读起来有一定的难度。

## socket() 函数

```python
socket.socket([family[, type[, proto]]])
```

* family: 套接字家族可以使 AF_UNIX 或者 AF_INET。
* type: 套接字类型可以根据是面向连接的还是非连接分为 `SOCK_STREAM` 或 `SOCK_DGRAM`。
* protocol: 一般不填默认为 0。

## Socket 对象方法

菜鸟教程中介绍了一些 Socket 对象的方法，分类如下

* 服务器端套接字
    * `s.bind()` 绑定地址 (host, port) 到套接字，在 AF_INET 下，以元组形式表示地址。
    * `s.listen()` 开始 TCP 监听。backlog 指定在拒绝连接之前，操作系统可以挂起的最大连接数量。一般设定可为 5。
    * `s.accept()` 被动 TCP 客户端连接，（阻塞式）等待连接的到来。
* 客户端套接字
    * `s.connect()` 主动初始化 TCP 连接，如果连接出错返回 socket.err 错误【当然在 UDP 连接中 client 也可以用 connect 绑定服务器 socketname，进而使用 send 和 recv 函数】
    * `s.connect_ex()` connect() 函数的拓展，出错时返回错误码而非抛出异常
* 公共用途套接字函数
    * `s.recv()` 接受 TCP 数据，bufsize 指定要接受的最大数据量，flag 提供有关消息的其他信息，通常可忽略
    * `s.send()` 发送 TCP 数据，将 string 中的数据发送到连接的套接字，返回值是发送的字节数量，该数量可能小于 string 的字节大小
    * `s.sendall()` 完整发送 TCP 数据，失败则抛出异常
    * `s.recvfrom()` 接收 UDP 数据
    * `s.sendto()`发送 UDP 数据
    * `s.close()`
    * `s.getpeername()` 返回连接套接字的远程地址
    * `s.getsocketname()` 返回套接字自己的地址
    * `s.setsocketopt(level, optname, value)` 设置给套接字选项的值
    * `s.getsockopt(level, optname[.buflen])`
    * `s.settimeout(timeout)` timeout 单位为秒，值为 None 表明没有超时期
    * `s.gettimeout()`
    * `s.fileno()` 返回套接字的文件描述符
    * `s.setblocking(flag)` 如果 flag 为 0 则将套接字设置为非阻塞模式，否则设置为**阻塞模式（默认**）。非阻塞模式下，如果调用 recv() 没有发现任何数据，或 send() 调用无法立即发送数据，那么将引起 socket.error 异常。
    * `s.makefile()` 创建一个与该套接字相关联的文件

[这里](https://docs.python.org/zh-cn/3/library/socket.html#socket-objects) 是中文版的 API。
