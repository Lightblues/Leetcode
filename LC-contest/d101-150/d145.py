from typing import *
from math import ceil
from heapq import heappop, heappush
from bisect import bisect_right

""" @2025-06-07
https://leetcode.cn/contest/biweekly-contest-145

Easonsi @2025 """
class Solution:
    """ 3375. 使数组的值全部为 K 的最少操作次数 """
    def minOperations(self, nums: List[int], k: int) -> int:
        ans = 0
        for x in sorted(set(nums), reverse=True):
            if x < k: return -1
            elif x==k: continue
            else: ans += 1
        return ans

    """ 3376. 破解锁的最少时间 I #medium 有一组锁需要一定消耗一定分数可以打开. 
每一时刻: 分数S增加 X (初始S=0; X=1); 决定是否开锁, 若开锁, 消耗**全部分数**, 但 X+=K. 问所需最小时间
限制: n 8; val 1e6
思路0 #模拟 #贪心 排序, 能量满足就打开
    ERROR 审题错误
    注意审题: 每次开锁消耗全部分数!
    无法贪心? strength = [3,4,1], k = 1
    第一轮: 等待1次后打开i=2; 增加 X=2;
    第二轮: 等待2次后应该打开i=1; 增加 X=3;
    第三轮: 等待1次后直接打开i=0; 增加 X=4; 注意上一步若开i=0则无法打开!
    """
    def findMinimumTime(self, strength: List[int], k: int) -> int:
        x = 1
        ans = 0
        # for val in sorted(strength):
        #     ans += ceil(val / x)
        #     x += k
        # return ans
        strength.sort()
        while strength:
            delta = ceil(strength[0] / x)
            ans += delta
            strength.pop(bisect_right(strength, x*delta)-1)
            x += k
        return ans
    
    """ 3377. 使两个整数相等的数位操作 #medium 对于两个数位相同的整数. 每次选择n的一位 +/- 1; 最后将其变为m; 要求每次操作后n都不是质数. 问操作过程中所有数字和的最小值. 
限制: n,m 1e4
思路1: #UCS #搜索
[ling](https://leetcode.cn/problems/digit-operations-to-make-two-integers-equal/solutions/3013737/dijkstra-zui-duan-lu-pythonjavacgo-by-en-ofby/)
指出是 #Dijkstra
    """
    def minOperations(self, n: int, m: int) -> int:
        # build prime table
        mx = 10**5
        isPrime = [False, False] + [True] * (mx)
        for i in range(2,mx+1):
            if isPrime[i]:
                for j in range(i*i,mx+1,i):
                    isPrime[j] = False
        
        if isPrime[n] or isPrime[m]: return -1  # NOTE: 边界情况!
        # search
        h = [(n, n)]; vis = set([n])
        def get_cands(x: int) -> list[int]:
            out = []
            chars = list(str(x))
            for i,ch in enumerate(chars):
                if ch<"9":
                    chars[i] = chr(ord(ch)+1)
                    out.append(int("".join(chars)))
                if ch>"0" and not (ch=="1" and i==0):
                    chars[i] = chr(ord(ch)-1)
                    out.append(int("".join(chars)))
                chars[i] = ch
            return sorted(out)
        while h:
            s, x = heappop(h)
            if x==m: return s
            for cand in get_cands(x):
                if cand in vis or isPrime[cand]: continue
                vis.add(cand)
                heappush(h, (s+cand, cand))
        return -1

    """ 3378. 统计最小公倍数图中的连通块数目 #hard 给定一组数字. 任意两个节点的 #lcm <=th 则连边. 问构成图的连通块数量.
限制: n 1e5; val 1e9; th 2e5
思路1: #并查集 + 枚举 #GCD
    #模板 两个注意点:
    1. 看到 LCM 就应该联想到 GCD; 有关系 x*y / GCD(x,y) = LCM(x,y)
    2. gcd 出现在分母上, 就应该想到枚举 g = GCD(x,y)
        这是因为调和级数相加, 复杂度可控! O(log T) 级别
    回到本题, 要求 x*y / GCD(x,y) <= th. 转为枚举 g, 那么如何再遍历 x,y 呢? 
        显然不能两层for, 因为g的倍数有 th/g 个, 单考虑一个g的复杂度就是 O((th/g)^2) 超时了!
        核心是只考虑最小的x (g的倍数)! 因为更大的数字必然也能和x连起来! 用并查集即可
    复杂度? 
        并查集平均 O(a)
        两层for O(t log(t))
[ling](https://leetcode.cn/problems/count-connected-components-in-lcm-graph/solutions/3013720/mei-ju-gcd-bing-cha-ji-pythonjavacgo-by-sq6vd/)
 """
    def countComponents(self, nums: List[int], threshold: int) -> int:
        # 
        n = len(nums)
        fa = list(range(n))
        def find(x:int) -> int:
            rt = x
            while fa[rt] != rt:
                rt = fa[rt]
            while fa[x] != rt:
                fa[x], x = rt, fa[x]
            return rt
        # build the map -- 注意题目保证了元素互不相等
        m = {x:i for i,x in enumerate(nums)}
        # enum g
        for g in range(1, threshold+1):
            x_group = -1
            for x in range(g, threshold, g):
                if x in m:
                    x_group = find(m[x])
                    break
            if x_group < 0: continue
            # y <= g*th/x
            for y in range(x+g, g*threshold//x+1, g):
                if y in m:
                    y_group = find(m[y])
                    if x_group != y_group:
                        fa[y_group] = x_group
                        n -= 1  # reduce the # components
        return n


sol = Solution()
result = [
    # sol.minOperations(nums = [9,7,5,3], k = 1),
    # sol.minOperations(nums = [5,2,5,4,5], k = 2),
    sol.findMinimumTime(strength = [3,4,1], k = 1),
    sol.findMinimumTime(strength = [2,5,4], k = 2),
    sol.findMinimumTime([46,11,13], 4),
    # sol.minOperations(n = 10, m = 12),
    # sol.minOperations(n = 4, m = 8),
    # sol.countComponents(nums = [2,4,8,3,9], threshold = 5),
    # sol.countComponents(nums = [2,4,8,3,9,12], threshold = 10),

]
for r in result:
    print(r)
