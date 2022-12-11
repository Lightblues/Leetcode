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
https://leetcode.cn/contest/weekly-contest-323
进前百了: https://leetcode.cn/contest/weekly-contest-323/ranking/

@2022 """
class Solution:
    """ 6257. 删除每行中的最大值 #easy 模拟 """
    def deleteGreatestValue(self, grid: List[List[int]]) -> int:
        m,n = len(grid),len(grid[0])
        for i in range(m):
            grid[i].sort()
        ans = 0
        for j in range(n):
            ans += max(grid[i][j] for i in range(m))
        return ans
    
    """ 6258. 数组中最长的方波 #medium 类似「两数之和」 """
    def longestSquareStreak(self, nums: List[int]) -> int:
        nums.sort()
        num2max = defaultdict(lambda: 0)
        for num in nums:
            if sqrt(num).is_integer():
                num2max[num] = num2max[int(sqrt(num))] + 1
            else:
                num2max[num] = 1
        mx = max(num2max.values())
        return mx if mx > 1 else -1


    """ 6260. 矩阵查询可获得的最大分数 #hard
给定一个 grid, 对于k次查询, 每次需要返回在 queres[i] 的限制范围内, 可以到达的点的数量. 限制: 节点数量 N 1e5
思路1: 每次在threshold限制的情况下进行 #BFS. 如何降低复杂度? 对于threshold排序之后分步进行BFS, 这样每个节点访问一次, 复杂度 O(N)
    细节: 如何避免重复访问? 记录访问过的节点, 可以直接在原 grid上修改. 
"""
    def maxPoints(self, grid: List[List[int]], queries: List[int]) -> List[int]:
        m,n = len(grid),len(grid[0])
        keys = sorted(queries)  # 从小到大排序
        ans = {}
        dirs = [(0,1),(0,-1),(1,0),(-1,0)]
        # 待访问的节点. 根据val进行排序 (heapq)
        q = [(grid[0][0], 0, 0)]
        grid[0][0] = inf    # 标记已访问
        acc = 0
        def bfs(th: int):
            """ 根据th进行BFS """
            nonlocal acc, q
            while q and q[0][0] < th:
                v,x,y = heapq.heappop(q)
                acc += 1
                # grid[x][y] = inf
                # 拓展节点, 加入待访问队列
                for dx,dy in dirs:
                    nx,ny = x+dx,y+dy
                    if 0<=nx<m and 0<=ny<n and grid[nx][ny] < inf:
                        heapq.heappush(q, (grid[nx][ny], nx, ny))
                        # 注意应该在这里标记, 如果在上面标记会导致重复访问
                        grid[nx][ny] = inf  # 标记已访问
            return acc
        # 依次以查询的threshold进行BFS
        for k in keys:
            ans[k] = bfs(k)
        return [ans[k] for k in queries]
        
""" 6259. 设计内存分配器 #medium 给定一个指定大小的内存. 要求实现 1) allocate(int size, int mID) 找到大小为size的连续空闲空间, 设置为mID 2) free(int mID) 将所有 mID的空间释放 (注意可能有非连续的两个 allocate有相同的mID).
限制: 1 <= n, size, mID <= 1000, 查询次数 <= 1000
思路1: 用一个 freeMems={start: freeSize} 记录空闲空间; allocated={mID: [start,len]} 记录已分配的空间
    如何分配? 根据 freeMems 排序, 找到第一个满足 freeSize >= size 的空间, 将其分配给mID, 并更新 freeMems
    如何释放? 关键是如何合并空闲空间. 
        下面实现了一个 merge_frees(self) 暴力遍历整个 freeMems, 将所有相邻的空闲空间合并. 
"""
class Allocator:
    def __init__(self, n: int):
        self.n = n
        self.freeMems = {0: n}
        self.allocated = defaultdict(list)

    def allocate(self, size: int, mID: int) -> int:
        for s in sorted(self.freeMems.keys()):
            if self.freeMems[s] >= size:
                self.allocated[mID].append((s, size))
                if self.freeMems[s] > size:
                    self.freeMems[s+size] = self.freeMems[s] - size
                del self.freeMems[s]
                return s
        return -1

    def free(self, mID: int) -> int:
        acc = 0
        for s, size in self.allocated[mID]:
            self.freeMems[s] = size
            acc += size
        del self.allocated[mID]
        self.merge_frees()
        return acc

    def merge_frees(self):
        toDel = []
        for s in sorted(self.freeMems.keys(), reverse=True):
            nxt = s + self.freeMems[s]
            if nxt in self.freeMems:
                self.freeMems[s] += self.freeMems[nxt]
                toDel.append(nxt)
        for s in toDel:
            del self.freeMems[s]
    
sol = Solution()
result = [
    # sol.deleteGreatestValue(grid = [[1,2,4],[3,3,1]]),
    # sol.longestSquareStreak(nums = [4,3,6,16,8,2]),
    # sol.longestSquareStreak(nums = [2,3,5,6,7]),
#     testClass("""["Allocator", "allocate", "allocate", "allocate", "free", "allocate", "allocate", "allocate", "free", "allocate", "free"]
# [[10], [1, 1], [1, 2], [1, 3], [2], [3, 4], [1, 1], [1, 1], [1], [10, 2], [7]]"""),
    sol.maxPoints(grid = [[1,2,3],[2,5,7],[3,5,1]], queries = [5,6,2]),
    sol.maxPoints(grid = [[5,2,1],[1,1,2]], queries = [3]),
]
for r in result:
    print(r)
