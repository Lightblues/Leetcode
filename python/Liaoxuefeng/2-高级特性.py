
# 自己实现 strip() 方法
flag = 0
if flag:
    # def trim(s):
    #     l = len(s)
    #     if l == 0:
    #         return ""
    #
    #     for i in range(l):
    #         if s[i] != ' ':
    #             start = i
    #             break
    #     for i in range(l-1, -1, -1):
    #         if s[i] != ' ':
    #             end = i
    #             break
    #     if start == l-1:
    #         return ''
    #     else:
    #         return s[start:end+1]

    # 找到了一个更简单的实现，利用了 Python 的 list/str 索引特性：允许「越界」的索引，还有如 [12,3][:0] 将返回 [] 空列表
    def trim(s):
        while s[:1]==' ':
            s=s[1:]
        while s[-1:]==' ':
            s=s[:-1]
        return s

    print(trim('  Hello   '))
    print(trim(''))
    print("    ")


# 迭代
flag = 0
if flag:
    from collections import Iterable
    print(isinstance('abc', Iterable)) # str是否可迭代
    print(isinstance(123, Iterable))

    def findMinAndMax(L):
        # if not isinstance(L, (list, tuple)):
        if len(L) == 0:
            return (None, None)
        _min = L[0]
        _max = L[0]
        for n in L:
            _min = min(_min, n)
            _max = max(_max, n)
        return (_min, _max)
    # print(findMinAndMax([]))
    # print(findMinAndMax([7]))
    # print(findMinAndMax([7, 1]))
    # print(findMinAndMax([7, 1, 3, 9, 5]))
    if findMinAndMax([]) != (None, None):
        print('测试失败!')
    elif findMinAndMax([7]) != (7, 7):
        print('测试失败!')
    elif findMinAndMax([7, 1]) != (1, 7):
        print('测试失败!')
    elif findMinAndMax([7, 1, 3, 9, 5]) != (1, 9):
        print('测试失败!')
    else:
        print('测试成功!')

# 列表解析式
flag = 0
if flag:
    # 注意，for 前面的 if 是正常的 if-else 而 for 后面的 if 实际上是晒筛选表达式
    something = [x if x % 2 == 0 else -x for x in range(1, 11) if x<8]
    print(something)

    # 例如，还可以加一个判断防止出错
    L1 = ['Hello', 'World', 18, 'Apple', None]
    L2 = [s.lower for s in L1 if isinstance(s, str)]

# 生成器 ######################################
# 这就是一个生成器
flag = 0
if flag:
    g = (x * x for x in range(10))
    g
    next(g)
    next(g)

    # def fib(max):
    #     n, a, b =  0, 0, 1
    #     while  n < max:
    #         print(b)
    #         a, b = b, a+b
    #         n += 1
    #     return 'done'
    # fib(5)

    # 修改为 generator
    def fib(max):
        n, a, b =  0, 0, 1
        while  n < max:
            yield b
            a, b = b, a+b
            n += 1
        return 'done'
    print([i for i in fib(6)])
    # 然而，用 for 循环调用 generator 时拿不到 return 的返回值——若要拿回必须捕获 StopIteration 错误
    g = fib(6)
    while True:
        try:
            x = next(g)
            print("g:", x)
        except StopIteration as e:
            print('Generator return value:', e.value)
            break

    # 利用生成器，杨辉三角 ###
    def triangles():
        L = [1]
        while True:
            yield L
            L = [1] + [L[i]+ L[i+1] for i in range(len(L)-1)] + [1]
    t = triangles()
    print(next(t))
    print(next(t))
    print(next(t))

# 迭代器 ##################################


from collections import Iterable, Iterator
r = range(10)       # 只是 Iterable，即可以用 for 循环
print(isinstance(r, Iterable), isinstance(r, Iterator))
r = iter(r)         # 变为 Iterator，可以被 next 函数调用
print(next(r), next(r))

