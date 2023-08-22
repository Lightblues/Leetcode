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
https://leetcode.cn/contest/weekly-contest-355
https://leetcode.cn/circle/discuss/1AqXeK/

两道hard的一周. T3的构造比较难想明白 (有时间去看看灵神视频), T4的转换惊艳到了!
Easonsi @2023 """
class Solution:
    """ 2788. 按分隔符拆分字符串 """
    def splitWordsBySeparator(self, words: List[str], separator: str) -> List[str]:
        ans = []
        for word in words:
            for w in word.split(sep=separator):
                if w: ans.append(w)
        return ans
    
    """ 2789. 合并后数组中的最大元素 """
    def maxArrayValue(self, nums: List[int]) -> int:
        pre = 0
        ans = 0
        for x in nums[::-1]:
            if x>pre: pre = x
            else: pre += x
            ans = max(ans, pre)
        return ans
    
    """ 2790. 长度递增组的最大数目 #hard 给定n个数字每个可以使用的limit数量. 要求构造一个数组序列, 满足: 1] 每一个数组的长度递增; 2] 每个数组中的元素个各不相同. 问最长序列
分析: 
    显然, 一个最基本的情况是 [1,2,3] 可以构成长度为3的结果. (假设三个数字分别为0/1/2) 结果为 [[2], [1,2], [0,1,2]]
    需要注意的 [2,2,2] 的情况, 它可以构成 [[0,1,2], [0,1],[2]] 这样的组合!
思路1: #贪心
    直接给出一种 #贪心 构造方式: 先将数组排序, 按照下面的方式填充数字. 注意到剩余的元素只能往后
        正确性: 在于我们已经做了排序!
    见 [讨论](https://leetcode.cn/circle/discuss/1AqXeK/) 彭旭锐
```
# 测试用例 [2, 100, 2, 2, 2] => 排序 [2, 2, 2, 2, 100]
0 => 0 1 => 0 1 2  => 0 1 2 3
       1      1 2       1 2 3
                0         0 4
                            4
```
    """
    def maxIncreasingGroups(self, usageLimits: List[int]) -> int:
        usageLimits.sort()
        # n = len(usageLimits)
        remain = 0; ans = 0
        for x in usageLimits:
            remain += x
            if remain >= ans+1:
                ans += 1
                remain -= ans
        return ans
    
    
    """ 2791. 树中可以形成回文的路径数 #hard 给定一个树, 找到数上所有的路径, 重拍后形成回文!
限制: n 1e5
思路1.0: #树形DP 但是 #TLE
    对于每一个节点, 匹配孩子节点之间是否可构成回文
    复杂度: 节点的状态记录太多! 会超时
思路1.1: 进一步考虑, 对于 u,v 它们之间的路径可以构成回文, 那么找到它们的 「最小公共祖先 lca」, 则 root-lca-u, root-lca-v 两段路径之和也可以构成回文!
    因此, 仅需要记录节点到根的路径即可!
    复杂度: O(n L)
见 [灵神](https://leetcode.cn/problems/count-paths-that-can-form-a-palindrome-in-a-tree/solution/yong-wei-yun-suan-chu-li-by-endlesscheng-n9ws/)
    """
    def countPalindromePaths(self, parent: List[int], s: str) -> int:
        # 思路1.0: #树形DP 但是 #TLE
        n = len(parent)
        childs = [[] for _ in range(n)]
        for u,p in enumerate(parent):
            if p==-1: continue
            childs[p].append(u)
        s = [1<<(ord(i)-ord('a')) for i in s]
        ans = 0
        def dfs(u):
            # if not childs[u]:
            #     return {s[u]:1}
            nonlocal ans
            base = s[u]
            cnt = Counter()
            for v in childs[u]:
                tmp = dfs(v)
                for m,c in tmp.items():
                    if m.bit_count()<=1: ans += c
                    # 1] ^ ==0
                    ans += cnt[m] * c
                    # # 2] 比m少一位
                    # mask = m
                    # while mask:
                    # # 获取最低位
                    #     lowbit = mask & -mask
                    #     ans += cnt[mask ^ lowbit] * c
                    #     mask ^= lowbit
                    # # 3] 比m多一位
                    # for i in range(26):
                    #     if 1<<i & m: continue
                    #     ans += cnt[m | (1<<i)] * c
                    for i in range(26):
                        ans += cnt[m ^ (1<<i)] * c
                for m,c in tmp.items():
                    cnt[m] += c
            cnt = Counter({m^base:c for m,c in cnt.items()})
            cnt[base] += 1
            
            return cnt
        dfs(0)
        return ans
    def countPalindromePaths(self, parent: List[int], s: str) -> int:
        n = len(parent)
        childs = [[] for _ in range(n)]
        for u,p in enumerate(parent):
            if p==-1: continue
            childs[p].append(u)
        s = [1<<(ord(i)-ord('a')) for i in s]
        ans = 0
        cnt = Counter()
        cnt[0] = 1
        def dfs(u, w):
            nonlocal ans
            for v in childs[u]:
                x = w ^ s[v]
                ans += cnt[x] + sum(cnt[x ^ (1<<i)] for i in range(26))
                cnt[x] += 1
                dfs(v, x)
        dfs(0, 0)
        return ans
            
    
sol = Solution()
result = [
    # sol.splitWordsBySeparator(words = ["one.two.three","four.five","six"], separator = "."),
    # sol.splitWordsBySeparator(words = ["|||"], separator = "|"),
    
    # sol.countPalindromePaths(parent = [-1,0,0,1,1,2], s = "acaabc"),
    # sol.countPalindromePaths(parent = [-1,0,0,0,0], s = "aaaaa"),
    # sol.countPalindromePaths([-1,4,0,4,6,0,5,5], "bhrlorou"),   # 18
    
    sol.maxIncreasingGroups(usageLimits = [1,2,5]),
    sol.maxIncreasingGroups(usageLimits = [2,1,2]),
]
for r in result:
    print(r)
