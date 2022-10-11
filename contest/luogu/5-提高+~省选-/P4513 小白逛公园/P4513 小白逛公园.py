""" P4513 小白逛公园 提高+/省选-
有一个数组, 有两类操作: 1) 将指定位置的值修改; 2) 查询 [l,r] 范围内的最大值.
思路1: #线段树 下面的代码有问题, 有机会看一下...
"""

import math

n,m = map(int, input().split())
arr = [0] * n
for i in range(n):
    arr[i] = int(input())

mx = [0] * (4*n)
def query(o,l,r, left, right):
    # 查询 [left, right] 区间内的最大值
    if l>=left and r<=right:
        return mx[o]
    m = (l+r)//2
    ans = -math.inf
    if m>=left: ans = max(ans, query(2*o,l,m, left,right))
    if m<right: ans = max(ans, query(2*o+1,m+1,r, left,right))
    return ans
def update(o,l,r, idx, val):
    # 将idx节点的值更新为val
    if l==r:
        mx[o] = val
        return
    m = (l+r)//2
    if idx<=m: update(2*o,l,m, idx, val)
    else: update(2*o+1,m+1,r, idx, val)
    mx[o] = max(mx[2*o], mx[2*o+1])
def build(o,l,r):
    # 递归构建线段树
    if l==r:
        mx[o] = arr[l-1]; return
    m = (l+r)//2
    build(2*o,l,m)
    build(2*o+1,m+1,r)
    mx[o] = max(mx[2*o], mx[2*o+1])

build(1,1,n)
# ans = []
for i in range(m):
    t,a,b = map(int, input().split())
    if t==1:
        # ans.append(query(1,1,n,a,b))
        print(query(1,1,n,a,b))
    else:
        update(1,1,n,a,b)
# print()
""" 

5 3
1
2
-3
4
5
1 2 3
2 2 -1
1 2 3
"""