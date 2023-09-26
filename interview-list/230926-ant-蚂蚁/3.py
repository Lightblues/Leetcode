
""" 
给定序列. 对于若干相邻数字i可以合并成i+1. 问最终可以得到的最大数字. 
限制: n 1e5

思考: 
    考虑例子 
    [4,2,1,1,3,5] 需要左右「拓展」
    [4,2,1,1,2,3,5] 需要清理条左右多余的数字! 
    [4,2,1,1,...,1,1,3,4] 往一边拓展! 但是注意, 一定可以「吃掉另一边」
    比较难的例子: [1,1,2,2,1,1,4]
从哪些位置开始拓展? 从小开始! 并且标记已经走过的位置! 

思路1: 并查集! #todo #hard

6
1 3 1 1 1 2
# 4
6
1 1 1 1 1 9
# 9
"""
import math
n = int(input())
arr = list(map(int, input().split()))
# (num, cnt)
nums = []
lst = cnt = -1
for x in arr+[-1]:
    if x!=lst:
        cnt = 1
        if lst!=-1: nums.append((lst,cnt))
    lst = x
m = len(nums)


ans = max(arr)
# visited = set()
# for v,idx in vals:
#     if idx in visited: continue
from collections import defaultdict
# {idx: (val,cnt,l,r)}
idx2vals = {}
for i,(v,c) in enumerate(nums):
    idx2vals[i] = (v,c,i,i)
fa = list(range(m))
def find(x):
    while fa[x]!=x:
        x = fa[x]
    return x
def merge(x,y):
    fx,fy = find(x),find(y)
    if idx2vals[fx][0]>idx2vals[fy][0]:
        fx,fy = fy,fx
    if fx!=fy:
        vx,cx,lx,rx = idx2vals[fx]
        vy,cy,ly,ry = idx2vals[fy]
        pass

# print(math.log2(4))
print(ans)
