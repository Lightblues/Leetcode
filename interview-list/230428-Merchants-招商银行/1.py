""" 
有某个真实的数字, 现在给定N个半区间 (例如 >=x, <=x) 的论断, 判断可能的最少的错误论断的数量. 
限制: N 1e3
2
G 1
L 4
# 0
2
G 6
L 5
# 1

思路1: 
    问题等价, 找到重复区间的最大值. 
    题目中的时间范围很大, 一种思路是对时间进行离散化
    另外, 可以对 G, L 的时间分别排序. 先在-inf位置满足 len(L) 个要求作为 cc
        然后, 对于G,L序列中的较小数字, 若较小的是G, 则cc+1, 否则cc-1
    复杂了! 可以直接双指针! 在G上遍历一遍即可!!
"""
n = int(input())
G,L = [],[]
for _ in range(n):
    c,x = input().split()
    if c=='G':
        G.append(int(x))
    else:
        L.append(int(x))
G.sort()
L.sort()
a,b = len(G),len(L)
cc = len(L)
mx = cc
j = 0
for i,g in enumerate(G):
    while j<b and L[j]<g:
        cc -= 1
        j += 1
    cc += 1
    mx = max(cc, mx)
print(n - mx)

