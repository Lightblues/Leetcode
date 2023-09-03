""" 对于一个字符串, 判断严格进行K次修改是否可变为回文 
若为偶数长度: 非对称数量 <= K 
奇数: 非对称数量 <= K
"""

def check(s: str, k:int):
    n = len(s)
    acc = 0
    for i in range(n//2):
        if s[i]!=s[n-1-i]: acc += 1
    return acc<=k

n = int(input())
for _ in range(n):
    s = input().strip()
    k = int(input())
    if check(s, k):
        print("YES")
    else: print("NO")
    

