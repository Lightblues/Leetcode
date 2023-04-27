""" 检查骰子是否合法. 要求相对面之和相同, 面数为n
T 100; n 1e5; 数字 1e5

思路1: #贪心
    排序之后检查是否和相同
"""
T = int(input())
def f():
    n = int(input())
    if n%2: return False
    arr = list(map(int, input().strip().split()))
    arr.sort()
    tgt = arr[0] + arr[-1]
    for i in range(n//2):
        if arr[i] + arr[-i-1] != tgt: return False
    return True

for _ in range(T):
    ret = f()
    print("YES" if ret else "NO")
