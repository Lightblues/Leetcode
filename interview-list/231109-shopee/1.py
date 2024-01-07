""" 找出长度为k的字符串中, 元音字母的最大数量 
s = "tryhard", k = 4
"""

vowels = "aeiou"

s, k = input().strip().split(',')
k = int(k.split('=')[1])
s = s.split('=')[1].strip().strip('"')
cnt = mx = 0
for i in range(k):
    if s[i] in vowels:
        cnt += 1
mx = cnt
for i in range(k,len(s)):
    if s[i] in vowels:
        cnt += 1
    if s[i-k] in vowels:
        cnt -= 1
    mx = max(mx, cnt)
print(mx)

