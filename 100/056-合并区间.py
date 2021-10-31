"""
以数组 intervals 表示若干个区间的集合，其中单个区间为 intervals[i] = [starti, endi] 。请你合并所有重叠的区间，并返回一个不重叠的区间数组，该数组需恰好覆盖输入中的所有区间。

输入：intervals = [[1,3],[2,6],[8,10],[15,18]]
输出：[[1,6],[8,10],[15,18]]
解释：区间 [1,3] 和 [2,6] 重叠, 将它们合并为 [1,6].

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/merge-intervals
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""
from typing import List
class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        def is_in_interval(x, interval):
            # 判断 x 是否在 interval 中
            return interval[0]<=x<=interval[1]
        def get_interval_index(x, intervals):
            # 判断 x 是否在 interval 数组中，若在则返回所在 interval 的序号
            for i, inter in enumerate(intervals):
                if is_in_interval(x, inter):
                    return i
            return -1
        intervals.sort()
        # 先对数组排序，可以省去很多……
        result = []
        for l, r in intervals:
            l_index, r_index = get_interval_index(l, result), get_interval_index(r, result)
            if l_index==r_index==-1:
                result.append([l, r])
            elif l_index == r_index:
                pass
            elif l_index!=-1:
                result[l_index][1] = r
            elif r_index!=-1:
                result[r_index][0] = l
        return result

    def merge2(self, intervals: List[List[int]]) -> List[List[int]]:
        intervals.sort(key=lambda x: x[0])
        merged = []
        for interval in intervals:
            # 如果列表为空，或者当前区间与上一区间不重合，直接添加
            if not merged or merged[-1][1] < interval[0]:
                merged.append(interval)
            else:
                # 否则的话，我们就可以与上一区间进行合并
                merged[-1][1] = max(merged[-1][1], interval[1])
        return merged

# intervals = [[1,3],[2,6],[8,10],[15,18]]
intervals = [[0,1], [1,2]]
print(Solution().merge2(intervals))
