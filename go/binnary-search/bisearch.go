package main

import (
	"fmt"
)

// =================== Binary Search 基本算法 ===================================
func searchFirstEqualElement(nums []int, target int) int {
	l, r := 0, len(nums)-1
	for l<=r{
		mid := l+(r-l)>>1
		if nums[mid]>target{
			r = mid-1
		} else if nums[mid] < target{
			l = mid +1
		} else {
			if mid==0 || (nums[mid-1]!=target) {
				return mid
			}
			r = mid-1
		}
	}
	return -1
}
func searchLastEqualElement(nums []int, target int) int {
	l, r := 0, len(nums)-1
	for l<=r{
		mid := l+(r-l)>>1
		if nums[mid]>target{
			r = mid-1
		} else if nums[mid] < target{
			l = mid +1
		} else {
			if mid==len(nums)-1 || (nums[mid+1]!=target) {
				return mid
			}
			l = mid+1
		}
	}
	return -1
}

func min(x, y int) int {
	if x < y {
		return x
	}
	return y
}

func max(x,y int)int{
	if x>y{
		return x
	}
	return y
}

// =================== Binary Search ===================================
/* 0004.Median-of-Two-Sorted-Arrays/ 难
给定两个大小为 m 和 n 的有序数组 nums1 和 nums2。
请你找出这两个有序数组的中位数，并且要求算法的时间复杂度为 O(log(m + n))。
你可以假设 nums1 和 nums2 不会同时为空。 
nums1 = [1, 3]
nums2 = [2]
The median is 2.0*/
// 方法一 二分
func findMedianSortedArrays(nums1 []int, nums2 []int) float64 {
	// 确保 nums1 的长度小
	if len(nums1) > len(nums2){
		return findMedianSortedArrays(nums2, nums1)
	}
	// 这里 k = (len(nums1)+len(nums2)+1)>>1, 此时 
	// 1. 当总长度为奇数, 中位数为 max(nums1[m1-1], nums2[m2-1])
	// 2. 总长度为偶数, 中位数为 mean(max(nums1[m1-1], nums2[m2-1])), min(nums1[m1], nums2[m2])))
	l, r, k, m1, m2 := 0, len(nums1), (len(nums1)+len(nums2)+1)>>1, 0,0
	for(l<=r){
		// nums1:  ……………… nums1[nums1Mid-1] | nums1[nums1Mid] ……………………
		// nums2:  ……………… nums2[nums2Mid-1] | nums2[nums2Mid] ……………………
		m1 = (l+r)>>1 // 分界限右侧是 mid，分界线左侧是 mid - 1
		m2 = k-m1
		// 由于 nums1 的长度小, 下面可以保证 nums2[m2-1], nums2[m2] 总是不越界
		if m1!=len(nums1) && nums1[m1]<nums2[m2-1] {
			l = m1+1
		} else if m1!=0 && nums1[m1-1]>nums2[m2] {
			r = m1-1
		} else {
			// 终止: 1. m1 到达最后边界; 2. 找到分界点, 满足 nums1[m1]>=nums2[m2-1] && nums2[m2]>=nums1[m1-1]
			break
		}
	}
	// 1. 总长度为奇数
	midL, midR := 0, 0
	if m1==0 {
		midL = nums2[m2-1]
	} else if m2==0 {
		midL = nums1[m1-1]
	} else {
		midL = max(nums1[m1-1], nums2[m2-1])
	}
	if (len(nums1)+len(nums2)) % 2 == 1{
		return float64(midL)
	}
	// 2. 偶数
	if m1==len(nums1){
		midR = nums2[m2]
	} else if m2==len(nums2){
		midR = nums1[m1]
	} else {
		midR = min(nums1[m1], nums2[m2])
	}
	return float64(midL+midR) / 2
}
// 方法二 合并
func findMedianSortedArrays2(nums1 []int, nums2 []int) float64 {
	sorted := []int{}
	m, n := len(nums1), len(nums2)
	for i,j:=0,0; i<m||j<n; {
		if i==m {
			sorted = append(sorted, nums2[j])
			j++
		} else if j==n {
			sorted = append(sorted, nums1[i])
			i++
		} else {
			if nums1[i] < nums2[j]{
				sorted = append(sorted, nums1[i])
				i++
			} else {
				sorted = append(sorted, nums2[j])
				j++
			}
		}
	}
	if len(sorted) % 2 ==1 {
		return float64(sorted[(len(sorted))/2])
	} 
	return float64(sorted[len(sorted)/2-1] + sorted[len(sorted)/2]) / 2
}
func f4(){
	fmt.Println(findMedianSortedArrays2([]int{1,2}, []int{3,4}))
	fmt.Println(findMedianSortedArrays2([]int{1,3}, []int{2}))
	fmt.Println(findMedianSortedArrays2([]int{5,6}, []int{1,2,3,4,7}))
}

/* 0033.Search-in-Rotated-Sorted-Array/
假设按照升序排序的数组在预先未知的某个点上进行了旋转。( 例如，数组 [0,1,2,4,5,6,7] 可能变为 [4,5,6,7,0,1,2] )。搜索一个给定的目标值，如果数组中存在这个目标值，则返回它的索引，否则返回 -1 。你可以假设数组中不存在重复的元素。

Input: nums = [4,5,6,7,0,1,2], target = 0
Output: 4 

- 可以在常规二分查找的时候查看当前 mid 为分割位置分割出来的两个部分 `[l, mid]` 和 `[mid + 1, r]` 哪个部分是有序的
- 如果 `[l, mid - 1]` 是有序数组 (即 `nums[mid]>=nums[0]`)，且 target 的大小满足 `[nums[l],nums[mid])`，则我们应该将搜索范围缩小至 `[l, mid - 1]`，否则在 `[mid + 1, r]` 中寻找。
- 反之, 若 `nums[mid]<=nums[-1]`, 则可直接根据 target 是否在 `(nums[mid], nums[r]]` 判断是否在右半部分, 否则在另一边搜索*/
func search33(nums []int, target int) int {
	l, r := 0, len(nums)-1
	for l<=r {
		mid := l+(r-l)>>1
		if nums[mid] == target {
			return mid
		}
		if nums[mid] >= nums[0] {
			if target >= nums[0] && target<nums[mid] {
				r = mid-1
			} else {
				l = mid+1
			}
		} else {
			if target <= nums[len(nums)-1] && target > nums[mid] {
				l = mid+1
			} else {
				r = mid-1
			}
		}
	}
	return -1
}
func f33(){
	fmt.Println(search33([]int{4,5,6,7,0,1,2}, 0))
}

/* 0034.Find-First-and-Last-Position-of-Element-in-Sorted-Array/
给定一个按照升序排列的整数数组 nums，和一个目标值 target。找出给定目标值在数组中的开始位置和结束位置。你的算法时间复杂度必须是 O(log n) 级别。如果数组中不存在目标值，返回 [-1, -1]。

Input: nums = [5,7,7,8,8,10], target = 8
Output: [3,4] */

func searchRange(nums []int, target int) []int {
	return []int{searchFirstEqualElement(nums, target), searchLastEqualElement(nums, target)}
}

/* 0035.Search-Insert-Position/
Given a sorted array and a target value, return the index if the target is found. If not, return the index where it would be if it were inserted in order.
You may assume no duplicates in the array.

Input: [1,3,5,6], 7
Output: 4
这一题是经典的二分搜索的变种题，在有序数组中找到最后一个比 target 小的元素。*/
func searchInsert(nums []int, target int) int {
	low, high := 0, len(nums)-1
	for low <= high {
		mid := low + (high-low)>>1
		if nums[mid] >= target {		// [1], 1 应该返回 0
			high = mid-1
		} else {
			if mid==len(nums)-1 || nums[mid+1]>=target{
				return mid+1
			}
			low = mid+1
		}
	}
	return 0  // 注意这里的返回条件
}
func f35(){
	fmt.Println(searchInsert([]int{1,3,5,6}, 0))
}



/* 0069.Sqrtx/
实现 int sqrt(int x) 函数。计算并返回 x 的平方根，其中 x 是非负整数。由于返回类型是整数，结果只保留整数的部分，小数部分将被舍去。
Input: 8
Output: 2
Explanation: The square root of 8 is 2.82842..., and since 
             the decimal part is truncated, 2 is returned. */
// 解法一 二分, 找到最后一个满足 n^2 <= x 的整数n
func mySqrt(x int) int {
	l, h := 0, x
	for l<=h{
		mid := l+(h-l)>>2
		if mid*mid > x{
			h = mid-1
		} else {
			if (mid+1)*(mid+1) > x{
				return mid
			}
			l = mid+1
		}
	}
	return -1
}
// 解法二 牛顿迭代法 https://en.wikipedia.org/wiki/Integer_square_root
// 即求 f(r)=r^2-x 的零点
func mySqrt1(x int) int {
	r := x
	for r*r > x {
		r = (r + x/r) / 2
	}
	return r
}
func f69(){
	fmt.Println(mySqrt(8), mySqrt(0))
}

/* 0074.Search-a-2D-Matrix/
Write an efficient algorithm that searches for a value in an m x n matrix. This matrix has the following properties:

Integers in each row are sorted from left to right.
The first integer of each row is greater than the last integer of the previous row.

Input:
matrix = [
  [1,   3,  5,  7],
  [10, 11, 16, 20],
  [23, 30, 34, 50]
]
target = 3
Output: true

其实就是一维的有序列表搜索, 不过需要进行坐标变换*/
func searchMatrix(matrix [][]int, target int) bool {
	m, n:=len(matrix), len(matrix[0])
	low, high := 0, m*n-1
	for low<=high {
		mid := low+(high-low)>>1
		if matrix[mid/n][mid%n] == target {
			return true
		} else if matrix[mid/n][mid%n] > target{
			high = mid -1
		} else {
			low = low+1
		}
	}
	return false
}
func f74(){
	matrix := [][]int{
		{1,   3,  5,  7},
		{10, 11, 16, 20},
		{23, 30, 34, 50}}
	fmt.Println(searchMatrix(matrix, 3))
}

/* 0081.Search-in-Rotated-Sorted-Array-II/
Suppose an array sorted in ascending order is rotated at some pivot unknown to you beforehand.
(i.e., [0,0,1,2,2,5,6] might become [2,5,6,0,0,1,2]).
You are given a target value to search. If found in the array return true, otherwise return false. 

Input: nums = [2,5,6,0,0,1,2], target = 0
Output: true

This is a follow up problem to  Search in Rotated Sorted Array, where nums may contain duplicates.
Would this affect the run-time complexity? How and why? */
func search(nums []int, target int) bool {
	l, r := 0, len(nums)-1
	for l<=r {
		mid := l+(r-l)>>1
		if nums[mid] == target{
			return true
		}
		if nums[mid] == nums[l] && nums[mid]==nums[r]{
			// 此时无法确定左右哪一边是有序的
			l++; r--
		} else if nums[mid] >= nums[l] {
			// 1. 左半部分有序: 在 nums[l] != nums[r] 时, nums[l] 一定 >nums[r]
			if target>=nums[l] && target<nums[mid] {
				r = mid-1
			} else {
				l = mid+1
			}
		} else {
			// 2. 右半部分有序
			if target<=nums[r] && target>nums[mid] {
				l = mid+1
			} else {
				r = mid-1
			}
		}
	}
	return false
}
func f81(){
	fmt.Println(search([]int{2,5,6,0,0,1,2}, 3))
}

/* 0153.Find-Minimum-in-Rotated-Sorted-Array/
假设按照升序排序的数组在预先未知的某个点上进行了旋转。( 例如，数组 [0,1,2,4,5,6,7] 可能变为 [4,5,6,7,0,1,2] )。请找出其中最小的元素。
你可以假设数组中不存在重复元素。 */
// 方法一 基本二分终止条件
func findMin(nums []int) int {
	l, r, mid := 0, len(nums)-1, 0
	for l<=r{
		mid = (l+r)/2
		if nums[mid]<=nums[r]{		// =: 边界情况, 长度为1 [2]
			if nums[mid] > nums[l] {
				return nums[l]
			}
			if mid==0 || nums[mid-1]>nums[mid]{
				return nums[mid]
			}
			r = mid-1
		} else{
			l = mid+1
		}
	}
	return -1
}
// 方法二 这类题目也可以用 `low < high` 作为终止条件, 相较于基本范式, 这里 high 和 low 的是不对等的. high 只是用来缩减搜索范围, 而 low为输出结果的指针
// https://leetcode-cn.com/problems/find-minimum-in-rotated-sorted-array/solution/xun-zhao-xuan-zhuan-pai-xu-shu-zu-zhong-5irwp/
func findMin0(nums []int) int {
    low, high := 0, len(nums) - 1
    for low < high {
		// 1. 注意, 根据这里 pivot 的更新公式 和循环终止条件, 其可能=low 而不可能为 high
        pivot := low + (high - low) / 2
        if nums[pivot] < nums[high] {
			// 2. 这里 high 和 low 的是不对等的. high 只是用来缩减搜索范围, 而 low为输出结果
			// 当 nums[pivot] < nums[high], 此时的 pivot 可能正是最小值, 更新 high
            high = pivot
        } else {
            low = pivot + 1 // 3. 结合(1), low 是可以到达 high 的, 即终止条件
			// low 更新条件: nums[pivot] >= nums[high] (注意 pivot!=high), 说明 pivot 及其左侧为升序, pivot 右侧一定有更小的
        }
    }
    return nums[low]
}
func f153(){
	fmt.Println(findMin([]int{4,5,6,7,0,1,2}))
	fmt.Println(findMin([]int{0,1,2,4,5,6,7}))
	fmt.Println(findMin([]int{2,2,2,0,1,2}))  // 无法应对重复
}

/* 0154.Find-Minimum-in-Rotated-Sorted-Array-II/ 难
相较于上一题可能出现重复
Input: [2,2,2,0,1]
Output: 0 */
// 解法一 判断条件更复杂了
func findMin154(nums []int) int {
	l, r, mid := 0, len(nums)-1, 0
	for l<=r{
		mid = (l+r)/2
		if nums[mid] == nums[r]{
			if mid == l{
				return nums[mid]
			}
			r--
		}else if nums[mid]<=nums[r]{
			if nums[mid] > nums[l] {
				return nums[l]
			}
			if mid==0 || nums[mid-1]>nums[mid]{
				return nums[mid]
			}
			r = mid-1
		} else{
			l = mid+1
		}
	}
	return -1
}
func findMin1542(nums []int) int {
	low, high := 0, len(nums)-1
	for low<high {
		mid := low+(high-low)>>1
		if nums[mid] > nums[high] {
			low = mid+1
		} else if nums[mid] == nums[high] {
			high--
		} else {
			high = mid
		}
	}
	return nums[low]
}
func f154(){
	fmt.Println(findMin1542([]int{2,2,2,0,1}))
}

/* 0162.Find-Peak-Element/
A peak element is an element that is greater than its neighbors.
Given an input array nums, where nums[i] ≠ nums[i+1], find a peak element and return its index.
The array may contain multiple peaks, in that case return the index to any one of the peaks is fine.
Input: nums = [1,2,1,3,5,6,4]
Output: 1 or 5 
Explanation: Your function can return either index number 1 where the peak element is 2, 
             or index number 5 where the peak element is 6.
找到山峰的 index */
func findPeakElement(nums []int) int {
	l, r := 0, len(nums)-1
	for l<r{
		mid := (l+r)/2
		if nums[mid+1] >= nums[mid]{
			l = mid+1
		} else {
			r = mid
		}
	}
	return l
}
func f162(){
	fmt.Println(findPeakElement([]int{1,2,1,3,5,6,4}))
}

/* 0167.Two-Sum-II-Input-array-is-sorted/
找出两个数之和等于 target 的两个数字，要求输出它们的下标。注意一个数字不能使用 2 次。下标从小到大输出。假定题目一定有一个解。
Input: numbers = [2,7,11,15], target = 9
Output: [1,2]
Explanation: The sum of 2 and 7 is 9. Therefore index1 = 1, index2 = 2. */
func twoSum167(numbers []int, target int) []int {
	m := make(map[int]int)
	for i:=0; i<len(numbers); i++{
		another := target - numbers[i]
		if idx, ok := m[another]; ok {
			return []int{idx+1, i+1}
		}
		m[numbers[i]] = i
	}
	return nil
}
// 解法二 由于数组有序, 可以用二分搜索
func f167(){
	fmt.Println(twoSum167([]int{2,7,11,15}, 9))
}

/* 0209.Minimum-Size-Subarray-Sum/
给定一个整型数组和一个数字 s，找到数组中最短的一个连续子数组，使得连续子数组的数字之和 sum>=s，返回最短的连续子数组的返回值。

Input: s = 7, nums = [2,3,1,2,4,3]
Output: 2
Explanation: the subarray [4,3] has the minimal length under the problem constraint.
*/
// 自己写的双指针, 思路是一样的但不够优雅
func minSubArrayLen(target int, nums []int) int {
	l, r, s := 0,0,0
	res := len(nums)+1
	for r<len(nums) {
		if s < target {
			s += nums[r]
			r++
		} 
		// 把 res = min(res, r-l+1) 这句放到 for 里面, 就和解法二一样不要 if 判断了
        if s>=target{
            for s>= target {
                s -= nums[l]
                l++
            }
            res = min(res, r-l+1)
        }
	}
	if res == len(nums)+1{
		return 0
	}
	return res
}
func minSubArrayLen2(target int, nums []int) int {
	left, sum, res := 0, 0, len(nums)+1
	for right, v  := range nums {
		sum+=v
		for sum >= target{
			res = min(res, right-left+1)
			sum -= nums[left]
			left++
		}
	}
	if res == len(nums)+1 {
		return 0
	}
	return res
}
func f209(){
	fmt.Println(minSubArrayLen(7, []int{2,3,1,2,4,3}))
}

/* 0222.Count-Complete-Tree-Nodes/
输出一颗完全二叉树的结点个数。
Definition of a complete binary tree from Wikipedia: In a complete binary tree every level, except possibly the last, is completely filled, and all nodes in the last level are as far left as possible. It can have between 1 and 2^h nodes inclusive at the last level h. */

 // =================== Main ===================================
func main(){
	f209()
}