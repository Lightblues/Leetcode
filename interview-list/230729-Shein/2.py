""" 最长的没有重复元素的子串长度 返回字符串中, 最长的没有重复元素的子串长度
限制: n 1e5
"""

def lengthOfLongestSubstring(arr) -> int:
    s = set()
    l = 0
    ans = 0
    for r,x in enumerate(arr):
        if x in s:
            while arr[l] != x:
                s.remove(arr[l])
                l += 1
            l += 1
        s.add(x)
        ans = max(ans, r-l+1)
    return ans

for a in [
    "abcabcbb",
    "bbbbb",
    "pwwkew",
    "",
]:
    print(lengthOfLongestSubstring(a))

