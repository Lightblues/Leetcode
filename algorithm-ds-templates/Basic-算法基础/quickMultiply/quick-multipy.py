""" 
from [here](https://leetcode.cn/circle/article/8uRHgu/)
"""
def fpowx(x, n):
    """ 快速幂 x^n. 当然也可以像下面的 fmulti一样加一个mod.
    Python中自带的 pow 函数就是快速幂 """
    res = 1
    while n:
        if n & 1:
            res = res * x
        # compute x^2 x^4 x^8
        x *= x
        n >>= 1
    return res

def fmulti(m, n, mod=10 ** 9 + 7):
    """ 大数字乘法, 防止溢出 (计算过程取模). 例如 x*14 = x*8 + x*4 + x*2 """
    res = 0
    while n:
        if n & 1:
            res += m
        m = (m + m) % mod
        res %= mod
        n >>= 1
    return res


def matrix_multiply(matrix_a, matrix_b):
    """ 按照基本公式计算 A*B """
    n_row = len(matrix_a)
    n_col = len(matrix_b[0])
    n_tmp = len(matrix_a[0])
    matrix_c = [[0 for _ in range(n_col)] for _ in range(n_row)]
    for i in range(n_row):
        for j in range(n_col):
            for k in range(n_tmp):
                matrix_c[i][j] += matrix_a[i][k] * matrix_b[k][j]
    return matrix_c

def get_unit_matrix(n):
    # matrix I 生成单位矩阵
    unit_matrix = [[0 for _ in range(n)] for _ in range(n)]
    for _ in range(n):
        unit_matrix[_][_] = 1
    return unit_matrix
def quick_matrix_pow(matrix_a, n):
    """ 矩阵快速幂 A^n. 例如 A^9 = A^8 * A * I
    """
    l = len(matrix_a)
    res = get_unit_matrix(l)
    while n:
        if n & 1:
            # 调用矩阵乘法
            res = matrix_multiply(res, matrix_a)
        matrix_a = matrix_multiply(matrix_a, matrix_a)
        n >>= 1
    return res


""" 应用题: 疫情爆发, 第一天x个病人, 第二天y个病人, 病人在两天后有传染性, 所以第三天 x+y, 求第N天有多少个病人, 结果需要对10^9 +7 取模
提示: 递推公式满足Fibonacci公式: `F(n) = F(n-1) + F(n-2)`
思路1: #递推 计算. 据说爆栈了.
思路2: 采用 #矩阵 #快速幂
    显然, 设前两天的人数为 A = [f(n-1), f(n-2)]', 则更新有的今天昨天的人数为 A' = [f(n), f(n-1)] = X * A, 其中X为矩阵 [[1,1], [1,0]].
    因此, 若前两天人数为 Base = [x,y]', 则第n天的人数为 A^(n-2) * Base 的第一行元素.
 """
from functools import lru_cache
@lru_cache(None)
def fibonacci(x, y, n):
    # 思路1
  if n == 1:
    return x
  if n == 2:
    return y
  return fibonacci(x, y, n - 1) + fibonacci(x, y, n - 2)

def get_Fib_n(i, j, n):
    # 思路2
    if n == 0:
        return i
    elif n == 1:
        return j
    else:
        a = [[1, 1], [1, 0]]
        base = [[j], [i]]
        Fib_n = matrix_multiply(quick_matrix_pow(a, n - 2), base)
        return Fib_n[0][0]

