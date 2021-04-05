"""
写出一个程序，接受一个由字母、数字和空格组成的字符串，和一个字母，然后输出输入字符串中该字母的出现次数。不区分大小写。

ABCabc
A

2
"""

import sys
s = sys.stdin.readline().strip()
c = sys.stdin.readline().strip()

base = ord('A')
if ord(c)<base+32:
    c2 = chr(ord(c)+32)
else:
    c2 = chr(ord(c)-32)

count = 0
for char in s:
    if char in (c, c2):
        count += 1

print(count)
