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
https://leetcode.cn/contest/weekly-contest-412
两道题, 事后来看不算太难, 但做起来很费劲!
T3 解题的部分代码太糟糕了
T4 反过来, 考虑每个数字可能形成的所有结果! 有启发

Easonsi @2023 """
class Solution:
    """ 3264. K 次乘运算后的最终数组 I 每次从nums中找到最小的, *multiplier . 返回进行k次操作后的结果. 
限制: k 10
"""
    def getFinalState(self, nums: List[int], k: int, multiplier: int) -> List[int]:
        for _ in range(k):
            idx = nums.index(min(nums))
            nums[idx] *= multiplier
        return nums
    
    """ 3265. 统计近似相等数对 I 对于 (i,j) 两个数字, 若对一个数字进行之多进行两个数位的交换后数字相等, 则满足条件. 统计满足条件的数量.
例子: 3 和 30 。交换 30 中的数位 3 和 0 ，得到 3 
限制: n 100; x 1e5
    """
    def countPairs(self, nums: List[int]) -> int:
        nums = [str(x) for x in nums]
        maxL = max(map(len, nums))
        nums = ['0' * (maxL-len(x)) + x for x in nums]
        def check(x,y):
            if sorted(x) != sorted(y): return False
            c = sum(i!=j for i,j in zip(x,y))
            return c<=2
        ans = 0
        for i,x in enumerate(nums):
            for j in range(i+1, len(nums)):
                ans += check(x, nums[j])
        return ans
    
    """ 3266. K 次乘运算后的最终数组 II #hard 相较于 T1 增加了限制, 同时对结果取模.
限制: n 1e4; k 1e9; multiplier 1e6
思路1: 直接计算分配到每个idx的乘法次数 -> 但实际上写起来很复杂. 下面G了
    例子: nums = [2,1,3,5,6], k = 5, multiplier = 2
    先计算每个数字log2的结果 [(1,0), (0,0), (1,0.58..), (2,0.32..), (2,0.58..)] 后面的部分是小数点
        这样, 将 k=5 分配的结果是 [2,2,1,0,0] -> 先根据 (整数部分,idx) 分配, 再按照 (小数部分,idx) 进行分配
思路2: 用 #推 来实现
    像一个如果用堆来实现, 最多会进行多少次? log(MAX, multiplier) * n < log2(1e4) * n 也不高! 可以直接用堆来找! 
    -> 优化的部分类似上面思路1, 参见ling
[ling](https://leetcode.cn/problems/final-array-state-after-k-multiplication-operations-ii/solutions/2892178/zui-xiao-dui-mo-ni-shu-xue-gong-shi-pyth-z4zw/)
    """
    def getFinalState(self, nums: List[int], k: int, multiplier: int) -> List[int]:
        # 边界! 
        if multiplier == 1:
            return nums
        MOD = 1_000_000_007
        n = len(nums)
        mx = max(nums)
        h = [(x,i) for i,x in enumerate(nums)]
        heapify(h)
        # 
        while k and h[0][0] < mx:
            x,i = h[0]
            heapq.heapreplace(h, (x*multiplier, i))
            k -= 1
        # the remains
        h.sort() # 这里可以直接sort了
        _a,r = divmod(k, n)
        for i,(x,idx) in enumerate(h):
            nums[idx] = x * pow(multiplier, _a + int(i<r), MOD) % MOD
        return nums
    
    # def getFinalState(self, nums: List[int], k: int, multiplier: int) -> List[int]:
    #     """ 太脏的写法了, 不过还有 corner case 挂了! """
    #     if multiplier == 1:
    #         return nums
    #     p1 = []
    #     p2 = []
    #     for x in nums:
    #         factional, integer = math.modf(math.log(x, multiplier))  # get the factional/integer part
    #         p1.append(int(integer))
    #         p2.append(factional)
    #     n = len(nums)
    #     muls = [0] * n
    #     # sort with idx 
    #     _idx = []
    #     for i, (x,integer) in enumerate(zip(nums, p1)):
    #         _idx.append((x, i, integer))
    #     _idx.sort()
    #     # 构造一个台阶
    #     _heights = Counter((i[2] for i in _idx))
    #     steps = sorted(_heights.items())
    #     acc_w = 0
    #     flag = False
    #     for i in range(len(steps)-1):
    #         h,w = steps[i]
    #         hn = steps[i+1][0]
    #         if (acc_w+w) * (hn-h) >= k:
    #             flag = True
    #             _h, r = divmod(k, acc_w+w)
    #             height = h + _h
    #             _idx2 = []
    #             for x,idx,integer in _idx:
    #                 if integer <= height:
    #                     muls[idx] = height - integer
    #                     _idx2.append((p2[idx], idx))
    #             _idx2.sort()
    #             for _,idx in _idx2[:r]:
    #                 muls[idx] += 1
    #             break
    #         else:
    #             acc_w += w
    #             k -= (acc_w) * (hn-h)
    #     if not flag:
    #         _h, r = divmod(k, n)
    #         max_h = _idx[-1][-1]
    #         for idx,h in enumerate(p1):
    #             muls[idx] = max_h - h + _h
    #         # 此时只排序小数部分
    #         _idx2 = sorted([(f,i) for i,f in enumerate(p2)])
    #         for _,idx in _idx2[:r]:
    #             muls[idx] += 1
    #     # 
    #     mod = 1_000_000_007
    #     ans = []
    #     for x,m in zip(nums, muls):
    #         ans.append(
    #             x * pow(multiplier, m, mod) % mod
    #         )
    #     return ans
    
    """ 3267. 统计近似相等数对 II #hard
对于 (i,j) 两个数字, 若对一个数字进行至多进行两次 "两个数位的交换" 操作后后数字相等, 则满足条件. 统计满足条件的数对数量.
例子: 1023 和 2310 。交换 1023 中数位 1 和 2 ，然后交换数位 0 和 3 ，得到 2310 。
限制: n 5e3; x 1e7
(错误的)分析: 对于至多两次交换, 可能形成什么情况? 如何 check(x,y) 成立?
    注意, 若两个数字有三位不一样, 则一定可以通过两次操作满足! 例如 (1,2,3) 两次之后-> (3,1,2)
    若两个数字有四位不一样, 则一定是分成两组互换操作. 例如的 (1,2,3,4) 选择 (0,1)(2,3) 互换之后 -> (2,1,4,3)
    然而, 这题的数量 n 5e3, O(n*2) 复杂度不够! 
思路1: 考虑每个x进行至多两次操作之后可以形成的所有可能! 
[ling](https://leetcode.cn/problems/count-almost-equal-pairs-ii/solutions/2892072/pai-xu-mei-ju-you-wei-hu-zuo-pythonjavac-vbg0/)
    """
    def countPairs(self, nums: List[int]) -> int:
        nums = [str(x) for x in nums]
        maxL = max(map(len, nums))
        nums = ['0' * (maxL-len(x)) + x for x in nums]
        def getAllPoss(x: str):
            ans = set([x]) # num_op = 0
            x = list(x)
            for i,j in itertools.combinations(range(maxL), 2):
                x[i],x[j] = x[j], x[i]
                ans.add(''.join(x)) # num_op = 1
                for p,q in itertools.combinations(range(maxL), 2):
                    x[p],x[q] = x[q], x[p] # num_op = 2
                    ans.add(''.join(x))
                    x[p],x[q] = x[q], x[p] # put back! 
                x[i],x[j] = x[j], x[i] # put back! 
            return ans
        cnt = Counter()
        ans = 0
        for x in nums:
            if x in cnt: ans += cnt[x]
            for a in getAllPoss(x):
                cnt[a] += 1
        return ans
    
sol = Solution()
result = [
    sol.getFinalState(nums = [2,1,3,5,6], k = 5, multiplier = 2),
    # sol.getFinalState([1], 1, 1),
    # sol.getFinalState([1,2,5],1,2),
    # sol.getFinalState([2,1,4],2,3),
    # sol.getFinalState([2,5,2,2],2,2),
    # sol.getFinalState([2,5,1,5,1,1,3,5],5,2),

    # sol.countPairs(nums = [3,12,30,17,21]),
    
    # sol.countPairs(nums = [1023,2310,2130,213]),
]
for r in result:
    print(r)
