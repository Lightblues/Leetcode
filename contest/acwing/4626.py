""" 4626. 最小移动距离
https://www.acwing.com/problem/content/4629/
n个节点每个节点连出一条边. 要求一个「最小移动距离」t. 使其满足: 若x经过t步可以到y, 则y经过t步也可以到x. (互相可达)
提示: 要满足这一强条件, 可以一定是几个环.
思路1: 判断是否都是环; 然后求 #最小公倍数
    细节: 对于长度 l 为奇数的环, 最小满足条件的 t=l//2; 偶数就是 t=l
    
"""
import math
from functools import reduce

n = int(input())
g = list(map(int, input().split()))
g = [i-1 for i in g]

# 判断是否都是环
# seen = [False] * n
remains = set(range(n))
circle_lens = []    # 所有环的长度
while remains:
    head = remains.pop()
    length = 1
    i = g[head]
    while i != head:
        if i not in remains: print(-1); exit()
        remains.remove(i)
        i = g[i]
        length += 1
    circle_lens.append(length)

# 对于长度 l 为奇数的环, 最小满足条件的 t=l//2; 偶数就是 t=l
circle_lens = [i if i%2 else i//2 for i in circle_lens]
def lcm(a, b):
    # 3.9 之后可以用 math.lcm
    return a * b // math.gcd(a, b)
ans = reduce(lambda x,y: lcm(x,y), circle_lens)
print(ans)