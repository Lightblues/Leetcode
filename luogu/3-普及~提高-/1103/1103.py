""" P1103 书本整理 #逆向
基本题型就是, 给定一个长度为n的序列, 从中抽去K个元素, 要求所得结果的「不整齐度」最小, 这里分数的定义为, 相邻元素的差的绝对值之和.
限制: K<n<100
提示: 感觉像是DP的题, 但是「正向」考虑每次抽去一本书, 递推关系比较难得到; 此时, 「逆向」考虑按照顺序放置 n-K 本书, 累加score更为简单.
思路1: #逆向
    `f[i][j]` 表示从前i本中选取j本, 并且第i本一定被选择时的最小分数, 需要满足 `i>=j` 其中i从1开始计数
    递推: `f[i][j] = min{f[k][j-1] + score(k, i)}` 这里枚举的k表示从前k本中取 j-1 本, 并且其中最后的是第k本; score表示 (k,i) 两本书相邻的分数 `abs(weight[k]-weight[i])`
        显然需要满足 `k>=j-1`, 这里的k也是从1开始
    答案: `min{f[...][N-K]}`
    复杂度: 如果不会与上面的min操作进行优化, 则复杂度为 `O((n-K)^2*n)`. 在计算的时候维护一个 (k,minScore) 元组的话, 可以进一步优化到 `O((n-K)*n)` 级别; 不过一开始写的 v0 没有算明白下标错了 后面用了naive的方式直接过.
    这题需要注意下标防止越界和出错.
总结: **对于这种递推关系比较复杂的 #DP 题, 可以在纸上画出依赖关系, 推导出递推公式 (注意下标)**; 而不知一上来就写代码, 很容易乱掉!
"""
n, K = map(int, input().split())
books = []
for _ in range(n):
    books.append(list(map(int, input().split())))
books.sort()
weights = [b[1] for b in books]
def v0():
    # 尝试简化, 太乱了, WA
    f = [[0]*(n-K+1) for _ in range(n)]
    for j in range(1, n-K+1):
        # f[j][j] = f[j-1][j-1] + abs(weights[j-1]-weights[j-2]) if j>1 else 0
        k, mi = j-1, f[j-1][j-1]
        for i in range(j, n):
            f[i][j] = f[k][j-1] + abs(weights[i]-weights[k])
            if f[i][j-1] < mi:
                mi = f[i][j-1]
                k = i
    print(
        min(f[i][n-K-1] for i in range(n-K-1,n))
    )

# 终止: 选择 n-K 本书
f = [[float('inf')]*(n-K+1) for _ in range(n+1)]
# 依次选择 1,2,...,n-K 本书
for j in range(1, n-K+1):
    # 从前 i本中选择, i的取值范围为 [j...n]
    for i in range(j, n+1):
        # 初始化: f[j][j] 表示对于前j本书全部选择. 注意weights[i]是从0开始计数的, 另外有选择第一本书时的边界条件
        f[i][j] = f[i-1][j-1] + abs(weights[i-1]-weights[i-2]) if j>1 else 0
        for k in range(j-1, i):
            f[i][j] = min(f[i][j], f[k][j-1] + abs(weights[i-1]-weights[k-1]))
print(
    min(f[i][n-K] for i in range(1, n+1))
)