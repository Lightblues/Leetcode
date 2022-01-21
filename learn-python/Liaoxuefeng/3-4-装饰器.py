
import functools

# 装饰器
flag = 0
if flag:
    def log(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print('call wrapped function {}():'.format(func.__name__))
            return func(*args, **kw)
        return wrapper

    # 正常的方式，随便的函数都可以，可以带参数
    @log
    def now(a):
        print('2020-8-30', a)
    now(12)                     # 相较于下面的不太「优雅」的方式，这里直接用了 Decorator 的方式进行定义
    # 可以等价于这样
    def now(a):
        print('2020-8-30', a)
    now = log(now)              # 注意这里和下面一行，两层的函数调用，log 接受一个函数对象 now 作为参数，返回的「函数」仅仅是 now 的一个「别名」
    now(12)                     # 因此可以利用这个「别名」调用之前定义好的 now 函数


# 若果装饰函数也需要传入参数，则需要三层嵌套的 decorator
flag = 0
if flag:
    def log(text):                          # 这一层用于接收 Decorator 的参数
        def decorator(func):                # 这一层用于接收所需要装饰的函数 func
            @functools.wraps(func)          # 这里完成了 wrapper.__name__ = func.__name__ 这样的一行操作
            def wrapper(*args, **kw):       # 这一层是核心，直接调用了 func 达到「装饰」的目的，但注意到整体返回的是 wrapper 函数并没有执行
                print("{} {}:".format(text, func.__name__))
                # wrapper.__name__ = func.__name__
                return func(*args, **kw)
            return wrapper
        return decorator

    @log('execute')
    def hello(name):
        print('Hello', name)
    hello("Kate")
    print(hello.__name__)

    def hello(name):
        print('Hello', name)
    hello = log('execute')(hello)       # 和上面的两层嵌套对比，注意这里「调用」了三次，而其实三次 return 的结果指向的都是同一个函数
    hello('Kate')
    print(hello.__name__)


# 一个练习：请设计一个decorator，它可作用于任何函数上，并打印该函数的执行时间：
flag = 0
if flag:
    import time, functools
    def metric(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kw):
            t_start = time.time()
            result = fn(*args, **kw)
            print("Running time: {}".format(time.time() - t_start))
            return result                   # 注意不要被上面的示例局限了，在 wrapper 的调用中事实上已经执行了被装饰的函数 fn
        return wrapper                      # 事实上调用 metric(fn) 或者用 @metric 表达式，返回的都是 wrapper，并没有进行调用

    # 测试
    @metric
    def fast(x, y):
        time.sleep(0.0012)
        return x + y;
    @metric
    def slow(x, y, z):
        time.sleep(0.1234)
        return x * y * z;
    f = fast(11, 22)                # 这里执行了函数
    s = slow(11, 22, 33)
    if f != 33:
        print('测试失败!')
    elif s != 7986:
        print('测试失败!')


# 偏函数 ############################
"""
当函数的参数个数太多，需要简化时，使用functools.partial可以创建一个新的函数，这个新函数可以固定住原函数的部分参数，从而在调用时更简单。
"""
flag = 0
if flag:
    # 一个例子：int 函数可以设定一个参数值 base 对不同基的数字进行转换
    def int2(x, base=2):
        return int(x, base=base)
    print(int2('1000000'), int2('1010101'))     # 这样就不用重复调用 int(x, base=2) 了

    import functools
    int2 = functools.partial(int, base=2)

    # 注意，不仅仅可以接收命名参数，也可以接收 *args, **kw 。例如
    max2 = functools.partial(max, 10)       # 就相当于
    print(max2(5, 6, 7))                    # 相当于 max(10, 5, 6, 7)



