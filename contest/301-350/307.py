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
https://leetcode.cn/contest/weekly-contest-307

灵神: https://leetcode.cn/circle/discuss/t6hE2C/view/CK3s97/
@2022 """

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    """ 6152. 赢得比赛需要的最少训练时长 """
    def minNumberOfHours(self, initialEnergy: int, initialExperience: int, energy: List[int], experience: List[int]) -> int:
        se = sum(energy)
        ans = ans = 0 if initialEnergy>se else se+1 - initialEnergy
        exp = initialExperience
        for e in experience:
            if exp > e:
                exp += e
            else:
                diff = e-exp+1
                ans += diff
                exp += diff+e
        return ans
    
    """ 6166. 最大回文数字 #medium
给定一组0-9数字, 要求从中构造最大的回文串, 不能有前缀零.
思路1: #细节 #构造
    如何得到最大回文? 尽量用到多的数字, 大的放在前面. 将一个回文数分割成 [left,mid,right] 三部分, 中间mid可能为空或者单个字符, 左右部分对称.
    注意: 由于不能有前缀零, 需要有很多细节的判断.
"""
    def largestPalindromic(self, num: str) -> str:
        cnt = collections.Counter(num)
        left = ""   
        mid = ''
        # 先考虑正数
        for i in '123456789'[::-1]:
            v = cnt[i]
            a,b = divmod(v,2)
            left += i * a
            if mid=='' and b:
                mid = i
        # 特判
        v0 = cnt['0']
        a,b = divmod(v0,2)
        if len(left) >= 1:  # 不在首位
            left += '0' * a
        # 什么情况下mid=0? 1) left 为空并且 mid 也为空, 说明此时字符串为全零; 2) left 非空, 同一般情况.
        if mid=='':
            if (left=='') or (left!='' and b):
                mid = '0'
        return left + mid + left[::-1]
    
    """ 6154. 感染二叉树需要的总时间 #medium 求二叉树上的某一节点到其他点的最大距离.
思路1: 先进行一次DFS得到父亲节点 (变成无向图). 然后就是基本的BFS
"""
    def amountOfTime(self, root: Optional[TreeNode], start: int) -> int:
        # DFS得到所有节点的father
        val2node = {}
        def f(a: TreeNode):
            val2node[a.val] = a
            if a is None: return
            if a.left:
                a.left.fa = a
                f(a.left)
            if a.right:
                a.right.fa = a
                f(a.right)
        root.fa = None
        f(root)
        # BFS计算
        root = val2node[start]
        visited = set([root])
        q = deque([(0, root)])
        mx = 0
        while q:
            dist,u = q.popleft()
            mx = max(mx, dist)
            for v in [u.fa, u.left, u.right]:
                if v is None: continue
                if v in visited: continue
                q.append((dist+1, v))
                visited.add(v)
        return mx

    """ 6155. 找出数组的第 K 大和 #hard #题型
给定一个数组, 在此数组的所有子序列的和中, 求第k大的. 
限制: 数组长度 1e5, 元素大小 +/-1e9. 重点是这里的k最大为 2000
提示: 
    显然, 最大值就是正数和. 那么, **那些次大元素如何得到呢?** 减去一些正数, 或者加上一些负数.
    假设正数和为sum是可能得到的最大值. 然后 **我们可以把nums都取绝对值**, 选取一组数字, 其和就是可能从sum中减去的结果.
思路1: 利用 #堆
    直接给结论: 1) 初始化最大堆 `(sum, 0)`, 堆元素 `(val, idx)`, 这里的第二个参数idx表示我们下一个要处理的位置, 注意此时我们一定选择了idx-1. 2) 第i次弹出最大元素, 这里的val就是第i大的和. 考虑选择idx, 或者选择idx并去掉idx-1. 将这两个新元素入堆.
    形式化问题: 「**从n个非负数中求k个最小的子序列和**」. 上面的过程就是解法. 这里的正确性来自, 1) 枚举了所有的子序列; 并且 2) 入堆的元素一定比出堆元素大. 见题解2.
    关联: 「1982. 从子集的和还原数组」
    复杂度: `O(n logn + k logk)`
思路2: #二分 查找子序列和不大于limit的数量.
    还是为了解决上面形式化的子问题. 我们可以在 [0, U] 中搜索一个值, 使得取绝对值之后的nums中子序列和不大于该值的数量刚好有 k-1 个 (因为我们要求第k个).
    因此, 可以用二分搜索. 我们需要一个函数 `count(limit)` 统计nums中小于等于limit的子序列数量. 这里的基本思想和思路1一致, 见代码. #细节. 注意, 这里最多求k个, 因此count函数的复杂度为 O(k).
    复杂度: `O(nlogn + k logU)`. 空间: count函数需要递归, 最多 `min(k,n)` 层.
思路0: 想到了提示1, 但没进一步想到提示2. 所以比较繁琐
    步骤: 从正数中找到最小的k个, 负数组合中找到绝对值最小的k个, 两两组合就是减去的最小情况.
    面临同样的子问题, 作弊用 SortedList 侥幸过了.
[灵神](https://leetcode.cn/problems/find-the-k-sum-of-an-array/solution/zhuan-huan-dui-by-endlesscheng-8yiq/)
"""
    def kSum(self, nums: List[int], k: int) -> int:
        # 思路0: 想到了提示1, 但没进一步想到提示2. 所以比较繁琐
        from sortedcontainers import SortedList
        nums.sort()
        i0 = bisect_left(nums, 0)
        negs, poss = nums[:i0], nums[i0:]
        def getMinK(arr: List[int]):
            # 给定一个整数数组 (排序), 返回最小的k个子序列和. 作弊用 sl
            if len(arr)==0: return [0]
            sl = SortedList([0,arr[0]])
            for a in arr[1:]:
                nValues = []
                for v in sl[:k]:
                    idx = sl.bisect_right(v+a)
                    if idx > k: break
                    nValues.append(v+a)
                for v in nValues: sl.add(v)
            return sl[:k]
        minPos = getMinK(poss)
        minNegs = getMinK([-i for i in negs[::-1]])
        # 一开始直接 product 超时, 还是按照 getMinK思路剪枝, 就过了
        # values = [a+b for a,b in product(minPos, minNegs)]
        # values.sort()
        values = SortedList(minPos)
        for a in minNegs[1:]:
            nValues = []
            for v in minPos:
                idx = values.bisect_right(a+v)
                if idx > k: break
                nValues.append(a+v)
            for v in nValues: values.add(v)
        return sum(poss) - values[k-1]
    def kSum(self, nums: List[int], k: int) -> int:
        # 思路1: 利用 #堆
        sum = 0
        for i, x in enumerate(nums):
            if x >= 0: sum += x     # sum 求正数和 (最大值)
            else: nums[i] = -x      # 将 nums 都变成正数
        nums.sort()
        # 「**从n个非负数中求k个最小的子序列和**」
        # (val, idx) 这里的idx表示下一个要考虑的数字的位置
        h = [(-sum, 0)]  # 取负号变成最大堆
        for _ in range(k - 1):
            s, i = heappop(h)
            if i < len(nums):
                heappush(h, (s + nums[i], i + 1))  # 保留 nums[i-1]
                if i: heappush(h, (s + nums[i] - nums[i - 1], i + 1))  # 不保留 nums[i-1]
        return -h[0][0]
    def kSum(self, nums: List[int], k: int) -> int:
        # 思路2: #二分 查找子序列和不大于limit的数量.
        sum = tot = 0   # sum 为正数和, tot 为绝对值和
        for i, x in enumerate(nums):
            if x >= 0:
                sum += x
                tot += x
            else:
                tot -= x
                nums[i] = -x
        nums.sort()

        def count(limit: int) -> int:
            # 计算nums中子序列和 <= limit的个数
            cnt = 0
            def f(i: int, s: int) -> None:
                nonlocal cnt
                # cnt >= k - 1 提前终止!!!
                if i == len(nums) or cnt >= k - 1 or s + nums[i] > limit:
                    return
                cnt += 1
                f(i + 1, s + nums[i])  # 选
                f(i + 1, s)  # 不选
            f(0, 0)
            return cnt
        # 注意是 left
        return sum - bisect_left(range(tot), k - 1, key=count)

            
        
sol = Solution()
result = [
    # sol.minNumberOfHours(initialEnergy = 5, initialExperience = 3, energy = [1,4,3,2], experience = [2,6,3,1]),
    # sol.minNumberOfHours(initialEnergy = 2, initialExperience = 4, energy = [1], experience = [3]),
    sol.largestPalindromic("44494713700"),
    sol.largestPalindromic("1155"),
    sol.largestPalindromic("000011"),
    # sol.kSum(nums = [2,4,-2], k = 5),
    # sol.kSum(nums = [1,-2,3,4,-10,12], k = 16),
    # sol.kSum([492634335,899178915,230945927], 2),
    # sol.kSum([-202224630,-918893555,540446399,116155652,733614701,661520492,758915058,-384765776,298311344,721301747,-617042302,-5769948,285542800,-208878786,-528162506,821351427,-476275800,-533770898,884834038,330712773,683263035,555154695], 1367),
    # sol.kSum([-487322177,-656480132,850198596,-291605661,-272668395,110865952,-162529283,-145886963,202657909,125667049,-282090943,120877054,-85849348,-482630078,-802177895,-574862206,374637017,804297842], 1707),
]
for r in result:
    print(r)
