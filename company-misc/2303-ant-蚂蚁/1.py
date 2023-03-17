""" 一个01序列, 进行k个反转操作, 求可以得到的最大数字
思路1: 尽可能将前面的数字都变成1, 如果有多余的操作就吧末尾变成0
 """

s = list(map(int, input().strip()))
k = int(input())

for i,x in enumerate(s):
    if x==0 and k>0:
        s[i] = 1; k-=1
if k%2==1:
    s[-1] = 0
print("".join(map(str, s)))

