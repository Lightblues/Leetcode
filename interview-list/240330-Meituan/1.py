""" 
441 1 -20
# 153 134 154
"""

k,x,y = map(int, input().split())
a = (k+x-y)//3
res = [a-x,a+y,a]
print(" ".join(map(str, res)))