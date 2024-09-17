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
https://leetcode.cn/contest/weekly-contest-399
Easonsi @2023 """
class Solution:
    """ 3162. 优质数对的总数 I """
    def numberOfPairs(self, nums1: List[int], nums2: List[int], k: int) -> int:
        n,m = len(nums1), len(nums2)
        ans = 0
        for x in nums1:
            for y in nums2:
                if x % (y*k) == 0:
                    ans += 1
        return ans

    """ 3163. 压缩字符串 III """
    def compressedString(self, word: str) -> str:
        ans = ""
        pre = ""; cnt = 0
        for c in word + " ":
            if c == pre:
                cnt += 1
                if cnt > 9:
                    ans += "9" + pre
                    cnt -= 9
            else:
                if pre:
                    ans += str(cnt) + pre
                pre = c
                cnt = 1
        return ans
    
    """ 3164. 优质数对的总数 II #medium 有两个数组 nums1 和 nums2, 问有多少idx对 (i,j), 满足 nums1[i] % (nums2[j] * k) == 0
限制: n 1e5; x 1e6
[ling](https://leetcode.cn/problems/find-the-number-of-good-pairs-ii/solutions/2790631/tong-ji-yin-zi-ge-shu-pythonjavacgo-by-e-bl3o/)
    """
    def numberOfPairs(self, nums1: List[int], nums2: List[int], k: int) -> int:
        n,m = len(nums1), len(nums2)
        ans = 0
    
    

    
sol = Solution()
result = [
    sol.numberOfPairs(nums1 = [1,3,4], nums2 = [1,3,4], k = 1),
    # sol.compressedString(word = "aaaaaaaaaaaaaabb"),
]
for r in result:
    print(r)
