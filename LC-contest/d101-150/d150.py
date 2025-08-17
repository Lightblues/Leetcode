from typing import *

""" 
https://leetcode.cn/contest/biweekly-contest-150
Easonsi @2025
T2 暴力用二分也OK, 但可以更精细地分析; 也可以扫描线
T3 好复杂, #Lazy线段树 + #扫描线 TODO:
T4 放弃... 
"""
class Solution:
    """ 3452. 好数字之和 """
    def sumOfGoodNumbers(self, nums: List[int], k: int) -> int:
        acc = 0
        for i,x in enumerate(nums):
            if i-k>=0 and x<=nums[i-k]: continue
            if i+k<len(nums) and x<=nums[i+k]: continue
            acc += x
        return acc

    """ 3453. 分割正方形 I #medium 给定一组二维坐标里的正方形, 问最小的平行x轴的线, 使得直线上下分割得到的面结之和相等.
限制: n 5e4; 总面积 1e12. 答案精确到 1e-5
思路1: #二分 更准确的应该叫 #浮点二分
    复杂度: O(n log(U)), 其中U为坐标范围
思路2: #整数二分
思路3: #差分 + #扫描线
    想象有一根扫描线从0往上扫描, 依次经过 "所有正方形的边界y值". 
    在此过程中, 累计扫描线下方面的面积. 
    - 某一刻, 累计面积 > S/2, 
    - 此外, 可以记录某一刻y值包含的正方向x方向底边之和! -- 可以用 #差分 来记录!
    复杂度: O(n log(n)) 其中logn是排序复杂度
[ling](https://leetcode.cn/problems/separate-squares-i/solutions/3076424/zheng-shu-er-fen-pythonjavacgo-by-endles-8yn5/)
    """
    def separateSquares(self, squares: List[List[int]]) -> float:
        total_s, mn, mx = 0, 0, 0
        for x,y,l in squares:
            total_s += l*l
            mn = min(mn, y)
            mx = max(mx, y+l)
        # 
        def check(yline):
            s = 0
            for x,y,l in squares:
                if y+l <= yline: s += l*l
                elif y <= yline <= y+l: s += (yline-y)*l
            return s
        l,r = mn, mx
        while abs(r-l) > 1e-6:  # NOTE: 二分精度
            mid = (l+r)/2
            if check(mid) < total_s/2:
                l = mid
            else:
                r = mid
        return (l+r)/2  # NOTE: 中点精度更高!

    """ 3454. 分割正方形 II #hard 相较于上一题, 重叠部分的面积不能叠加
思路1: #Lazy 线段树 + 扫描线
[ling](https://leetcode.cn/problems/separate-squares-ii/solutions/3078402/lazy-xian-duan-shu-sao-miao-xian-pythonj-eeqk/)

0850. 矩形面积 II
[ling](https://leetcode.cn/problems/rectangle-area-ii/solutions/3078272/lazy-xian-duan-shu-sao-miao-xian-pythonj-4tkr/)
     """


    """ 3455. 最短匹配子字符串 #hard 有一个恰好包含两个 * 的pattern字符串, 问其匹配的s的子串的最小长度
限制: n 1e5
线性做法：KMP+枚举中间+三指针 [ling](https://leetcode.cn/problems/shortest-matching-substring/solutions/3076453/xian-xing-zuo-fa-kmpmei-ju-zhong-jian-sa-5qow/)
    """


sol = Solution()
result = [
    sol.separateSquares(squares = [[0,0,2],[1,1,1]]),
]
for r in result:
    print(r)