

""" 反转字符串中的大写序列
思路1: #栈
 """

s  = input().strip()
import string

st = []
ans = []
for i in s:
    if i in string.ascii_uppercase:
        st.append(i)
    else:
        while st:
            ans.append(st.pop())
        ans.append(i)
# 加两行
while st:
    ans.append(st.pop())
ans = "".join(ans)
print(ans)


