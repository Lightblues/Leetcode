""" 
数组元素 0,+/- 1/2/4/8 求连续子数组中, 积最大的子数组范围. 限制: n 1e5
若相同, 则选择尽可能长的、靠右的子数组. 
注意: 定义空数组之积为 1
思路1: 将数组按照0进行分割, 每个部分记录2的因子数量(和负号数量)
    注意, 累乘可能会溢出, 需要转 log相加
"""
# import itertools
import math
n = int(input())
arr = list(map(int, input().split()))
# 辅助数组
log2 = [0] * n
flag = [0] * n
for i,x in enumerate(arr):
    if x==0: continue
    if x<0: flag[i] = 1; x = -x
    log2[i] = int(math.log2(x))
def f(i,j):
    """ 统计 [i,j] 范围内的最大积 
    返回: log2(最大正数积), 左边界, 右边界
    """
    if i>j: return -1, 0,-1
    if sum(flag[i:j+1])%2==0: 
        return sum(log2[i:j+1]), i,j
    else:
        l = i
        while flag[l]==0: l+=1
        r = j
        while flag[r]==0: r-=1
        ll,rr = sum(log2[i:r]), sum(log2[l+1:j+1]),
        if ll>rr or ll==rr and r-i>j-l: return ll, i,r-1
        else: return rr, l+1,j
arr.append(0)
pre = -1    # 上一个边界
ans = (0,0,-1)
while pre<n:
    nxt = arr.index(0, pre+1)
    mx, l,r = f(pre+1, nxt-1)
    if mx>ans[0] or (mx==ans[0] and r-l>=ans[2]-ans[1]):    # 注意这里是 >=
        ans = (mx, l,r)
    pre = nxt
if ans[1]>ans[2]: print(-1)
else: print(ans[1], ans[2])
