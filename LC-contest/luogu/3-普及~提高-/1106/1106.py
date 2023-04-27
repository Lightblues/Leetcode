""" P1106 删数问题
给定一个正整数, 删去其中的k位, 要求结果最小.
约束: 位数不超过 250
思路1: #单调栈
    从左往右遍历, 维护一个单调递增栈即可.
    注意: 本题允许数字有前导零, 例如 20018 2 的答案为 1.
"""

nums = list(map(int, input().strip()))
n = len(nums)
k = int(input())
s = []
for num in nums:
    while s and s[-1]>num and k:
        # if num==0 and len(s)==1: break
        s.pop()
        k -= 1
    s.append(num)
# 当k==0时, s[:-0] = []
s = s[:-k] if k else s
# 注意到转一下int
# 用例: 20018 2, 结果为1; 也即允许出现前导0
print(int("".join(map(str, s))))