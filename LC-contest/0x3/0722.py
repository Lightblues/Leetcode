""" 
D2. Remove the Substring (hard version)
https://codeforces.com/problemset/problem/1203/D2

输入两个字符串 s 和 t，长度均不超过 2e5，且由小写字母组成。保证 t 是 s 的子序列。
请你从 s 中删除一个最长的子串，使得 t 仍然是剩下的 s' 的子序列。
输出这个最长子串的长度。

原题的样例不是很好，我这里造一个
输入
axxxbxc
abc
输出
3
解释：删除子串 xxx 后，s'=abxc，abc 是 s' 的子序列。

思路: 分别从两侧匹配, 对应的相邻字符之间距离相减即为可能的最大距离.
"""

s = input()
t = input()
n = len(s); l = len(t)

iLeft = [0] * l
idx = 0; i=0
while idx<l:
    if s[i]==t[idx]:
        iLeft[idx] = i
        idx += 1
    i += 1
iRight = [0] * l
idx = l-1; i=n-1
while idx>=0:
    if s[i]==t[idx]:
        iRight[idx] = i
        idx -= 1
    i -= 1

ans = max(iRight[0], n-iLeft[l-1]-1)
for i in range(1, l):
    ans = max(ans, iRight[i]-iLeft[i-1]-1)
print(ans)