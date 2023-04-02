""" 
对于一个元素范围 [1,1e4] 的数组, 每次操作将一个数字替换为0, 问至少多少次可以使得数组递增. 
限制: 查询次数 q 1e3; n 1e4
思路1: 
    注意到, 对 a[i]>a[i+1], 则 a[i] 必然要变为0!
    维护一个动态的前缀set表明要变为0的数字. 在顺序遍历的过程中记录前缀区间. 
"""
def f(arr):
    s = set()
    n = len(arr)
    pre = -1
    for i in range(n-1):
        if arr[i+1] in s: 
            arr[i+1] = 0 
        if arr[i]>arr[i+1]:
            for j in range(pre+1, i+1):
                s.add(arr[j])
            pre = i
    return len(s) if 0 not in s else len(s)-1

q = int(input())
for _ in range(q):
    n = int(input())
    arr = list(map(int, input().split()))
    ans = f(arr)
    print(ans)


