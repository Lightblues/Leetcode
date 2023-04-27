""" P1016 [NOIP1999 提高组] 旅行家的预算
给定两个城市之间的距离 dist, 汽车油箱容量 capacity, 每升汽油可以行驶的距离 range. 除了出发城市之外, 路上还有N个加油站, 每个加油站的价格可能不同.
问能否到达目的地, 能的话 返回最小花费.
不知道为啥试了两种方案, 还是有WA
思路1: #贪心 
    表示: 这些段落用 `steps = [(cost_i, remains_i)]` 表示, 其中第一项cost从距离转为所需的油量, remains 是这一段剩余的路程/所需的油.
    贪心: 对于price从小到大排序, 这样尽量从价格小的油走最多的路. 从当前(最优油价)开始向后查看, 直到油箱的边界情况.
思路2: #贪心 到达下一个加油点
    从一个点出发, 加多少油? 
        如果可以到达一个比当前油价低的点, 那么就加这么多油
        否则, 就加满油, 到能够到达的加油点中价格最低的那一个 (当前油价更低)
        
https://www.luogu.com.cn/problem/P1016 吐了, 不知道为啥WA...
"""
dist, capacity, per, p0, n = map(float, input().split())
n = int(n)
prices = [p0]
dists = [0]
for _ in range(int(n)):
    d,p = map(float, input().split())
    prices.append(p)
    dists.append(d - dists[-1])
dists = dists[1:] + [dist - sum(dists)]
needed = [d/per for d in dists]
if any(i>capacity for i in needed):
    print("No Solution")
    exit()
# needed 为各阶段需要的油量; prices 为各加油站的价格

def v0():
    """ 思路1 """
    steps = [[ne, ne] for ne in needed]
    prices = [(p,i) for i,p in enumerate(prices)]
    prices.sort()
    ans = 0
    for p,i in prices:
        c = capacity
        for j in range(i,n+1): 
            cost, remain = steps[j]
            # 之前的一定填充的是前面的 (cost-remain) 部分, 因此新填充的应该姐在后面
            if remain>0 and c>(cost-remain):
                cover = min(cost, c - (cost-remain))
                ans += p * cover
                steps[j][1] -= cover
            c -= cost
            if c<=0: break
    print(f"{ans:.2f}")


def search(idx):
    # 找到价格比 prices[idx] 低的点; 或者次高点
    p = prices[idx]
    c = capacity - needed[idx]
    bestPrice, best = prices[idx+1], idx+1 # 次高价格的加油站
    for i in range(idx+1, N):
        if needed[i]>c: break
        c -= needed[i]
        if prices[i] <= p:
            return i
        if prices[i] < bestPrice:
            bestPrice, best = prices[i], i
    return best
# 哨兵
prices.append(0); needed.append(0)
N = len(needed)
idx = 0
ans = 0
remained = 0
while idx != N-1:
    # 从能够到达的点中寻找
    nextIdx = search(idx)
    if prices[nextIdx] <= prices[idx]:
        # 找到了下一个价格更低的加油点
        ans += prices[idx] * (sum(needed[idx:nextIdx]) - remained)
        # idx = nextIdx
        remained = 0
    else:
        # 否则, 加满油
        ans += prices[idx] * (capacity - remained)
        remained = capacity - sum(needed[idx:nextIdx])
    idx = nextIdx
print(f"{ans:.2f}")