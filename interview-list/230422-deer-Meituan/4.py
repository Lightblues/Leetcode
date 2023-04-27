""" 删除01串
给定一个01串, 可以删除前后缀(保留连续子串); 删除的代价为, 删除部分1的个数 + 保留部分0的个数; 要求最小化代价
限制: n 1e5
例子
输入: 101110110
输出: 2

思路1: 问题转化. 
    记保留的字符串为 ss, 其中包含的0和1的个数分别为 c0,c1, 则代价为 c0 + (cnt1 - c1), 其中cnt1为完整字符串中1的个数, 是一个常数不影响
    因此, 目标是最小化 c0-c1. 
    这样, 我们将0/1分别映射为 -1/1, 问题就转化为「求和最大的连续子串」
    做法: 经典的 #DP, 
        记 f[x] 表示以x结尾的最大和, 则 f[x] = max{ f[x-1]+s[x], s[x] }
    复杂度: O(n)
"""
def min_cost(s):
    """ 下面写得复杂了! 以为要记录 [l,r] 区间, 但实际上dp的答案就是 c1-c0 """
    cnt1 = s.count('1')
    # 将0/1分别映射为 -1/1, 问题就转化为「求和最大的连续子串」
    arr = [-1 if c=='0' else 1 for c in s]
    mx = arr[0] # 记录答案
    l,r = 0,0   # 记录答案区间
    ll = 0      # 当前f[x]的起点
    cur = 0     # 当前f[x]值
    for i,x in enumerate(arr):
        if cur<=0:
            cur = x
            ll = i
        else: cur += x
        if cur>mx:
            mx = cur
            l,r = ll,i
    ss = s[l:r+1]
    c0 = ss.count('0')
    c1 = ss.count('1')
    return c0 + (cnt1-c1)
def min_cost(s):
    cnt1 = s.count('1')
    # 将0/1分别映射为 -1/1, 问题就转化为「求和最大的连续子串」
    arr = [-1 if c=='0' else 1 for c in s]
    n = len(arr)
    f = [0]*n
    f[0] = arr[0]
    mx = f[0]
    for i in range(1,n):
        f[i] = max(f[i-1]+arr[i], arr[i])
        mx = max(mx, f[i])
    return cnt1 - mx


s = input().strip()
print(min_cost(s))


