""" 元素乘积
有三个数组, 问有多少下标对 (i,j,k), 使得它们元素的乘积在 [L,R] 返回内

限制: 三个数组的长度分别为 n,m,k. 其中 n,m 1e3; k 1e5
元素范围 1e6; l,r 1e18
思路1: #滑动窗口 a,b 所有组合的数字范围最后 1e6; 然后对于得到的数组 d 和 c 进行匹配, 双指针
 """

n,m,k = map(int, input().strip().split())
a = list(map(int, input().strip().split()))
b = list(map(int, input().strip().split()))
c = list(map(int, input().strip().split()))
L,R = map(int, input().strip().split())

d = [i*j for i in a for j in b]
d.sort(reverse=True)
c.sort()
# c += [float('inf')]
l=r=0
ans = 0
for x in d:
    while l<k and x*c[l]<L:
        l+=1
    while r<k and x*c[r]<=R:
        r+=1
    ans += r-l
print(ans)


