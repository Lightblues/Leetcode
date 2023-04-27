from easonsi import utils
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
https://leetcode.cn/contest/weekly-contest-215
@2022 """

""" 1656. 设计有序流 #easy  """
class OrderedStream:
    def __init__(self, n: int):
        self.stream = {}
        self.idx = 1

    def insert(self, idKey: int, value: str) -> List[str]:
        self.stream[idKey] = value
        ans = []
        while self.idx in self.stream:
            ans.append(self.stream[self.idx])
            self.idx += 1
        return ans
        

class Solution:
    """ 1657. 确定两个字符串是否接近 #medium 可以对一个字符串进行某种规则的两种操作, 问能否转化为另一个 """
    def closeStrings(self, word1: str, word2: str) -> bool:
        if len(word1)!=len(word2): return False
        if set(word1)!=set(word2): return False
        cnt1, cnt2 = Counter(word1), Counter(word2)
        v1, v2 = sorted(cnt1.values()), sorted(cnt2.values())
        return v1==v2
    
    """ 1658. 将 x 减到 0 的最小操作数 #medium 给定一个整数x, 可以从数组两端选择数组, 求两端之和为x的最小数字数量.
思路1: 分别计算前缀后缀和, 用字典来记录 {presum: idx}, 进行匹配, 复杂度 O(n)
思路2: #逆向 等价转换
    可以等价转换为, 求和为 `sum-x` 的最长子数组
    可以 同向 #双指针 复杂度 O(n)
"""
    def minOperations(self, nums: List[int], x: int) -> int:
        # 思路1: 分别计算前缀后缀和 复杂度 O(n)
        n = len(nums)
        presum = list(accumulate(nums, initial=0))
        presum2idx = {a:i for i,a in enumerate(presum)} # 注意 0->0
        ans = inf if x not in presum2idx else presum2idx[x]
        postsum=0
        for i in range(n-1, -1, -1):
            postsum += nums[i]
            tgt = x - postsum
            if tgt in presum2idx and presum2idx[tgt]<i:
                ans = min(ans, presum2idx[tgt] + n-i)
        return ans if ans!=inf else -1
    def minOperations(self, nums: List[int], x: int) -> int:
        # 思路2: #逆向 等价转换
        target = sum(nums) - x
        if target < 0: return -1  # 全部移除也无法满足要求
        ans = -1
        left = s = 0
        for right, x in enumerate(nums):
            s += x
            while s > target:  # 缩小子数组长度
                s -= nums[left]
                left += 1
            if s == target:
                ans = max(ans, right - left + 1)
        return -1 if ans < 0 else len(nums) - ans


    
    """ 1659. 最大化网格幸福感 #hard 非常复杂的DP, 不必掌握
给一个 (m,n) 网格, 有 in,ex 个内向/外向的人可选择. score定义为: 内向的人初始120, 每一个邻居-30; 外向的人初始40, 每一个邻居+20. 不必填入所有人, 要求 score最大.
限制: m,n [1,5]; in,ex [0,6]
思路1: 暴力按行 #DP, 用 #预处理 进行加速. DP转移需要用 #记忆化 搜索求解.
    数量级较小, 考虑采用 #状压 进行记录. 0/1/2 分别记录三种情况.
    记 `f(maskB,row, inL,exL)` 表示当前row行, 上一行为maskB, 内外向剩余人数分别为 inL,exL 时的最大score. 则有转移 `f(maskB,row, inL,exL) = max_mask{ f(mask,row+1, inL-cntIn,exL-cntIn) + score_inner(mask) + score_outer(mask, maskB) }`
        其中 cntIn, cntIn 为当前mask中内外向人的数量; `score_inner, score_outer` 分别计算当前行的分数, 以及相邻行的分数.
    复杂度: 状态数 `3^n*n*6*6`, 每次转移 `3^n`, 因此总时间复杂度 `O(3^2n *n *6*6)`
    see [zero](https://leetcode.cn/problems/maximize-grid-happiness/solution/zui-da-hua-wang-ge-xing-fu-gan-by-zerotrac2/)
思路2: 拓展解法, 叫做 #轮廓线动态规划 见zero
"""
    def getMaxGridHappiness(self, m: int, n: int, introvertsCount: int, extrovertsCount: int) -> int:
        mxRow = 3**n        # 行限制
        # 采用记忆化搜索
        @lru_cache(None)
        def dfs(mask_last, row, nx,wx):
            # 边界
            if row==m or nx+wx==0: return 0
            # 
            best = 0
            for mask in range(mxRow):
                if nx_inner[mask]>nx or wx_inner[mask]>wx: continue
                score = score_inner[mask] + score_outer[mask][mask_last]
                best = max(best, score + dfs(mask, row+1, nx-nx_inner[mask], wx-wx_inner[mask]))
            return best
        return dfs(0, 0, introvertsCount, extrovertsCount)

# 辅助
N = 5
MX = 3**N
mask_span = [[0] * N for _ in range(MX)]    # 转为3进制
nx_inner, wx_inner, score_inner, score_outer = [0] * MX, [0] * MX, [0] * MX, [[0] * MX for _ in range(MX)]

def calc(x,y):
    # 两相邻元素的分数
    if x==0 or y==0: return 0
    if x==1==y: return -60
    if x==2==y: return 40
    return -10
for mask in range(MX):
    # cals mask
    tmp = mask
    for i in range(N):
        mask_span[mask][i] = tmp % 3
        tmp //= 3
        if tmp==0: break
    for i in range(N):
        if mask_span[mask][i]==1:
            nx_inner[mask] += 1
            score_inner[mask] += 120
        elif mask_span[mask][i]==2:
            wx_inner[mask] += 1
            score_inner[mask] += 40
        if i>0:
            score_inner[mask] += calc(mask_span[mask][i-1], mask_span[mask][i])
# 相邻行分数
for mask0 in range(MX):
    for mask1 in range(MX):
        for i in range(N):
            score_outer[mask0][mask1] += calc(mask_span[mask0][i], mask_span[mask1][i])

sol = Solution()
result = [
#     testClass("""["OrderedStream", "insert", "insert", "insert", "insert", "insert"]
# [[5], [3, "ccccc"], [1, "aaaaa"], [2, "bbbbb"], [5, "eeeee"], [4, "ddddd"]]"""),
    # sol.closeStrings(word1 = "cabbba", word2 = "abbccc"),
    # sol.closeStrings(word1 = "cabbba", word2 = "aabbss"),
    sol.minOperations(nums = [1,1,4,2,3], x = 5),
    sol.minOperations(nums = [3,2,20,1,1,3], x = 10),
    sol.minOperations(nums = [5,6,7,8,9], x = 4),
    sol.minOperations([1,1], 3),
    # sol.getMaxGridHappiness(m = 2, n = 3, introvertsCount = 1, extrovertsCount = 2),
    # sol.getMaxGridHappiness(m = 3, n = 1, introvertsCount = 2, extrovertsCount = 1),
    # sol.getMaxGridHappiness(m = 2, n = 2, introvertsCount = 4, extrovertsCount = 0),
]
for r in result:
    print(r)
