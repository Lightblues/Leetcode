from easonsi.util.leetcode import *

def testClass(inputs):
    # 用于测试 LeetCode 的类输入
    s_res = [None] # 第一个初始化类, 一般没有返回
    methods, args = [eval(l) for l in inputs.split('\n')]
    class_name = eval(methods[0])(*args[0])
    for method_name, arg in list(zip(methods, args))[1:]:
        r = (getattr(class_name, method_name)(*arg))
        s_res.append(r)
    return s_res

""" 
https://leetcode.cn/contest/weekly-contest-345


Easonsi @2023 """
class Solution:
    """ 2682. 找出转圈游戏输家 """
    def circularGameLosers(self, n: int, k: int) -> List[int]:
        i = 0
        s = set([i])
        for ii in range(1,n+1):
            i = (i+ii*k) % n
            if i in s: break
            s.add(i)
        ans = [i for i in range(n) if i not in s]
        return [i+1 for i in ans]
    
    """ 2683. 相邻值的按位异或 #medium #数学 将原0/1数组 original 根据「相邻两个元素xor」的变换 得到结果 derived, 现在给定derived判断是否有对应的原数组存在
思路1: #数学
    猜derived的特点是1的个数为偶数!
    正确的, 因为在0/1场景下, xor的结果就是两个元素之和的奇偶性!
    在「相邻两个元素xor」的变换下, 每个元素都被用到了两次, 则奇偶性必然为偶!
    容易想到, 对于一个给定的 derived 是可以完成构造的
[灵神](https://leetcode.cn/problems/neighboring-bitwise-xor/solution/tui-gong-shi-by-endlesscheng-90t5/)
    """
    def doesValidArrayExist(self, derived: List[int]) -> bool:
        return sum(derived)%2==0
    
    """ 2684. 矩阵中移动的最大次数 #medium 
代码冗长, 见
    [灵神](https://leetcode.cn/problems/maximum-number-of-moves-in-a-grid/solution/cong-ji-yi-hua-sou-suo-dao-di-tui-by-end-pgq3/)
    """
    def maxMoves(self, grid: List[List[int]]) -> int:
        m,n = len(grid),len(grid[0])
        st = [0] * m
        ans = 0
        for j in range(1,n):
            nst = [0] * m
            for i in range(m):
                a = 0
                for ii in range(i-1,i+2):
                    if 0<=ii<m and grid[i][j]>grid[ii][j-1]:
                        if j==1 or (j>1 and st[ii]>0):
                            a = max(a, st[ii]+1)
                nst[i] = a
            st = nst
            nans = max(st)
            if nans==0: break
            ans = max(ans , nans)
        return ans
    
    """ 2685. 统计完全连通分量的数量 #medium #图论 #并查集 
统计图中, 完全连通分量的数量, 单独一个节点也算.
思路1: #并查集
思路2: 直接用 #DFS 统计边的数量
    注意到, 若为完全连通, 该部分节点和边的数量满足 e == v * (v - 1)
    [灵神](https://leetcode.cn/problems/count-the-number-of-complete-components/solution/dfs-qiu-mei-ge-lian-tong-kuai-de-dian-sh-opg4/)
    """
    def countCompleteComponents(self, n: int, edges: List[List[int]]) -> int:
        degree = [1] * n
        fa = [i for i in range(n)]
        def find(x):
            if fa[x]!=x: fa[x] = find(fa[x])
            return fa[x]
        def merge(x,y):
            x,y = find(x),find(y)
            if x==y: return False
            fa[x] = y
            return True
        for x,y in edges:
            degree[x] += 1
            degree[y] += 1
            merge(x,y)
        
        cls2is = defaultdict(list)
        # for i,f in enumerate(fa):
        #     cls2is[f].append(i)
        for i in range(n):
            cls2is[find(i)].append(i)
        
        ans = 0
        for c,ii in cls2is.items():
            flag = True
            for i in ii:
                if degree[i]!=len(ii):
                    flag = False
                    break
            ans += flag
        return ans
        
    
sol = Solution()
result = [
    # sol.circularGameLosers(n = 5, k = 2),
    sol.countCompleteComponents(n = 6, edges = [[0,1],[0,2],[1,2],[3,4]]),
    sol.countCompleteComponents(n = 6, edges = [[0,1],[0,2],[1,2],[3,4],[3,5]]),
]
for r in result:
    print(r)
