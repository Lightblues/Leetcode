""" 
对数组求和, 可以改变其中一个数字的符号, 但是前缀不能是负数. 求最大和
前缀和, 求最大可以减掉的数字
"""
n = int(input())
arr = list(map(int, input().split()))
s = sum(arr)
mx = -1
acc = 0
for i,x in enumerate(arr):
    if x<=acc:
        mx = max(mx, x)
    acc += x
if mx==-1:
    print(-1)
else:
    print(s - 2*mx)
