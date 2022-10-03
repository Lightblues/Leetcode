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
https://leetcode-cn.com/contest/biweekly-contest-88

T1 有点坑, 一开始WA了一次; T3异或的题目还是反应有点慢; T4需要进行问题的转化, 不能一开始被题目的样子很难而吓到, 直接上转化之后就比较简单了.

@2022 """
class Solution:
    """ 6212. 删除字符使频率相同 #easy 给定一个word, 判断能否删除一个字符后, 剩余字符的频率相同. 限制: n 100
思路1: 数据量比较小, 直接 #暴力
"""
    def equalFrequency(self, word: str) -> bool:
        # 尝试求解出来, 但 #WA 了还没调.
        cnt = Counter(word)
        values = sorted(cnt.values())
        if len(values) == 1: return False
        for i in range(1, len(values)-1):
            if values[i] != values[i-1]: return False
        if values[-1] != values[0]+1: return False
        return True
    def equalFrequency(self, word: str) -> bool:
        # 暴力
        n = len(word)
        for i in range(n):
            ww = word[:i] + word[i+1:]
            if len(set(Counter(ww).values())) == 1: return True
        return False
    
    """ 6213. 所有数对的异或和 #medium #题型 给定两个数组, 要求「所有数对的异或和」. 也即两两异或得到 mn 个数字, 再求异或. 限制: n,m 10^5
思路1: 注意到 #异或 的性质: `(a^b) ^ (a^c) = b^c`. 因此, 对于数组中的某一个数字而言, 它是否被保留, 仅取决于另一个数组的长度是否为偶数.
"""
    def xorAllNums(self, nums1: List[int], nums2: List[int]) -> int:
        m,n = len(nums1), len(nums2)
        ans = 0
        if m%2: ans ^= reduce(xor, nums2)
        if n%2: ans ^= reduce(xor, nums1)
        return ans
    
    """ 6198. 满足不等式的数对数目 #hard 给定两个长度都为 n 的数组, 并给定一个整数diff. 要求统计 i<j 的数量, 满足 `nums1[i]-nums1[j] <= nums2[i]-nums2[j] + diff`
限制: n 1e5; 元素大小 +/- 1e4.
思路1: #转换. 令 arr = nums1-nums2, 则原条件等价于, `arr[i]-arr[j] <= diff`. 
    则我们遍历一遍arr, 对于每个元素x, 其作为i需要匹配的j要求 arr[j] >= x-diff. 是一个 `[x-diff, )` 区间
    因此, 对于后续的元素, 我们如何计算其作为j进行的合法匹配? 我们将此前的区间进行排序, 用二分法进行查找.
        由于需要插入操作, 利用 #SortedList 存储.
    复杂度: O(n logn).
"""
    def numberOfPairs(self, nums1: List[int], nums2: List[int], diff: int) -> int:
        from sortedcontainers import SortedList
        arr = [i-j for i,j in zip(nums1, nums2)]
        bars = SortedList()
        ans = 0
        for a in arr:
            idx = bars.bisect_right(a)
            ans += idx
            bars.add(a-diff)
        return ans
        
        
        
""" 6197. 最长上传前缀 #medium #模拟 """
class LUPrefix:

    def __init__(self, n: int):
        self.n = n
        self.uploaded = [0] * n
        self.mxpre = 0

    def upload(self, video: int) -> None:
        self.uploaded[video-1] = 1
        while self.mxpre < self.n and self.uploaded[self.mxpre]:
            self.mxpre += 1

    def longest(self) -> int:
        return self.mxpre
    
sol = Solution()
result = [
    # sol.equalFrequency("xyyz"),
    # sol.equalFrequency("aabb"),
    # sol.equalFrequency("abc"),
#     testClass("""["LUPrefix", "upload", "longest", "upload", "longest", "upload", "longest"]
# [[4], [3], [], [1], [], [2], []]""")
    # sol.xorAllNums(nums1 = [2,1,3], nums2 = [10,2,5,0]),
    # sol.xorAllNums(nums1 = [1,2], nums2 = [3,4]),
    sol.numberOfPairs(nums1 = [3,2,5], nums2 = [2,2,1], diff = 1),
    sol.numberOfPairs(nums1 = [3,-1], nums2 = [-2,2], diff = -1),
]
for r in result:
    print(r)
