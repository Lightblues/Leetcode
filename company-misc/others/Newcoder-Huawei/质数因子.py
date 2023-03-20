"""
题目描述
功能:输入一个正整数，按照从小到大的顺序输出它的所有质因子（重复的也要列举）（如180的质因子为2 2 3 3 5 ）

最后一个数后面也要有空格

输入描述:
输入一个long型整数

输出描述:
按照从小到大的顺序输出它的所有质数的因子，以空格隔开。最后一个数后面也要有空格。

示例1
输入
复制
180
输出
复制
2 2 3 3 5
"""


def mytry():
    num = int(input().strip())

    # from https://stackoverflow.com/questions/25706885/generator-function-for-prime-numbers
    def getPrime(n):
        yield 2
        for i in range(3, n, 2):
            for x in range(3, int(i ** .5), 2):
                if i % x == 0:
                    break
            else:
                # 注意这里的 break...else 语法
                yield i

    gen = getPrime(num + 1)
    res = []
    while num > 1:
        prime = next(gen)
        while num % prime == 0:
            res.append(prime)
            num /= prime
    print(' '.join(list(map(str, res))) + ' ')


n = int(input())

i = 2
while i * i <= n:
    # 这里简单用了加一的方式，并且实时更新 n，以缩小范围
    # 当然还可以排除 2 之后以步长 2 进行更新
    while n % i == 0:
        n = n // i
        print(i, end=" ")
    i = i + 1
if n - 1:
    print(n, end=" ")
