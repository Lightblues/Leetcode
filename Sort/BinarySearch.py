


class Solution:
    """
    递归实现
    """
    def bsearch(self, arr: list, n: int, val: int):
        return self.bsearchInternally(arr, 0, n-1, val)

    def bsearchInternally(self, arr: list, low: int, high: int, val: int):
        if low > high:
            return -1
        mid = low + ((high-low) >> 1)
        if arr[mid] == val:
            return mid
        elif arr[mid] < val:
            return self.bsearchInternally(arr, mid+1, high, val)
        else:
            return self.bsearchInternally(arr, low, mid-1, val)

    """
    非递归实现
    """
    def bsearch2(self, arr: list, n: int, val: int):
        low = 0
        high = n - 1
        while low <= high:
            mid = (low+high) // 2
            if arr[mid] == val:
                return mid
            elif arr[mid] < val:
                low = mid + 1
            else:
                high = mid - 1
        return -1

    """
    变形：找到第一个为给定值的数
    """
    def bsearch_first_equal(self, arr: list, n: int, val: int):
        low = 0
        high = n-1
        while low <= high:
            mid = low + ((high-low) >> 1)
            if arr[mid] > val:
                high = mid - 1
            elif arr[mid] < val:
                low = mid + 1
            else:
                if mid == 0 or arr[mid-1] != val:
                    return mid
                else:
                    high = mid - 1
        return -1


    """
    查找第一个大于等于给定值的元素
    """
    def bsearch_first_ge(self, arr: list, n: int, val: int):
        low, high = 0, n-1
        while low <= high:
            mid = low + ((high-low) >> 1)
            if arr[mid] >= val:
                if mid == 0 or arr[mid - 1] < val:
                    return mid
                else:
                    high = mid-1
            else:
                low = mid + 1
        return -1

arr = [1, 2, 2, 2, 3, 3, 4, 5]
v = Solution().bsearch_first_ge(arr, len(arr), 6)
print(v)