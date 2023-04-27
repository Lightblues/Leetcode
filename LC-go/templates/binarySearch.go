package templates

/* 总结了二分查找的注意点:

- 循环退出条件，注意是 low <= high，而不是 low < high。
- mid 的取值，mid := low + (high-low)»1
- low 和 high 的更新。low = mid + 1，high = mid - 1。 */

func binarySearchMatrix(nums []int, target int) int {
 low, high := 0, len(nums)-1
 for low <= high {
  mid := low + (high-low)>>1
  if nums[mid] == target {
   return mid
  } else if nums[mid] > target {
   high = mid - 1
  } else {
   low = mid + 1
  }
 }
 return -1
}


/* 四个基本变种 */

// 二分查找第一个与 target 相等的元素，时间复杂度 O(logn)
func searchFirstEqualElement(nums []int, target int) int {
 low, high := 0, len(nums)-1
 for low <= high {
  mid := low + ((high - low) >> 1)
  if nums[mid] > target {
   high = mid - 1
  } else if nums[mid] < target {
   low = mid + 1
  } else {
   if (mid == 0) || (nums[mid-1] != target) { // 找到第一个与 target 相等的元素
    return mid
   }
   high = mid - 1
  }
 }
 return -1
}

// 二分查找最后一个与 target 相等的元素，时间复杂度 O(logn)
func searchLastEqualElement(nums []int, target int) int {
 low, high := 0, len(nums)-1
 for low <= high {
  mid := low + ((high - low) >> 1)
  if nums[mid] > target {
   high = mid - 1
  } else if nums[mid] < target {
   low = mid + 1
  } else {
   if (mid == len(nums)-1) || (nums[mid+1] != target) { // 找到最后一个与 target 相等的元素
    return mid
   }
   low = mid + 1
  }
 }
 return -1
}

// 二分查找第一个大于等于 target 的元素，时间复杂度 O(logn)
func searchFirstGreaterElement(nums []int, target int) int {
 low, high := 0, len(nums)-1
 for low <= high {
  mid := low + ((high - low) >> 1)
  if nums[mid] >= target {
   if (mid == 0) || (nums[mid-1] < target) { // 找到第一个大于等于 target 的元素
    return mid
   }
   high = mid - 1
  } else {
   low = mid + 1
  }
 }
 return -1
}

// 二分查找最后一个小于等于 target 的元素，时间复杂度 O(logn)
func searchLastLessElement(nums []int, target int) int {
 low, high := 0, len(nums)-1
 for low <= high {
  mid := low + ((high - low) >> 1)
  if nums[mid] <= target {
   if (mid == len(nums)-1) || (nums[mid+1] > target) { // 找到最后一个小于等于 target 的元素
    return mid
   }
   low = mid + 1
  } else {
   high = mid - 1
  }
 }
 return -1
}

/* 另外一类常见的: 基本有序数组. 在山峰数组中找山峰，在旋转有序数组中找分界点。
第 33 题，第 81 题，第 153 题，第 154 题，第 162 题，第 852 题
 */

func peakIndexInMountainArray(A []int) int {
 low, high := 0, len(A)-1
 for low < high {
  mid := low + (high-low)>>1
  // 如果 mid 较大，则左侧存在峰值，high = m，如果 mid + 1 较大，则右侧存在峰值，low = mid + 1
  if A[mid] > A[mid+1] {
   high = mid
  } else {
   low = mid + 1
  }
 }
 return low
}
