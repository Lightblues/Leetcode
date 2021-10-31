"""
给你一个 无重叠的 ，按照区间起始端点排序的区间列表。
在列表中插入一个新的区间，你需要确保列表中的区间仍然有序且不重叠（如果有必要的话，可以合并区间）。

输入：intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]], newInterval = [4,8]
输出：[[1,2],[3,10],[12,16]]
解释：这是因为新的区间 [4,8] 与 [3,5],[6,7],[8,10] 重叠。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/insert-interval
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""
from typing import List
class Solution:
    def insert_try(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        left, right = newInterval
        for i, (l, r) in enumerate(intervals):
            if i==0 and left<l<=right:
                new_right = max(right, intervals[0][1])
                intervals[0] = [left, new_right]
                j = 1
                while j<len(intervals):
                    if intervals[j][0]  <= new_right:
                        new_right = max(new_right, intervals[j][1])
                    j += 1
                del intervals[1:j]
                return intervals


            if l <= left <= r:
                if right <= r:
                    return intervals
                else:
                    intervals[i][1] = right
                    for j in range(i+1, len(intervals)):
                        # if intervals[j][0] <= right <= intervals[j][1]:
                        #     intervals
                        if right < intervals[j][0]:
                            del intervals[i+1:j]
                            return intervals
                        elif intervals[j][0] <= right <= intervals[j][1]:
                            intervals[i][1] = intervals[j][1]
                            del intervals[i+1:j+1]
                            return intervals
                    return intervals

            elif right < l:
                intervals.insert(i, newInterval)
                return intervals
        intervals.append(newInterval)
        return intervals

    def insert_try2(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        left, right = newInterval

        # for i, (l, r) in enumerate(intervals):
        #     if not
        # 找到最后一个满足 left<=l 的区间
        start = 0
        # while start+1<len(intervals) and intervals[start+1][0]>left:
        #     start += 1
        for l, r in intervals:
            if l>left:
                start += 1
        # 从 start（插入的位置）往后检索，看重合的区间
        end = start
        while end<len(intervals) and intervals[end][0]<=right<=intervals[end][1]:
            end += 1
            left = max(left, intervals[end][1])
        del intervals[start:end]
        intervals.append(start, [])

    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        left, right = newInterval
        placed = False
        ans = []
        for li, ri in intervals:
            if li > right:
                if not placed:
                    ans.append([left, right])
                    placed = True
                ans.append([li, ri])
            elif ri < left:
                ans.append([li, ri])
            else:
                left = min(left, li)
                right = max(right, ri)
        if not placed:
            ans.append([left, right])
        return ans


# intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]]; newInterval = [4,8]
# intervals = [[1,5]]; newInterval = [0,3]
# intervals = [[1,5],[6,8]]; newInterval = [0,9]
intervals = [[1,3],[6,9]]; newInterval = [2,5]
print(Solution().insert(intervals, newInterval))
