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
https://leetcode.cn/contest/weekly-contest-176

这一期赞! T2要求实现的DS有点意思, 累乘思路巧妙. T3的贪心也需要一定的思考. T4乍一看思路清楚, 但有一些细节需要仔细推敲才有可能一遍过.

@2022 """
class Solution:
    """ 1351. 统计有序矩阵中的负数 #easy m*n 的矩阵, 每一行每一列都是「非递增」的. 问有多少个负数
进阶要求: 时间复杂度 O(m+n) 
"""
    def countNegatives(self, grid: List[List[int]]) -> int:
        m,n = len(grid), len(grid[0])
        ret = 0
        idx = n-1
        for i in range(m):
            while idx>=0 and grid[i][idx]<0:
                idx -= 1
            ret += n-1-idx
        return ret
    
    """ 1353. 最多可以参加的会议数目 #medium #题型 有一组会议在 `[start_i, end_i]` 期间召开. 你可以在任意一天参加一个会. 问最多可以参加多少个会议. 限制: n 1e5; 范围 1e5
思路1: #贪心. 顺序遍历, 若可选多个会议, 则优先选择「end 前的会议」.
    因此, 可以按照 start 排序, 然后在遍历日期的过程中, 维护可参加的会议. 每次取最早结束的会议.
    时间复杂度: O(nlogn + T logn) T 为日期范围
"""
    def maxEvents(self, events: List[List[int]]) -> int:
        mn, mx = min([e[0] for e in events]), max([e[1] for e in events])
        ret = 0
        events.sort(key=lambda x: x[0])
        ends = []
        n = len(events); idx = 0
        for d in range(mn, mx+1):
            while idx<n and events[idx][0]<=d:
                heappush(ends, events[idx][1])
                idx += 1
            #注意! 可能有过期的无法参与
            while ends and ends[0]<d:
                heappop(ends)
            if ends:
                ret += 1
                heappop(ends)
        return ret
    
    """ 1354. 多次求和构造目标数组 #hard #题型 给定一个长n的目标数组 target, 一开始初始化一个全1的长n的数组 arr. 每次执行的操作是: 选择一个下标i使得该位置元素变为 sum(arr). 问能否生成 target?
限制: n 5e4; 元素大小 1e9
https://leetcode.cn/problems/construct-target-array-with-multiple-sums/description/
例如, [9,3,5] 的生成序列为 [1, 1, 1], [1,3,1], [1,3,5], [9,3,5]
思路1: #逆序 考虑. 注意到每次生成的数字一定是在序列中最大的.
    因此, 考虑 k+1 步, 数组中最大元素位置 i, 其值为 `arr_k_1[i] = sum(arr_k)`; 减去其他元素的和, 即为 `arr_k[i] = sum(arr_k) - sum(arr_k \ i) = arr_k_1[i] - (sum(arr_k_1)-arr_k_1[i]) = 2*arr_k_1[i] - sum(arr_k_1)`
    考虑到复杂度, 可以用一个 #最大堆 维护最大元素.
    条件判断: 是否可以将所有元素变为 1
    细节: 对于 [1,10000000] 的情况, 如何加速? 需要考虑一次能够抵消几次操作.
        可以通过下面的 `ceil((mx-(-h[0]))/sum_remains)` 来计算需要减去的步数.
更具体的说明和复杂度分析见 [官答](https://leetcode.cn/problems/construct-target-array-with-multiple-sums/solutions/101214/duo-ci-qiu-he-gou-zao-mu-biao-shu-zu-by-leetcode-s/)
"""
    def isPossible(self, target: List[int]) -> bool:
        if len(target)==1: return target[0]==1
        s = sum(target)
        h = [-i for i in target]
        heapify(h)
        """ 简单的写法是下面这种, 但遇到 `[1,1000000000]` 会超时 """
        # while -h[0]>1:
        #     mx = -heappop(h)
        #     mn_new = 2*mx - s
        #     if mn_new <=0: return False
        #     s += mn_new - mx
        #     heappush(h, -mn_new)
        while -h[0]>1:
            mx = -heappop(h)
            sum_remains = s - mx    # 其他元素和
            # 重点是这里的轮次计算!
            a = ceil((mx-(-h[0]))/sum_remains)
            if a <=0: return False          # [9,9]
            mn_new = mx - a*sum_remains
            # 上面算到的 a 可能会超过 mx, 因此需要判断一下
            if mn_new <=0: return False     # [1,1,2]
            s += mn_new - mx
            heappush(h, -mn_new)
        return True
    
""" 1352. 最后 K 个数的乘积 #medium #题型 #前缀 实现一个结构, 可以 add 一个数字到列表最后; getProduct(int k) 查询最后k个数字的乘积. 题目保证了查询的k都是有效的.
限制: 操作次数 n 4e4; k 4e4
思路1: 考虑 #前缀 乘积. 特殊考虑 0 的情况
    若没有因子0, 则可以直接用前缀乘积计算.
    那么如何解决因子0的情况? 注意到, 若查询的k超过了0的位置, 则结果一定是0! 因此, 我们可以直接「重置」所记录的数组. 通过检查 k 和记录数组长度的关系, 判断乘积范围是否包括了因子0.
    见 [官答](https://leetcode.cn/problems/product-of-the-last-k-numbers/solutions/101222/zui-hou-k-ge-shu-de-cheng-ji-by-leetcode-solution/)
"""
class ProductOfNumbers:
    def __init__(self):
        self.nums = []
        self.acc = [1]

    def add(self, num: int) -> None:
        if num!=0:
            # 不是 0 的一般情况
            self.nums.append(num)
            self.acc.append(self.acc[-1]*num)
        else:
            self.nums = []
            self.acc = [1]

    def getProduct(self, k: int) -> int:
        if k>len(self.nums):
            return 0
        else:
            return self.acc[-1]//self.acc[-k-1]

    
sol = Solution()
result = [
    # sol.countNegatives(grid = [[4,3,2,-1],[3,2,1,-1],[1,1,-1,-2],[-1,-1,-2,-3]]),
#     testClass("""["ProductOfNumbers","add","add","add","add","add","getProduct","getProduct","getProduct","add","getProduct"]
# [[],[3],[0],[2],[5],[4],[2],[3],[4],[8],[2]]"""),
    # sol.maxEvents([[1,2],[2,3],[3,4]]),
    # sol.maxEvents([[1,2],[1,2],[1,6],[1,2],[1,2]]),
    sol.isPossible([9,3,5]),
    sol.isPossible([1,1,1,2]),
    sol.isPossible([2]),
    sol.isPossible([1]),
    sol.isPossible([1,1000000000]),
    sol.isPossible([9,9,9]),
]
for r in result:
    print(r)
