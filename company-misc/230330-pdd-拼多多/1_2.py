""" 
有一组Boss/商人的线性关卡, m种宝石. 随身只能携带一个宝石. 问最优解. 限制: n,m 1e6
思路1: #记忆化 搜索
    对于商人的位置i, 定义 
    TLE 20%
思路0.2 未完成...
"""
from functools import cache
n,m = map(int, input().split())
arr  = []
for _ in range(n):
    line = input().strip()
    if line.startswith('b'):
        iid = int(line[2:])
        arr.append((0, iid))
    else:
        iid, v = map(int, line[2:].split())
        arr.append((iid, v))
pre = None
xx = []
for iid,v in arr:
    if iid==0:
        if type(pre)==set:
            pre.add(v)
        else:
            pre = set([v])
            xx.append(pre)
    else:
        if type(pre)==dict:
            pre[iid] = v
        else:
            pre = {iid:v}
            xx.append(pre)
ans = 0
n = len(xx)
@cache
def f(i, iid,v, ss):
    """ 在已经有ss金额的情况下, 从i开始, 寻找 iid, 收益为 v """
    global ans
    if i<0: return 
    if iid==0:
        # if type()
        pass
    else:
        if type(xx[i])==set:
            if iid in xx[i]:
                # 找到了!
                ss += xx[i][iid]
                ans = max(ans, ss)
                f(i-1, 0,0, ss)
            f(i-1, iid, v, ss)

f(n-1, 0, 0, 0)
print(ans)
