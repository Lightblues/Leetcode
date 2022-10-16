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
    """ 1413. 删除字符使频率相同 #easy 给定一个word, 判断能否删除一个字符后, 剩余字符的频率相同. 限制: n 100
思路1: 数据量比较小, 直接 #暴力
思路2: #分类 讨论. 注意到考虑完全. 复杂度 O(n)
关联: 1224. 最大相等频率 #hard
"""
    def equalFrequency(self, word: str) -> bool:
        # 暴力
        n = len(word)
        for i in range(n):
            ww = word[:i] + word[i+1:]
            if len(set(Counter(ww).values())) == 1: return True
        return False
    def equalFrequency(self, word: str) -> bool:
        # from 灵神的更优雅暴力
        for i in range(len(word)):
            cnt = Counter(word[:i] + word[i + 1:])
            same = cnt.popitem()[1]
            if all(c == same for c in cnt.values()):
                return True
        return False
    def equalFrequency(self, word: str) -> bool:
        """ 思路2: #分类 讨论. 注意到考虑完全. 复杂度 O(n)
        只有一种字符; 一个字符出现一次, 其他都相等; 其他字符出现x次, 只有一个字符出现 x+1次.
        用cnt很巧妙!!
        """
        c = sorted(Counter(word).values())
        return len(c) == 1 or \
            c[0] == 1 and len(set(c[1:])) == 1 or \
                c[-1] == c[-2] + 1 and len(set(c[:-1])) == 1


    """ 2425. 所有数对的异或和 #medium #题型 #math #xor 给定两个数组, 要求「所有数对的异或和」. 也即两两异或得到 mn 个数字, 再求异或. 限制: n,m 10^5
思路1: 注意到 #异或 的性质: `(a^b) ^ (a^c) = b^c`. 因此, 对于数组中的某一个数字而言, 它是否被保留, 仅取决于另一个数组的长度是否为偶数.
    见 [灵神](https://leetcode.cn/problems/bitwise-xor-of-all-pairings/solution/tao-lun-mei-ge-yuan-su-zai-da-an-zhong-d-uutg/)
https://leetcode.cn/problems/bitwise-xor-of-all-pairings/
"""
    def xorAllNums(self, nums1: List[int], nums2: List[int]) -> int:
        m,n = len(nums1), len(nums2)
        ans = 0
        if m%2: ans ^= reduce(xor, nums2)
        if n%2: ans ^= reduce(xor, nums1)
        return ans
    
    """ 2426. 满足不等式的数对数目 #hard 给定两个长度都为 n 的数组, 并给定一个整数diff. 要求统计 i<j 的数量, 满足 `nums1[i]-nums1[j] <= nums2[i]-nums2[j] + diff`
限制: n 1e5; 元素大小 +/- 1e4.
思路1: #转换. 令 arr = nums1-nums2, 则原条件等价于, `arr[i]-arr[j] <= diff`. 
    则我们遍历一遍arr, 对于每个元素x, 其作为i需要匹配的j要求 arr[j] >= x-diff. 是一个 `[x-diff, )` 区间
    因此, 对于后续的元素, 我们如何计算其作为j进行的合法匹配? 我们将此前的区间进行排序, 用二分法进行查找.
        由于需要插入操作, 利用 #SortedList 存储.
    复杂度: O(n logn).
思路2: 转化为 #逆序对 模型. 然后利用 #树状数组 求解
    灵神对于 `a[i] <= a[j]+diff` 的条件, 指出其本质就是「逆序对」
    解决方案:  #归并排序 或者 #树状数组
    关联: 0315. 计算右侧小于当前元素的个数 #hard
    [灵神](https://leetcode.cn/problems/number-of-pairs-satisfying-inequality/solution/by-endlesscheng-9prc/)
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
    def numberOfPairs(self, a: List[int], nums2: List[int], diff: int) -> int:
        # 思路2: 转化为 #逆序对 模型. 然后利用 #树状数组 求解
        class BIT:
            # 树状数组 模版
            def __init__(self, n):
                self.tree = [0] * n

            def add(self, x):
                while x < len(self.tree):
                    self.tree[x] += 1
                    x += x & -x

            def query(self, x):
                # 查询前缀和
                res = 0
                while x > 0:
                    res += self.tree[x]
                    x &= x - 1
                return res
    
        for i, x in enumerate(nums2):
            a[i] -= x
        b = a.copy()
        b.sort()  # 配合下面的二分，离散化

        ans = 0
        t = BIT(len(a) + 1)
        for x in a:
            ans += t.query(bisect_right(b, x + diff))
            t.add(bisect_left(b, x) + 1)
        return ans




    
    """ 1224. 最大相等频率 #hard #题型 给定一个数组, 要求找到一个最大的前缀子数组, 使得从子数组中删去一个元素后, 剩余的元素出现的频率相同. 限制: 1e5
关联: 1413. 删除字符使频率相同 #easy
思路1: #计数 #分类 讨论符合的情况 
    我们用一个字典记录出现次数的计数 cntFreq = { cnt: freq }. 表示出现cnt次的数字都有多少个. 
    考虑符合的可能情况: 四种
        len(cntFreq) = 1. 1) 只有一种数字; 2) 或者所有都只出现一次; 
        len(cntFreq) = 2. 1) 一个数字出现一次, 其他都相等; 2) 其他数字出现x次, 只有一个数字出现 x+1次.
        则上述情况都可以在 O(1) 时间check.
    因此, 遍历过程中, 维护该数组即可.
[官答](https://leetcode.cn/problems/maximum-equal-frequency/solution/zui-da-xiang-deng-pin-lu-by-leetcode-sol-5y2m/) 分类的思路更清楚一点
"""
    def maxEqualFreq(self, nums: List[int]) -> int:
        intCnt = defaultdict(int)
        cntFreq = defaultdict(int)
        ans = 1
        def check() -> bool:
            if len(cntFreq) == 1:
                c = list(cntFreq.keys())[0]
                # [1,2,3,4,5]
                if c==1: return True
                # [2,2,2,2]
                elif cntFreq[c]==1: return True
            elif len(cntFreq) == 2:
                c1,c2 = sorted(cntFreq.keys())
                # [1,2,2,2,2]
                if c1==1 and cntFreq[c1]==1: return True
                # [1,1,2,2,2]
                elif c2==c1+1 and cntFreq[c2]==1: return True
            return False
        for i, a in enumerate(nums):
            intCnt[a] += 1
            f = intCnt[a]
            # 多了一个 f, 少了一个 f-1
            cntFreq[f] += 1
            if f==1: pass
            else:
                cntFreq[f-1] -= 1
                if cntFreq[f-1]==0: cntFreq.pop(f-1)
            if check(): ans = i+1
        return ans
    
""" 2424. 最长上传前缀 #medium #模拟 """
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
    # sol.numberOfPairs(nums1 = [3,2,5], nums2 = [2,2,1], diff = 1),
    # sol.numberOfPairs(nums1 = [3,-1], nums2 = [-2,2], diff = -1),
    
    sol.maxEqualFreq(nums = [2,2,1,1,5,3,3,5]),
    sol.maxEqualFreq(nums = [1,1,1,2,2,2,3,3,3,4,4,4,5]),
    sol.maxEqualFreq([1,2]),
    sol.maxEqualFreq([1,2,3,4,5,6,7,8,9])
]
for r in result:
    print(r)
