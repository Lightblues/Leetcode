""" 计算耗时
有三种微服务耗时依次为 A<=B<=C. 
每次调用若干服务, 每种最多一个 (最多7种可能 A, B, C, A+B, A+C, B+C, A+B+C); 现在给定一组调用总耗时, 找到符合要求的三元组 (A,B,C) 的数量
限制: 测试用例 T 1e2; 每次给 4~7个总耗时, 数据范围在 2e9
思路1: 
    注意到, 由于会给4~7个总耗时, 因此在所有的两辆两diff和原本的数字中, 一定包含了ABC中的某一个! 
        例如, A+B+C, A+B 相减就可以得到C
    因此, 我们至少知道ABC中一个数值, 在此基础上进行回溯! 
"""

def check(arr, x):
    if x in arr: return True
    s = sum(arr)
    if s==x: return True
    for i in arr:
        if s-i==x: return True
    return False


def f(arr:list):
    ans = set()
    def dfs(arr, idx, vals):
        nonlocal ans
        if idx==len(arr) and len(vals)==3:
            # 找到了一个解
            ans.add(tuple(sorted(vals)))
            return
        x = arr[idx]
        # 已有的数字可以构成x
        if check(vals, x):
            dfs(arr, idx+1, vals)
        if len(vals)<3:
            # 1] 直接把x装进去
            vals.append()
            dfs(arr, idx+1, vals)
            vals.pop()
            # 2] 把x拆分成两个数, 装入diff
            for v in vals:
                if v>=x: continue
                vals.append(arr[idx]-v)
                dfs(arr, idx+1, vals)
                vals.pop()
            # 3] 把x拆分成三个数. 但发现不写也是对的!
    arr.sort()
    # start 中, 表示了ABC中的某一个数字
    start = set(arr)
    n = len(arr)
    for i in range(n):
        for j in range(i+1,n):
            x,y = arr[i],arr[j]
            if y>x: start.add(y-x)
    for x in start:
        dfs(arr,0,[x])
    return len(ans)

# print(f([4, 5, 7, 8]))

T = int(input())
for i in range(T):
    n = int(input())
    arr = list(map(int,input().split()))
    # print(f"[{i}]: {f(arr)}")
    print(f(arr))
