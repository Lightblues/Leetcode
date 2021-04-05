"""
实现 strStr() 函数。
给定一个 haystack 字符串和一个 needle 字符串，在 haystack 字符串中找出 needle 字符串出现的第一个位置 (从0开始)。如果不存在，则返回 -1。

输入: haystack = "hello", needle = "ll"
输出: 2

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/implement-strstr
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""

class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        L, n = len(needle), len(haystack)
        # 冗余的
        # if len(needle)==0:
        #     return 0
        for i in range(n-L+1):
            if haystack[i:i+L] == needle:
                return i
        return -1

    """
    上面用到了默认的字符串比较，相当于 O(n) 复杂度的（？）
    但从前缀还是比较就可得出结果，下面的实现用了 curr_len 记录匹配长度，从而结合两个指针可以定位开始匹配的 index
    当然直接记录还是匹配的 index，然后去线性检查是否完整匹配也行，但似乎要多一个变量；但这里的操作需要注意移动的位置（匹配失败更新 pn = pn-curr_len+1），结合图示
    """
    def strStr2(self, haystack: str, needle: str) -> int:
        L, n = len(needle), len(haystack)
        if L==0:
            return 0

        pn = 0 # pointer in haystack
        while pn < n-L+1:
            # 对齐 needle 第一个元素
            while pn<n-L+1 and haystack[pn]!=needle[0]:
                pn += 1
            # 从头开始匹配 needle，注意此时的 pn 指向的值必然为 needle 第 0 元素，也即 haystack[pn]==needle[pL]
            curr_len = 0    # 记录匹配长度
            pL = 0  # pointer in needle
            while pL<L and pn<n and haystack[pn]==needle[pL]:
                pn += 1
                pL += 1
                curr_len += 1

            if curr_len == L:   # 完整匹配
                return pn-L

            pn = pn-curr_len+1  # 否则回退到
        return -1


    """
    【思路三】利用 hash。例如选取 base=26，可将数组 [0,1,2,3] 计算 hash 值 h0=0*26^3 + 1*26^2 + 2*26^1 + 3*26^0
    向右移动变为 [1,2,3,4] ，更新公式为 h1 = (h0 - 0*26^3)*26 + 4*26^0 = h0*26 - 0*26^4 + 4*26^0
    于是更新公式为 h_{i+1} = hi*base - nums[i]*base^L + nums[i+L] 
    """
    def strStr3(self, haystack: str, needle: str) -> int:
        L, n = len(needle), len(haystack)
        if n<L:
            return -1

        a = 26      # bash value for rolling hash func
        modulus = 2**31

        h_to_int = lambda i: ord(haystack[i]) - ord('a')
        needle_to_int = lambda i: ord(needle[i]) - ord('a')

        # 计算 needle 的 ref_h 和 haystack[:n] 的 hash
        h = ref_h = 0
        for i in range(L):
            h = (h*a + h_to_int(i)) % modulus
            ref_h = (ref_h*a + needle_to_int(i)) % modulus
        if h == ref_h:
            return 0

        aL = pow(a, L, modulus)
        for start in range(1, n-L+1):
            h = (h*a - h_to_int(start-1)*aL + h_to_int(start+L-1)) % modulus
            if h==ref_h:
                return start
        return -1
# print(Solution().strStr2("hello", 'll'))
print(Solution().strStr3("hello", 'll'))