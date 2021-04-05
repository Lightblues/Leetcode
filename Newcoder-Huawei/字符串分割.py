"""
题目描述
•连续输入字符串，请按长度为8拆分每个字符串后输出到新的字符串数组；
•长度不是8整数倍的字符串请在后面补数字0，空字符串不处理。

输入描述:
连续输入字符串(输入多次,每个字符串长度小于100)

输出描述:
输出到长度为8的新字符串数组

示例1
输入
复制
abc
123456789
输出
复制
abc00000
12345678
90000000
"""
while True:
    try:
        line = input().strip()
        l = len(line)
        n, res = divmod(l, 8)
        for i in range(n):
            print(line[i*8: (i+1)*8])
        if res:
            print(line[-res:] + '0'*(8-res))
    except:
        break