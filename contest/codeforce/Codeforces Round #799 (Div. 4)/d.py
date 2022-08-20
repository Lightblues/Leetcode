""" D. The Clock
有一个24小时制的时钟, 从start时刻开始, 每隔x分钟看一次时钟 (时间无限) 问看到的时刻中有多少种是回文数 (例如 12:21 )?
思路1: #模拟 判断, 用 #记忆化 来加速

注意CF用的是Python3.x, 不支持cache语法.
"""
from functools import lru_cache

@lru_cache(None)
def check_palindrome(num: int):
    hours, mins = divmod(num, 60)
    return f"{hours:02d}"[::-1] == f"{mins:02d}"
MAX = 24*60
@lru_cache(None)
def check_time(t:int, x:int):
    s = set()
    ans = 0
    while t not in s:
        if check_palindrome(t):
            ans += 1
        s.add(t)
        t = (t+x) % MAX
    return ans

def f():
    t, x = input().split()
    h,m = map(int, t.split(':'))
    t = h*60 + m
    x = int(x)
    print(check_time(t, x))

for _ in range(int(input())):
    f()