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
https://leetcode-cn.com/contest/biweekly-contest-123
https://leetcode.cn/circle/discuss/nZJeLH/
找回状态! T4 排序有点意思
Easonsi @2023 """
class Solution:
    """ 3024. 三角形类型 """
    def triangleType(self, nums: List[int]) -> str:
        nums.sort()
        if nums[0]+nums[1] <= nums[2]:
             return 'none'
        if len(set(nums)) == 1:
            return 'equilateral'
        elif len(set(nums)) == 2:
            return 'isosceles'
        else:
            return 'scalene'
    
    """ 3025. 人员站位的方案数 I 在二位平面上有一组点, 问有多少个pair, 使得以 a=(x1,y1), b=(x2,y2) 分别作为左上角和右下角的矩阵内没有其他的点 (可以退化成线段)
限制: n 50
    """
    def numberOfPairs(self, points: List[List[int]]) -> int:
        pass
    
    """ 3026. 最大好子数组和 """
    def maximumSubarraySum(self, nums: List[int], k: int) -> int:
        acc = list(accumulate(nums, initial=0))
        x2idx = {}
        mx_sum = -inf
        for i,x in enumerate(nums):
            if x-k in x2idx:
                mx_sum = max(mx_sum, acc[i+1]-acc[x2idx[x-k]])
            if x+k in x2idx:
                mx_sum = max(mx_sum, acc[i+1]-acc[x2idx[x+k]])
            
            # NOTE: 注意 x in x2idx 的情况!
            if x not in x2idx:
                x2idx[x] = i
            else:
                if acc[i] - acc[x2idx[x]] < 0:      # 注意这里 i和此前的位置总会取到一个
                    x2idx[x] = i
        return mx_sum if mx_sum != -inf else 0
    
    """ 3027. 人员站位的方案数 II #hard
限制: n 1e3; x,y 1e9
思路1: 比较复杂的遍历模拟
    对于x轴进行离散化, 也即出现在不同x值的点, 按照大小关系变为 0,1,2,...
    考虑 x=0 轴上, 从上往下的那些点
        在这个轴当前最高点为 y00, 下面的一个点为 y01. 考虑哪些点可以和 (x=0,y00) 构成符合要求的矩阵?
        在 x=1 轴上, 满足 y01<y<=y00 的最高的那个点, 计作 y1.
        在 x=2 轴上, 满足 y1<y<=y00 的最高的那个点, 计作 y2, ...
    复杂度: 预处理离散化+排序, O(nlogn). 然后从x=0开始遍历, 每次的复杂度是 O(n), 因此是 O(n^2)
思路2: 直接双指标排序!
    核心: 按照横坐标从小到大排序，横坐标相同的，按照纵坐标从大到小排序!
    然后, 固定 point[i], 对于 point[j] 进行遍历, 维护「满足要求的pair中, 最大的纵坐标」!
    复杂度: 也是 O(n^2), 但常数小太多了!
    [ling](https://leetcode.cn/problems/find-the-number-of-ways-to-place-people-ii/solutions/2630655/on2-you-ya-mei-ju-by-endlesscheng-z86d/)
    """
    def numberOfPairs(self, points: List[List[int]]) -> int:
        x2ys = defaultdict(list)
        for x,y in points:
            x2ys[x].append(y)
        ys = []
        for x in sorted(x2ys):
            ys_ = sorted(x2ys[x], reverse=True)
            ys.append(ys_)
        # 
        res = 0
        for i,yy in enumerate(ys):
            if len(yy) > 1:
                res += len(yy)-1
            # ys_ = ys[i+1:]        # NOTE: 需要 deepcopy
            ys_ = deepcopy(ys[i+1:])
            ys_to_idx = [0] * len(ys_)
            for y0, y1 in itertools.pairwise(yy + [-inf]):
                for ii in range(len(ys_)):
                    # while ys_[ii] and ys_[ii][0] > y0:
                    #     # NOTE: 这里应该 pop(0), 为了降低复杂度采用 ys_to_idx 进行记录
                    #     ys_[ii].pop()
                    # if ys_[ii]:
                    while ys_to_idx[ii] < len(ys_[ii]) and ys_[ii][ys_to_idx[ii]] > y0:
                        ys_to_idx[ii] += 1
                    if ys_to_idx[ii] < len(ys_[ii]):
                        if ys_[ii][ys_to_idx[ii]] > y1:
                            res += 1
                            y1 = ys_[ii][ys_to_idx[ii]]
                            if y1 == y0:
                                break
        return res

    def numberOfPairs(self, points: List[List[int]]) -> int:
        """ from ling """
        points.sort(key=lambda p: (p[0], -p[1]))
        ans = 0
        for i, (_, y0) in enumerate(points):
            max_y = -inf
            for (_, y) in points[i + 1:]:
                if max_y < y <= y0:
                    max_y = y
                    ans += 1
        return ans

    
sol = Solution()
result = [
    # sol.triangleType(nums = [3,4,5]),
    # sol.maximumSubarraySum(nums = [-1,3,2,4,5], k = 3),
    # sol.maximumSubarraySum([3,3,2], 1),

    sol.numberOfPairs(points = [[1,1],[2,2],[3,3]]),
    sol.numberOfPairs(points = [[6,2],[4,4],[2,6]]),
    sol.numberOfPairs(points = [[3,1],[1,3],[1,1]]),
    sol.numberOfPairs([[2,1],[4,6],[4,1]]),
    sol.numberOfPairs([[5,2],[4,3],[5,5],[0,4]]),
]
for r in result:
    print(r)
