
# 函数名也是变量
flag = 0
if flag:
    # abs = 10
    #
    # import builtins
    # builtins.abs = 10

    print(abs)

# 传入函数
flag = 0
if flag:
    def add(x, y, f):
        return f(x) + f(y)
    print(add(1, -1, abs))


# map/reduce ################################
flag = 0
if flag:
    # def f(x):
    #     return x*x
    # r = map(f, [1,2,3,4])       # 注意 map 返回的是一个 Iterator
    # print(list(r))
    #
    # from functools import reduce
    # def add(x, y):
    #     return x+y
    # print(reduce(add, [1, 3, 5, 7]))

    # 一个更有趣的例子：定义将字符串转化为数字的函数
    from functools import reduce

    DIGITS = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}

    def str2int(s):
        def fn(x, y):
            return x * 10 + y
        def char2num(s):
            return DIGITS[s]
        return reduce(fn, map(char2num, s))
    # 实现2：借用了一个 lambda 表达式，并不再使用嵌套的函数定义
    def char2num(s):
        return DIGITS[s]
    def str2intV2(s):
        return reduce(lambda x, y: x * 10 + y, map(char2num, s))

# 这一题的任务是将不规范的英文名转化为规范的格式，自己写得也太臃肿了吧， 不过算是锻炼代码能力？
flag = 0
if flag:
    from functools import reduce
    def normalize(name):
        lower_list = list(chr(i) for i in range(ord('a'), ord('a')+26))
        upper_list = list(chr(i) for i in range(ord('A'), ord('A')+26))
        U2L = dict(zip(upper_list, lower_list))
        L2U = dict(zip(lower_list, upper_list))
        def lower(c):
            if c in upper_list:
                return U2L[c]
            return c
        def upper(c):
            if c in lower_list:
                return L2U[c]
            return c
        name_mapper = map(lower, name[1:])
        return upper(name[0]) + reduce(lambda x, y: x+y, list(name_mapper))
    print(normalize('adam'), normalize('LiST'))

# 实现连乘
flag = 0
if flag:
    from functools import reduce
    def prod(L):
        return reduce(lambda x, y: x*y, L)
    print(prod([3, 5, 7, 9]))

# 实现字符串转 float ，这里直接盗了评论区的一种实现：去除小数点，然后得到一个整数之后将小数点加上去
flag = 0
if flag:
    def str2float(s):
        def mul10(x, y):
            return int(x) * 10 + int(y)
        s = list(s)
        if '.' in s:
            defcimal_poit = len(s) - s.index('.') - 1  # 计算小数点位置
            num = 10**(-defcimal_poit)  # 计算整个数去掉小数点后需乘以多少才能还原
            s.remove('.')  # 去除小数点
            result = round(reduce(mul10, s) * num,
                           defcimal_poit)  # 对计算结果按原数字小数点位数进行四舍五入，避免精度问题造成数字与原数不同
        else:
            result = reduce(mul10, s)
        return result
    print(str2float('45.443'), str2float('.124'))

# filter ###########################################
flag = 0
if flag:
    def not_empty(s):
        return s and s.strip()

    r = list(filter(not_empty, ['A', '', 'B', None, 'C', '  ']))
    print(r)
    # 结果: ['A', 'B', 'C']


# 结合了 filter 和 Iterator 实现素数的筛选，每次取出数列的第一个数字，然后将其倍数删除 ********
# 调试了一下代码，发现 filter 好像是直接作用到 Iterator 上的，所以之前设置的 filter 都会保存在 Iterator 中
flag = 0
if flag:
    def _odd_iter():
        # 生成无限奇数的迭代器
        n = 1
        while True:
            n += 2
            yield n

    def _not_divisible(n):
        return lambda x: x%n > 0        # 注意到，这里的返回的是一个函数，用了 lambda 表达式，非常优雅

    def primes():
        yield 2
        it = _odd_iter()        # 初始序列
        while True:
            n = next(it)        # 返回序列的第一个数
            yield n
            it = filter(_not_divisible(n), it)  # 构造新序列

    for n in primes():      # 注意需要设置终止条件
        if n<1000:
            print(n)
        else:
            break

# filter 的有一个例子：筛选出回文字
flag = 0
if flag:
    def is_palindrome(n):
        n_str = str(n)
        # 获得反向数列的方式：这样的索引方式当然太臃肿了
        # n_rev = [n_str[i] for i in range(len(n_str)-1, -1, -1)]
        # n_rev = ''.join(n_rev)

        # 更优雅的方式，采用列表的索引，注意第二个数字不能填 -1 因为其代表数列最后一个元素，只能留空；而下面的那种是更好的方式：两个都留空，步长为 -1 即可
        # n_rev = n_str[len(n_str)-1::-1]
        n_rev = n_str[::-1]
        return n_str == n_rev
    # 测试:
    output = filter(is_palindrome, range(1, 1000))
    print('1~1000:', list(output))
    if list(filter(is_palindrome, range(1, 200))) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 22, 33, 44, 55, 66, 77, 88, 99, 101, 111, 121, 131, 141, 151, 161, 171, 181, 191]:
        print('测试成功!')
    else:
        print('测试失败!')

# sorted ##################
flag = 0
if flag:
    r = sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.lower, reverse=True)            # 这里的一个技巧：用 str.lower 的方式引用类方法
    print(r)

    L = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]
    def by_name(t):
        return t[0]
    # 按照成绩由高到低排序
    def by_score(t):
        return -t[1]
    L2 = sorted(L, key=by_name)
    print(L2)




# 返回函数 ############################
"""
https://www.liaoxuefeng.com/wiki/1016959663602400/1017434209254976 讲得很好

注意「闭包」的概念：
注意到返回的函数在其定义内部引用了局部变量args，所以，当一个函数返回了一个函数后，其内部的局部变量还被新函数引用，所以，闭包用起来简单，实现起来可不容易。

这也是一个内部函数的作用？
"""
# 实现一个计数器：该函数返回一个可以用来计数的函数，即每次调用返回增加；而再次利用该函数生成一个计数器，计数器清零
flag = 0
if flag:
    # def createCounter():
    #     cnt = [0]               # 将cnt设定为数组，神奇的是这样也可以
    #     def counter():
    #         cnt[0] = cnt[0]+1   # 修改数组中的元素值 【为什么这里就可以引用而下面的实现就会报错】
    #         return cnt[0]       # 返回修改的元素值
    #     return counter

    def createCounter():
        # global a        # 似乎用一组 global 也可以实现，不过关键字 global 好像一般用于 module 级别？
        a = 0
        def counter():
            nonlocal a      # 新学到的一个关键词 nonlocal 【这里没法使用「闭包」中的父函数中的局部变量，或许是因为 a 只是一个 int？】
            # global a
            a = a+1
            return a
        return counter
    # 测试:
    counterA = createCounter()
    print(counterA(), counterA(), counterA(), counterA(), counterA()) # 1 2 3 4 5
    counterB = createCounter()
    if [counterB(), counterB(), counterB(), counterB()] == [1, 2, 3, 4]:
        print('测试通过!')
    else:
        print('测试失败!')






