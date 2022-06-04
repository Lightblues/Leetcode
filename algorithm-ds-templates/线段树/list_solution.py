import bisect


class RangeModule:
    """ 0715. Range 模块 #hard #题型
要求实现对于 [) 形式的区间的 增删查操作.
思路1: 关联 6066, 用两个数组分别记录左右边界. 在添加记录的时候, 注意进行区间的合并.
思路2: [官方](https://leetcode.cn/problems/range-module/solution/range-mo-kuai-by-leetcode/) 答案中 #区间求交 #二分
实现了一个通用的函数, 计算查询区间 [l,r) 与所存储的区间有交集, 实现更为方便的 add, remove.
#技巧: 通过 (100, 10, 1) 这种形式的步长衰减来替代bisect

输入
["RangeModule", "addRange", "removeRange", "queryRange", "queryRange", "queryRange"]
[[], [10, 20], [14, 16], [10, 14], [13, 15], [16, 17]]
输出
[null, null, null, true, false, true]

解释
RangeModule rangeModule = new RangeModule();
rangeModule.addRange(10, 20);
rangeModule.removeRange(14, 16);
rangeModule.queryRange(10, 14); 返回 true （区间 [10, 14) 中的每个数都正在被跟踪）
rangeModule.queryRange(13, 15); 返回 false（未跟踪区间 [13, 15) 中像 14, 14.03, 14.17 这样的数字）
rangeModule.queryRange(16, 17); 返回 true （尽管执行了删除操作，区间 [16, 17) 中的数字 16 仍然会被跟踪）

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/range-module
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

"""
    def __init__(self):
        self.left = []
        self.right = []

    def addRange(self, left: int, right: int) -> None:
        """ 增加区间.
        注意, 如果已经有 [1,2), [3,4) 区间, 然后插入一个新区间 [2,3), 需要将其与相连的合并起来."""
        if len(self.left)==0:
            self.left.append(left)
            self.right.append(right)
            return
        # 注意为了查找数组交叉关系, 需要用 right 查找维护的左区间, 用 left 查找维护的右区间
        # 为了将相邻的数组合并 例如 [1,2) 和 [2,3), 需要分别 bisect_left, bisect_right
        idxL = bisect.bisect_left(self.right, left)
        idxR = bisect.bisect_right(self.left, right)
        if idxL == idxR:
            # 注意有 idxL<= idxR
            # idxL == idxR 说明: 没有与其他区间的交叉, 插入
            # 因此这里已经避免了 idxL==idxR == len() / 0 的边界情况, 下面的 idxL 和 idxR-1 可以不用判断越界
            valL, valR = left, right
        else:
            # 因为有了上面的判断, 可以避免数组越界
            valL = min(self.left[idxL], left)
            valR = max(self.right[idxR-1], right)
        # 用 slice 更新数组, 效率较高
        self.left[idxL:idxR] = [valL]
        self.right[idxL:idxR] = [valR]

    def queryRange(self, left: int, right: int) -> bool:
        """ 查询 [left, right) 区间是否被包含
        例子: 已有区间 [16,20), 则对于查询 [16,17), [17,18), [16,20) 均返回 True
        注意边界情况
        !! 智障!! 由于必然是包含关系, 只需要bisect一个index即可!
        """
        # 剪枝, 可以避免数组越界
        if len(self.left)==0: return False
        idxL = bisect.bisect_left(self.left, left)
        idxR = bisect.bisect_left(self.right, right)
        # 完全被包含的情况
        if idxL > idxR:
            return True
        # 这里用了 bisect_left, 说明超出了最大范围
        # 主要是为了避免数组越界
        if idxL>=len(self.left):
            return False
        return idxL==idxR and self.right[idxR]>=right and self.left[idxL]<=left

    def removeRange(self, left: int, right: int) -> None:
        """ 删除区间 """
        if len(self.left)==0: return
        idxL = bisect.bisect_left(self.right, left)
        # 注意删除不需要 bisect_right
        idxR = bisect.bisect_left(self.left, right)
        if idxL==idxR: return
        # 
        l, r = [], []
        if self.left[idxL] < left:
            l.append(self.left[idxL])
            r.append(left)
        if self.right[idxR-1]>right:
            l.append(right)
            r.append(self.right[idxR-1])
        self.right[idxL:idxR] = r
        self.left[idxL:idxR] = l

class RangeModule(object):
    def __init__(self):
        self.ranges = []

    def _bounds(self, left, right):
        """ 计算与 [left, right) 存在交集的区间有哪些
        #技巧: 通过 (100, 10, 1) 这种形式的步长衰减来替代bisect """
        i, j = 0, len(self.ranges) - 1
        for d in (100, 10, 1):
            while i + d - 1 < len(self.ranges) and self.ranges[i+d-1][1] < left:
                i += d
            while j >= d - 1 and self.ranges[j-d+1][0] > right:
                j -= d
        return i, j

    def addRange(self, left, right):
        i, j = self._bounds(left, right)
        if i <= j:
            left = min(left, self.ranges[i][0])
            right = max(right, self.ranges[j][1])
        self.ranges[i:j+1] = [(left, right)]

    def queryRange(self, left, right):
        i = bisect.bisect_left(self.ranges, (left, float('inf')))
        if i: i -= 1
        return (bool(self.ranges) and
                self.ranges[i][0] <= left and
                right <= self.ranges[i][1])

    def removeRange(self, left, right):
        i, j = self._bounds(left, right)
        merge = []
        for k in range(i, j+1):
            if self.ranges[k][0] < left:
                merge.append((self.ranges[k][0], left))
            if right < self.ranges[k][1]:
                merge.append((right, self.ranges[k][1]))
        self.ranges[i:j+1] = merge
