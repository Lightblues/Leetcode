""" 
AB 各自一个长n的0/1字符串, 分别选择位置, 拿到自己的字符. 选过的位置不可重复. 最后每人 n/2 个. 输出 red/draw/friend
限制: n 2e5

思路1: #数学 推导
    记两者都有/小红/朋友单独的位置数量为 a,b,c
    注意到, 两者一开始的最优策略都是抢a; 没有a的情况下, 抢自己或者堵对方! 
    1] 考虑 a=0 时, b=c/c-1 的时候, 平局
    2] 考虑 a=1 时, b=c-1/c-2 的时候, 平局

3
4
1100
1000
4
1100
1001
4
1100
1100
# red
# red
# draw
"""
def f():
    n = int(input())
    arrA = list(map(int, input().strip()))
    arrB = list(map(int, input().strip()))
    a,b,c = 0,0,0
    for i,j in zip(arrA,arrB):
        if i==j==1: a += 1
        elif i==1: b += 1
        elif j==1: c += 1
    if a%2==0:
        if b > c: print('red')
        elif b==c or b==c-1: print('draw')
        else: print('friend')
    else:
        if b > c-1: print('red')
        elif b==c-2 or b==c-1: print('draw')
        else: print('friend')

n = int(input())
for _ in range(n):
    f()
