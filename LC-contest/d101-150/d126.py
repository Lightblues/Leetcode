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
https://leetcode-cn.com/contest/biweekly-contest-126
T3 需要转一下思路
T4 逆向思维, 再用 0-1 背包
Easonsi @2023 """
class Solution:
    """ 3079. 求出加密整数的和 """
    def sumOfEncryptedInt(self, nums: List[int]) -> int:
        ans = 0
        for x in nums:
            s = str(x)
            ans += int(max(s) * len(s))
        return ans
    
    """ 3080. 执行操作标记数组中的元素 """
    def unmarkedSumArray(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        ans = []
        s = sum(nums)
        marked = set()
        vals = [(q,i) for i,q in enumerate(nums)]
        vals = deque(sorted(vals))
        for i,k in queries:
            if i not in marked:
                s -= nums[i]
                marked.add(i)
            while vals and k>0:
                v,i = vals.popleft()
                if i in marked: continue
                s -= v; k -= 1
                marked.add(i)
            ans.append(s)
        return ans
    
    """ 3081. 替换字符串中的问号使分数最小 #medium 对于字符串中的 ? 位置填空, 要求分数最小. 每个位置i的分数是此前位置出现ch的次数. 分数相同的话, 最小字典序. 
注意: 对于 abcd...xy??, 填入az和za的分数相同, 但是前者的字典序更小! --> 不能从左到右贪心了
思路1: 找到填入的集合之后排序
    注意到, 字母的顺序不重要! 关键在于最后 sorted(s)
    """
    def minimizeStringValue(self, s: str) -> str:
        cnt = Counter(); num_q = 0
        for ch in string.ascii_lowercase: cnt[ch] = 0
        for c in s:
            if c=='?': num_q += 1
            else: cnt[c] += 1
        q = [(c,ch) for ch,c in cnt.items()]
        heapify(q)
        added = []
        for _ in range(num_q):
            c,ch = heappop(q)
            added.append(ch)
            heappush(q, (c+1, ch))
        ans = list(s)
        added.sort(); idx = 0
        for i,c in enumerate(s):
            if c=='?': ans[i] = added[idx]; idx += 1
        return ''.join(ans)
    
    """ 3082. 求出所有子序列的能量和 #hard 对于一个数组, 能量和定义为其子序列中和为k的数量. 现给定一个nums, 求其所有子序列的能量和. 
限制: k 100; k 100
思路1: #逆向 考虑一个和为k的子序列的贡献. 
    显然, 对于长为 l 的和k的子序列, 它可能在 2**(n-l) 个子序列中产生贡献! 
    复杂度? O(n^2 k)
[ling](https://leetcode.cn/problems/find-the-sum-of-the-power-of-all-subsequences/solutions/2691661/liang-chong-fang-fa-er-wei-yi-wei-0-1-be-2e47/)
灵神有复杂度更低的 0-1 背包思路
    """
    def sumOfPower(self, nums: List[int], k: int) -> int:
        n = len(nums)
        cnt = [Counter() for _ in range(k+1)]  # 到idx为止和为x的大小为a的子序列个数
        for i,x in enumerate(nums):
            if x>k: continue
            for j in range(k,x,-1):
                for l,c in cnt[j-x].items():
                    cnt[j][l+1] += c
            cnt[x][1] += 1
        MOD = 10**9+7
        ans = 0
        for l,c in cnt[k].items():
            ans += c * pow(2, n-l, MOD)
        return ans % MOD
    
sol = Solution()
result = [
    # sol.sumOfEncryptedInt(nums = [10,21,31]),
    # sol.unmarkedSumArray(nums = [1,2,2,1,2,3,1], queries = [[1,2],[3,3],[4,2]]),
    # sol.minimizeStringValue(s = "???"),
    # sol.minimizeStringValue( s = "a?a?"),
    # sol.minimizeStringValue("abcdefghijklmnopqrstuvwxy??"),
    # sol.minimizeStringValue("eq?umjlasi"),
    # sol.sumOfPower( nums = [1,2,3], k = 3),
    sol.sumOfPower([6,1,3,1], 10),
]
for r in result:
    print(r)
