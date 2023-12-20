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
https://leetcode.cn/contest/weekly-contest-373
https://leetcode.cn/circle/discuss/ip8jWQ/

T4 有意思, 虽然第一个想法错了 WA了两发, 还是进行 top100
Easonsi @2023 """
class Solution:
    """ 2946. 循环移位后的矩阵相似检查 """
    def areSimilar(self, mat: List[List[int]], k: int) -> bool:
        m,n = len(mat),len(mat[0])
        for i in range(m):
            for j in range(n):
                if mat[i][j] != mat[i][(j+k)%n]:
                    return False
        return True
    
    """ 2947. 统计美丽子字符串 I """
    def beautifulSubstrings(self, s: str, k: int) -> int:
        n = len(s)
    
    """ 2948. 交换得到字典序最小的数组 #medium 对于绝对差值 <= limit 的两个位置可以交换, 求可以得到的最小序列
思路1: 对于 (x,i) 排序之后, 划分可以交换的区间
    """
    def lexicographicallySmallestArray(self, nums: List[int], limit: int) -> List[int]:
        n = len(nums)
        vals = []
        for i,x in enumerate(nums):
            vals.append((x,i))
        vals.sort()
        ans = nums[:]   # 注意下面的边界, 可能有没有遍历到的idx
        l,r = 0,1
        while r < n:
            while r < n and vals[r][0]-vals[r-1][0] <= limit:
                r += 1
            vs, idxs = zip(*vals[l:r])
            for idx,v in zip(sorted(idxs), vs):
                ans[idx] = v
            l,r = r,r+1
        return ans

    """ 2949. 统计美丽子字符串 II #hard 对于一个字符串, 若子串的元音非元音的量为 x,y, 若 x==y 并且 (x*y) %k == 0, 求数量
限制: n 5e4; k 1e3
思路0: 有问题!
    因为 x==y, 除非k是完全平方数, 否则x应该是k的倍数; 因此当k为完全平方数的时候, 可以 k <- sqrt{k}.
        这样, 问题化简为求元音长度为k的倍数的子串
    为此, 利用一个数组先记录哪些位置出发, 长度为2k的子串满足条件
        何时可以转移? 相邻的两个位置 (距离2k) 可以连接的时候!
    BUG: 存在可能长 2xk 的子串满足条件, 但是当个的长为 2k 的不满足! 例如对于 k=2, s = "aabb"
思路1: 
    将两者看作 1/-1, 问题等价于找到和为0, 同时长度为k的倍数的数量!
    为此, 可以根据前缀和计数 (并且统计idx和k的关系)
[灵神](https://leetcode.cn/problems/count-beautiful-substrings-ii/solutions/2542274/fen-jie-zhi-yin-zi-qian-zhui-he-ha-xi-bi-ceil/)
    """
    def beautifulSubstrings(self, s: str, k: int) -> int:
        # 思路0: 有问题!
        n = len(s)
        if sqrt(k) == int(sqrt(k)):             # BUG: 这里对于k的变换也不对
            k = int(sqrt(k))
        # 计算哪些长度为 2k的位置是满足条件的
        meet = [0] * n
        vowels = 'aeiou'
        cnt1 = 0
        for i,x in enumerate(s[:2*k]):
            cnt1 += int(x in vowels)
        if cnt1 == k: meet[0] = 1
        for i in range(2*k, n):
            cnt1 += int(s[i] in vowels) - int(s[i-2*k] in vowels)
            if cnt1 == k: meet[i-2*k+1] = 1
        # 计算满足条件的子串数量
        ans = 0
        for idx in range(k):
            cnts = [0]
            for i in range(idx, n, 2*k):
                if meet[i]:
                    if cnts[-1] == 0: cnts.append(1)
                    else: cnts[-1] += 1
                else:
                    if cnts[-1] != 0: cnts.append(0)
            # 对于一个长度为 x的连续序列, 子串数量 x*(x+1)/2
            for x in cnts:
                ans += x*(x+1)//2
        return ans
    def beautifulSubstrings(self, s: str, k: int) -> int:
        # 思路1
        # 对k进行变换 8 -> 4
        # if sqrt(k) == int(sqrt(k)): k = int(sqrt(k))    # k <- sqrt(k) 不对!
        bases = Counter()
        for x in range(2, ceil(sqrt(k+1))):
            while k%x == 0:
                bases[x] += 1
                k //= x
        if k != 1: bases[k] += 1
        k = 1
        for x,c in bases.items():
            k *= x**(ceil(c/2))
        # 遍历计算!
        step = 2*k              # 最小长度
        vowels = 'aeiou'
        s = [1 if x in vowels else -1 for x in s]
        csum = 0
        csum2d = defaultdict(Counter)
        csum2d[0][step-1] = 1       # 注意添加边界条件!
        ans = 0
        for i,x in enumerate(s):
            csum += x
            # 匹配条件为: ccum相同, 同时idx相差2k的倍数
            ans += csum2d[csum][i%step]
            csum2d[csum][i%step] += 1
        return ans

sol = Solution()
result = [
    # sol.lexicographicallySmallestArray(nums = [1,5,3,9,8], limit = 2),
    sol.beautifulSubstrings(s = "baeyh", k = 2),
    sol.beautifulSubstrings(s = "abba", k = 1),
    sol.beautifulSubstrings(s = "bcdf", k = 1),
    sol.beautifulSubstrings("ouuoeqd", 2),
    sol.beautifulSubstrings("eeebjoxxujuaeoqibd",8),
]
for r in result:
    print(r)
