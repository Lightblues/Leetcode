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
https://leetcode-cn.com/contest/biweekly-contest-108
https://leetcode.cn/circle/discuss/BO1c8V/

T2 因为没有读清楚题目WA了两次!
Easonsi @2023 """
class Solution:
    """ 2765. 最长交替子序列 #easy 考察细节. 
    下面写了个 O(n) 的, 没必要, O(n^2) 更简单
    """
    def alternatingSubarray(self, nums: List[int]) -> int:
        n = len(nums)
        ans = -1
        i = 0
        while i<n-1:
            if nums[i+1] == nums[i]+1:
                t = 2; i = i+2
                while i<n and nums[i]==nums[i-2]:
                    t += 1; i += 1
                ans = max(ans, t)
                # note case [2,3,4,3,4]
                i -= 1
            else:
                i += 1
        return ans
    
    """ 2766. 重新放置石块 """
    def relocateMarbles(self, nums: List[int], moveFrom: List[int], moveTo: List[int]) -> List[int]:
        # 没看清题目, TLE
        place2idxs = defaultdict(list)
        for i,x in enumerate(nums):
            place2idxs[x].append(i)
        for xfrom, xto in zip(moveFrom, moveTo):
            if xfrom==xto: continue
            place2idxs[xto] += place2idxs[xfrom]
            del place2idxs[xfrom]
        return sorted(place2idxs)
    def relocateMarbles(self, nums: List[int], moveFrom: List[int], moveTo: List[int]) -> List[int]:
        places = set(nums)
        for xfrom, xto in zip(moveFrom, moveTo):
            if xfrom==xto: continue
            places.remove(xfrom)
            places.add(xto)
        return sorted(places)
    
    """ 2767. 将字符串分割为最少的美丽子字符串 #medium 对于01字符串, 分解成 5的幂次 (二进制形式), 最小数量
限制: n 15
思路0: f(i,j) 形式的 #DP
思路1: 注意到分割类型需要包含所有字符, 因此DP考虑 f(i) 即可!
    """
    def minimumBeautifulSubstrings(self, s: str) -> int:
        MAX = 15
        avas = set(); t = 1
        while len(bin(t))-2 <= MAX:
            avas.add(bin(t)[2:])
            t *= 5
        @lru_cache(None)
        def f(i,j):
            if i>j: return inf
            if s[i:j+1] in avas: return 1
            ans = inf
            for x in range(i,j):
                ans = min(ans, f(i,x)+f(x+1,j))
            return ans
        ans = f(0,len(s)-1)
        return ans if ans!=inf else -1
    
    """ 2768. 黑格子的数目 #medium (m,n) 网格内, 有C个黑色的点, 问所有 (m-1)*(n-1) 个2*2格子中, 出现0~5个黑色格子的数量分别有多少
限制: m,n 1e5, C 1e4
思路1: #哈希表 
    1.1 对于所有点, 考虑其可能在的4个2*2格子, 分别对这四个格子中包含的黑色点计数, 如下
        注意到, 这样计数的话, 出现i个黑点的格子会被统计i次! 需要去重
    1.2 反过来考虑! 直接用一个hashmap记录所有2*2格子中所包含的黑色的数量! 对于所有的黑色点, 直接将其贡献加到hashmap中
        复杂度: O(C)
[灵神](https://leetcode.cn/problems/number-of-black-blocks/solution/mei-ju-by-endlesscheng-0mnx/)
    """
    def countBlackBlocks(self, m: int, n: int, coordinates: List[List[int]]) -> List[int]:
        # ans = [(m-1)*(n-1), 0,0,0,0]
        ans = [0, 0,0,0,0]
        points = set(map(tuple, coordinates))
        for x,y in coordinates:
            # ans[0] -= 4
            for i in range(x-1,x+1):
                if not 0<=i<m-1: continue
                for j in range(y-1,y+1):
                    if not 0<=j<n-1: continue
                    cnt = 0
                    for ii in range(i,i+2):
                        for jj in range(j,j+2):
                            if (ii,jj) in points: cnt += 1
                    ans[cnt] += 1
        for i in range(1,5):
            ans[i] //= i
        ans[0] = (m-1)*(n-1) - sum(ans[1:])
        return ans
            
        
sol = Solution()
result = [
    # sol.alternatingSubarray(nums = [2,3,4,3,4]),
    # sol.alternatingSubarray(nums = [4,5,6]),
    # sol.relocateMarbles(nums = [1,6,7,8], moveFrom = [1,7,2], moveTo = [2,9,5]),
    # sol.relocateMarbles(nums = [1,1,3,3], moveFrom = [1,3], moveTo = [2,2]),
    # sol.minimumBeautifulSubstrings(s = "1011"),
    # sol.minimumBeautifulSubstrings(s = "0"),
    # sol.minimumBeautifulSubstrings("111"),
    sol.countBlackBlocks(m = 3, n = 3, coordinates = [[0,0]]),
    sol.countBlackBlocks(m = 3, n = 3, coordinates = [[0,0],[1,1],[0,2]]),
]
for r in result:
    print(r)
