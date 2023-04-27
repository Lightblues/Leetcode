from easonsi.util.leetcode import *

def testClass(inputs):
    # 用于测试 LeetCode 的类输入
    s_res = [None] # 第一个初始化类, 一般没有返回
    methods, args = [eval(l) for l in inputs.split('\n')]
    class_name = eval(methods[0])(*args[0])
    for method_name, arg in list(zip(methods, args))[1:]:
        r = (getattr(class_name, method_name)(*arg))
        s_res.append(r)
    return s_res

""" 
https://leetcode.cn/contest/weekly-contest-185

这一期的题目都挺有意思. T3 数青蛙 需要考虑一些细节的点; T4 的生成数组 DP表达式也需要考虑一下.

@2022 """
class Solution:
    """ 1417. 重新格式化字符串 """
    def reformat(self, s: str) -> str:
        alphas = [c for c in s if c.isalpha()]
        nums = [c for c in s if c.isdigit()]
        if abs(len(alphas)-len(nums)) > 1: return ""
        if len(alphas) > len(nums):
            return "".join([a+n for a,n in zip(alphas, nums)] + [alphas[-1]])
        else:
            s = "".join([n+a for n,a in zip(nums, alphas)])
            return s if len(nums) == len(alphas) else s+nums[-1]
    
    """ 1418. 点菜展示表 #medium #模拟 有一组 <customer, tableNumber, foodItem> 的点餐记录, 要求根据桌号统计每一道菜的点餐次数, 并按桌号升序输出 """
    def displayTable(self, orders: List[List[str]]) -> List[List[str]]:
        food2idx = {}
        table2foods = defaultdict(lambda: defaultdict(int))
        for c,t,f in orders:
            if f not in food2idx: food2idx[f] = len(food2idx)
            fid = food2idx[f]
            table2foods[t][fid] += 1
        ret = []
        foodnames = sorted(food2idx.keys())
        ret.append(["Table"] + foodnames)
        # 注意桌号是字符串
        for t, foods in sorted(table2foods.items(), key=lambda x:int(x[0])):
            row = [str(t)] + [str(foods.get(food2idx[f], 0)) for f in foodnames]
            ret.append(row)
        return ret
    
    """ 1419. 数青蛙 #medium #题型 #interest 青蛙声音由 croak 的字符串构成. 由于可能有多只青蛙交错, 可能会出现 crcoakroak 这样的字符串. 给定字符串, 问最少需要多少青蛙可以构成这个字符串. 限制: n 1e5
注意, 像 croakcroak 只需要一只即可.
思路1: #贪心. 转化问题为「一组区间的最大重叠数」
    优先匹配最早发声的那只青蛙.
    进一步, 我们可以对于 "croak" 的每一个字符进行匹配. 第i次出现的c于第i次出现的r进行匹配. 这样, 每次发声对应了一个区间, 问题等价于 **一组区间的最大重叠数**.
    对于该问题, 可以用 #前缀 数组进行计算.
"""
    def minNumberOfFrogs(self, croakOfFrogs: str) -> int:
        cnt = Counter(croakOfFrogs)
        if not cnt["c"] == cnt["r"] == cnt["o"] == cnt["a"] == cnt["k"]: return -1
        chars = "croak"
        cmap = {c:i for i,c in enumerate(chars)}
        ch2idxs = [[] for _ in range(5)]
        for i,c in enumerate(croakOfFrogs):
            ch2idxs[cmap[c]].append(i)
        n = len(croakOfFrogs)
        diff = [0] * (n+1)
        for i in range(len(ch2idxs[0])):
            s, e = ch2idxs[0][i], ch2idxs[-1][i]
            for j in range(4):
                if ch2idxs[j+1][i] < ch2idxs[j][i]: return -1
            diff[s] += 1
            diff[e+1] -= 1
        acc = accumulate(diff)
        return max(acc)
    
    """ 1420. 生成数组 #hard 定义一个「从数组中找到最大元素」的算法, 顺序遍历, 定义算法的cost为更新mx的次数k.
现在要求所有的长 n的, 所有数组元素在 [1,m] 范围内的数组中, 代价为 k 的arr的数量. 限制: n 50, m 100; 对答案取模.
思路1: #DP 定义 `f[i,j,k]` 为长度为i, 最大值为j, 代价为k的数组数量.
    考虑转移: 最大值j是哪里来的? 1) 不是最后一个元素 `arr[i]<=j`, 则 k,j 不发生变化, 第i个元素可选 1...j, 计数 `j * f[i-1,j,k]`
        2) 是第i个元素 `arr[i]=j`. 计数 `sum{ f[i-1,jj,k-1] }` 其中jj范围 [1,j-1]
    因此, 总转移方程 `f[i,j,k] = j * f[i-1,j,k] + sum{ f[i-1,jj,k-1] for jj in [1,j-1] }`
        起始: f[1,j,1]=1, 对于k!=1的情况都不合法.
    复杂度: 状态空间 nmk, 转移 m, 因此时间复杂度 `O(nm^2k)`.
思路2: 对于上述 DP, 可以利用 #前缀和 进一步优化转移的复杂度. 
    具体而言, 对于求和式 `sum{ f[i-1,jj,k-1] for jj in [1,j-1] }` 可利用前缀和优化到 O(1).
[official](https://leetcode.cn/problems/build-array-where-you-can-find-the-maximum-exactly-k-comparisons/solution/sheng-cheng-shu-zu-by-leetcode-solution-yswf/)
"""
    def numOfArrays(self, n: int, m: int, k: int) -> int:
        mod = 10**9 + 7
        f = [[[0] * k for _ in range(m)] for _ in range(n)]
        for j in range(m):
            f[0][j][0] = 1
        for i in range(1, n):
            for j in range(m):
                for kk in range(k):
                    f[i][j][kk] = (j+1) * f[i-1][j][kk]
                    for jj in range(j):
                        # 注意避免 kk-1<0
                        f[i][j][kk] += f[i-1][jj][kk-1] if kk > 0 else 0
                    f[i][j][kk] %= mod
        return sum(f[n-1][i][k-1] for i in range(m)) % mod
    
sol = Solution()
result = [
    # sol.reformat("covid2019"),
    # sol.displayTable(orders = [["David","3","Ceviche"],["Corina","10","Beef Burrito"],["David","3","Fried Chicken"],["Carla","5","Water"],["Carla","5","Ceviche"],["Rous","3","Ceviche"]]),
    # sol.minNumberOfFrogs("crcoakroak"),
    # sol.minNumberOfFrogs("croakcrook"),
    sol.numOfArrays(n = 2, m = 3, k = 1),
    sol.numOfArrays(n = 5, m = 2, k = 3),
    sol.numOfArrays(n = 9, m = 1, k = 1),
    sol.numOfArrays(n = 50, m = 100, k = 25),
    sol.numOfArrays(n = 37, m = 17, k = 7),
    
]
for r in result:
    print(r)
