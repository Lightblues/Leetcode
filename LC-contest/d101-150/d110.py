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
https://leetcode-cn.com/contest/biweekly-contest-110
https://leetcode.cn/circle/discuss/N76IWK/

T4好难orz, 贪心+DP确实比较有思维量!
Easonsi @2023 """
class Solution:
    """ 2806. 取整购买后的账户余额 #easy 要求实现四舍五入, 下面 +5 然后整除的思路更优雅!
 """
    def accountBalanceAfterPurchase(self, purchaseAmount: int) -> int:
        # 复杂写法
        a = purchaseAmount / 10
        a = ceil(a) if a>= (purchaseAmount//10+.5) else floor(a)
        return 100 - a*10
    def accountBalanceAfterPurchase(self, purchaseAmount: int) -> int:
        # 简洁! 
        return 100 - (purchaseAmount + 5) // 10 * 10

    """ 2807. 在链表中插入最大公约数
 """
    def insertGreatestCommonDivisors(self, head: Optional[ListNode]) -> Optional[ListNode]:
        a,b = head, head.next
        while b:
            x = math.gcd(a.val,b.val)
            a.next = ListNode(x)
            a.next.next = b
            a,b = b,b.next
        return head
    
    """ 2808. 使循环数组所有元素相等的最少秒数 #medium 每一秒, 每个位置的数字可以变成 (i-1,i,i+1) 三个数字中的任意一个 (循环数组), 问将所有数字变为相同的操作次数
思路1: 显然, 传播的最小时间取决于相同数字x所在的间距. 
 """
    def minimumSeconds(self, nums: List[int]) -> int:
        n = len(nums)
        x2idxs = defaultdict(list)
        for i,x in enumerate(nums):
            x2idxs[x].append(i)
        ans = n-1
        for _,idxs in x2idxs.items():
            # if len(idxs)==1: continue
            mx = (idxs[0]+n) - idxs[-1]
            for i in range(1, len(idxs)):
                mx = max(mx, idxs[i]-idxs[i-1])
            ans = min(ans, mx//2)
        return ans
    
    
    """ 2809. 使数组和小于等于 x 的最少时间 #hard  给定两个数组, 在每次操作中, 1] 将 num1 += num2, 2] 选择一个idx将num1的某一位置零, 问使得nums1之和 <=x 的最小次数
限制: n 1e3; 元素 1e3; x 1e6
思路0: (想到了一半没思路了)
    要求操作k次, 如何找到最优解? (判断是否可行)
        若没有置零操作, 则和为 sum(x1 + k*x2), 考虑置零操作, 则减小量为 x1+i*x2, 0<i<=k 取决于对于该位置是何时置零的
        因此, 可以考虑对于没有置零过的元素构建 #最大堆
    如何找到最小的k? 二分? 不对!
思路1: #贪心 + #DP
    继续上面的思路, 转化问题: 「从数组中选取长度为k的子序列, 分别进行操作, 变换后的元素为 x1 + j*x2, 0<j<=k, 要求最大和」
    我们可以用 #DP 来求解: 定义 f[i,j] 表示从前i个数字中选择j个构成子序列的最大和! 则有递推:
        选, f[i,j] = f[i-1,j-1] + nums1[i]+j*nums2[i]
        不选, f[i,j] = f[i-1,j] 
        两者取较大值. 
    为什么可以对子序列的权重设置为 1,2,...j? 核心的是这里的 #贪心
        我们可以对nums2先进行排序, 根据 #排序不等式 的性质知道应该将大的因子分配到较大的数字上
见 [灵神](https://leetcode.cn/problems/minimum-time-to-make-array-sum-at-most-x/solutions/2374920/jiao-ni-yi-bu-bu-si-kao-ben-ti-by-endles-2eho/)
 """
    def minimumTime(self, nums1: List[int], nums2: List[int], x: int) -> int:
        s1, s2 = sum(nums1), sum(nums2)
        n = len(nums1)
        arr = sorted(zip(nums1, nums2), key=lambda x:x[1],)
        f = [[0]*(n+1) for _ in range(n+1)]   # 防止递推公式越界
        for i in range(1,n+1):
            # 对于前i个数字计算
            for j in range(1,i+1):
                # j 的取值范围为 [1...i]
                f[i][j] = max(f[i-1][j-1] + arr[i-1][0]+j*arr[i-1][1], f[i-1][j])
        # 
        for k in range(n+1):
            s = s1 + k*s2
            if s - f[n][k] <= x: return k
        return -1
                
                
        

    
sol = Solution()
result = [
    sol.minimumTime(nums1 = [1,2,3], nums2 = [1,2,3], x = 4),
    sol.minimumTime(nums1 = [1,2,3], nums2 = [3,3,3], x = 4),
]
for r in result:
    print(r)
