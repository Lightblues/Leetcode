

# 创建单元素 tuple
flag = 0
if flag:
    t = tuple([1])
    print(t)
    t = (2, )
    print(t)

# 注意 tuple 内的 list 还是可变的
flag = 0
if flag:
    t = (1, 2, [2,3])
    t[2][1] = "something"
    print(t)

# set 可以做 & | 运算
flag = 0
if flag:
    s1 = {1, 2, 3}      # 直接这样定义 set
    s2 = set([2,3,4])
    print(s1&s2, s1|s2)

# 注意函数的参数必须指向不变对象
flag = 0
if flag:
    def add_end(L=[]):
        L.append('END')
        return L
    print(add_end())
    print(add_end())

    # 这就是因为参数 L 也会指向一个对象，可变而出错；可以这样修改
    def add_end(L=None):
        if L is None:
            L = []
        L.append('END')
        return L

    print(add_end())
    print(add_end())


# 可变参数
flag = 0
if flag:
    def calc(*numbers):
        sum = 0
        for n in numbers:
            sum = sum + n * n
        return sum
    print(calc(1,2,3))
    print(calc(*[1,2,3]))


# 关键字参数
flag = 0
if flag:
    def person(name, age, **kw):
        print('name:', name, 'age:', age, 'other:', kw)
    extra = {'city': 'Beijing', 'job': 'Engineer'}
    person('Jack', 24, city=extra['city'], job=extra['job'])
    person('Me', 23, **extra)

    # 注意可变参数将其整理成了一个 tuple，但输出的形式是多个元素
    # def f1(*ps):
    #     for p in ps:
    #         print(p)
    # f1(12,2,3)

    # 注意到关键字参数将其整理成了一个字典， 但输入的形式是多个键值对
    # def f2(**ps):
    #     for p in ps.items():
    #         print(p)
    # f2(**{'1':"ONE", '2':"TWO"})


# 函数迭代：汉诺塔问题
flag = 0
if flag:
    def move(n, a, b, c):
        if n == 1:
            print(a, '-->', c)
        else:
            move(n-1, a, c, b)
            print(a, '-->', c)
            move(n-1, b, a, c)
    move(3, "A", "B", "C")