"""
给你一个字符串 s 、一个字符串 t 。返回 s 中涵盖 t 所有字符的最小子串。如果 s 中不存在涵盖 t 所有字符的子串，则返回空字符串 "" 。
注意：如果 s 中存在这样的子串，我们保证它是唯一的答案。
s 和 t 由英文字母组成

输入：s = "ADOBECODEBANC", t = "ABC"
输出："BANC"

输入：s = "a", t = "a"
输出："a"

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/minimum-window-substring
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""
class Solution:
    """
    理解错题意了
    下面的解法中，我还以为只要求 t 中重复字符出现一次即可
    """
    def minWindow_try(self, s: str, t: str) -> str:
        c2bin = lambda c: ord(c) - ord('A')
        from collections import defaultdict
        # def s2bin(string):
        #     binmask = 0
        #     for c in string:
        #         binmask |= 1<<c2bin(c)
        #     return binmask
        # tbin = s2bin(t)
        # left = len(set(t))
        # right = len(s)

        s_bins = [c2bin(c) for c in s]
        t_bins = [c2bin(c) for c in t]
        n = len(s)
        target = set(t_bins)

        def search(k):
            # 判断字符串 s 中是否有满足条件的 k 长子串
            now = defaultdict(int)
            for b in s_bins[:k]:
                now[b] += 1
            diff = target - set(now.keys()) # 不满足的元素
            if len(diff)==0:
                return 0
            for i in range(k, n):
                now[s_bins[i-k]] -= 1
                if s_bins[i-k] in target and now[s_bins[i-k]] == 0:
                    diff.add(s_bins[i-k])
                now[s_bins[i]] += 1
                if s_bins[i] in target and now[s_bins[i]] == 1:
                    diff.remove(s_bins[i])
                if len(diff) == 0:
                    return i-k+1
            return -1

        left = len(target)-1
        right = n
        # 保持 right 为搜索成功的 k 再加一
        # 保持 left 为搜索失败的k
        # 但这时要注意，计算的 mid 应该是 left right 中靠右的
        while left != right:
            mid = left + (right-left)//2
            if (right-left) % 2:
                mid += 1
            res = search(mid)
            if res == -1: # 搜索失败
                left = mid
            else:
                right = mid - 1

        if right == n:
            return ''
        k = right + 1
        res = search(k)
        return s[res: res+k]


    """
    自己写的，基于二分查找的思路
    """
    def minWindow(self, s: str, t: str) -> str:
        if len(s) < len(t):
            return ''

        from collections import Counter
        t_dict = Counter(t)

        def search(k):
            # 检查是否
            keys = t_dict.keys()
            start = [c for c in s[:k] if c in keys]
            now = dict(t_dict)
            for c in start:
                now[c] -= 1
            def test():
                return all([v<=0 for v in now.values()])
            if test():
                return 0
            for i in range(k, len(s)):
                if s[i] in keys:
                    now[s[i]] -= 1
                if s[i-k] in keys:
                    now[s[i-k]] += 1
                if test():
                    return i-k+1
            return -1

        # 二分搜索，和上面一样
        left, right = len(t)-1, len(s)
        while left != right:
            mid = left + (right-left)//2
            if (right-left) % 2:
                mid += 1
            res = search(mid)
            if res == -1:
                left = mid
            else:
                right = mid - 1
        if right == len(s):
            return ''
        k = right + 1
        res = search(k)
        return s[res: res+k]


    """
    滑动窗口
    """
    def minWindow2(self, s: str, t: str) -> str:

        from collections import Counter
        target = Counter(t)
        keys = target.keys()
        now = dict(target)
        def check():
            return all([v<=0 for v in now.values()])

        l = 0
        r = -1
        ansLen = float('inf')
        ansL, ansR = -1, -1
        while r < len(s)-1:
            r += 1
            if s[r] in keys:
                now[s[r]] -= 1

            while check() and l<=r:
                if r-l+1<ansLen:
                    ansLen = r-l+1
                    ansL = l
                if s[l] in keys:
                    now[s[l]] += 1
                l += 1
        if ansL == -1:
            return ""
        else:
            return s[ansL: ansL+ansLen]


s = "ADOBECODEBANC"; t = "ABC"
# s = 'a'; t='aa'
# s = "ab"; t="aaab"
print(Solution().minWindow2(s, t))
