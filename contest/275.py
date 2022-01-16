from typing import List
import collections
import random

""" @210109
https://leetcode-cn.com/contest/weekly-contest-275
 """
class Solution275:
    """ 5976. 检查是否每一行每一列都包含全部整数 """
    def checkValid(self, matrix: List[List[int]]) -> bool:
        n = len(matrix)
        tt = set(range(1,n+1))
        for i in range(n):
            if set(matrix[i]) != tt:
                return False
            if set([matrix[j][i] for j in range(n)]) != tt:
                return False
        return True

    """ 5977. 最少交换次数来组合所有的 1 II
交换 定义为选中一个数组中的两个 互不相同 的位置并交换二者的值。
环形 数组是一个数组，可以认为 第一个 元素和 最后一个 元素 相邻 。
给你一个 二进制环形 数组 nums ，返回在 任意位置 将数组中的所有 1 聚集在一起需要的最少交换次数。

1 <= nums.length <= 10**5

输入：nums = [0,1,1,1,0,0,1,1,0]
输出：2
解释：这里列出一些能够将所有 1 聚集在一起的方案：
[1,1,1,0,0,0,0,1,1] 交换 2 次（利用数组的环形特性）。
[1,1,1,1,1,0,0,0,0] 交换 2 次。
无法在交换 0 次或 1 次的情况下将数组中的所有 1 聚集在一起。
因此，需要的最少交换次数为 2 

需要滑动平均计算片段和, 不然会超时
 """
    def minSwaps(self, nums: List[int]) -> int:
        n = len(nums)
        need = sum(nums)
        tmpSum = sum(nums[:need])
        result = need-tmpSum
        for i in range(0,n):
            tmpSum += nums[(i+need)%n] - nums[i]
            result = min(result, need-tmpSum)
        return result

    """ 5978. 统计追加字母可以获得的单词数
给定  startWords 和 targetWords , 判断 target 中每一个词可以通过 start 中某一个词通过下面的转换操作得到的数量.

1 <= startWords.length, targetWords.length <= 5 * 104
1 <= startWords[i].length, targetWords[j].length <= 26
startWords 和 targetWords 中的每个字符串都仅由小写英文字母组成
在 startWords 或 targetWords 的任一字符串中，每个字母至多出现一次

转换操作 如下面两步所述：
- 追加 任何 不存在 于当前字符串的任一小写字母到当前字符串的末尾。
    - 例如，如果字符串为 "abc" ，那么字母 'd'、'e' 或 'y' 都可以加到该字符串末尾，但 'a' 就不行。如果追加的是 'd' ，那么结果字符串为 "abcd" 。
- 重排 新字符串中的字母，可以按 任意 顺序重新排布字母。
    - 例如，"abcd" 可以重排为 "acbd"、"bacd"、"cbda"，以此类推。注意，它也可以重排为 "abcd" 自身。 

注意题目给出的条件, 每个word 都是由不同的字母构成的, 因此将word按照字典序排序, 建立一个set即可
"""
    def wordCount(self, startWords: List[str], targetWords: List[str]) -> int:
        sortWord = lambda s: "".join(sorted(list(s)))
        record = dict()
        for w in startWords:
            record[sortWord(w)] = True
        result = 0
        for w in targetWords:
            w = sortWord(w)
            for j in range(len(w)):
                if record.get(w[:j] + w[j+1:]) != None:
                    result += 1
                    break
        return result
    """ 5979. 全部开花的最早一天
两个数组, 分别是 播种 和 开花 所需的时间, 要求使得所有花都开放的最小时间 

https://leetcode-cn.com/contest/weekly-contest-275/problems/earliest-possible-day-of-full-bloom/
输入：plantTime = [1,4,3], growTime = [2,3,1]
输出：9
解释：灰色的花盆表示播种的日子，彩色的花盆表示生长的日子，花朵表示开花的日子。
一种最优方案是：
第 0 天，播种第 0 枚种子，种子生长 2 整天。并在第 3 天开花。
第 1、2、3、4 天，播种第 1 枚种子。种子生长 3 整天，并在第 8 天开花。
第 5、6、7 天，播种第 2 枚种子。种子生长 1 整天，并在第 9 天开花。
因此，在第 9 天，所有种子都开花。 

输入：plantTime = [1,2,3,2], growTime = [2,1,2,1]
输出：9
解释：灰色的花盆表示播种的日子，彩色的花盆表示生长的日子，花朵表示开花的日子。 
一种最优方案是：
第 1 天，播种第 0 枚种子，种子生长 2 整天。并在第 4 天开花。
第 0、3 天，播种第 1 枚种子。种子生长 1 整天，并在第 5 天开花。
第 2、4、5 天，播种第 2 枚种子。种子生长 2 整天，并在第 8 天开花。
第 6、7 天，播种第 3 枚种子。种子生长 1 整天，并在第 9 天开花。
因此，在第 9 天，所有种子都开花。 

- 题目给了干扰: 将一种花分成两次播种没有意义, 因为两者总的播种时间是一样的, 因此在过程中两种花都不会提早开花.
- 于是可以化简为, 给依次播种的花进行排序
- 可知, 总的播种时间是一定的, 目标在于减少开花所需时间. 因此每次根据开花所需时间排序, 选择需要最长时间的那种即可.
"""
    def earliestFullBloom(self, plantTime: List[int], growTime: List[int]) -> int:
        times = sorted(zip(growTime, plantTime), reverse=True)
        plantSum = 0
        result = 0
        for gt,pt in times:
            plantSum += pt
            result = max(result, plantSum+gt)
        return result
    pass

sol = Solution275()
res = [
    # sol.minSwaps(nums = [1,1,0,0,1]),
    # sol.wordCount(startWords = ["ab","a"], targetWords = ["abc","abcd"])
    sol.earliestFullBloom(plantTime = [1,2,3,2], growTime = [2,1,2,1]),
    sol.earliestFullBloom(plantTime = [1,4,3], growTime = [2,3,1]),
]
for r in res:
    print(r)