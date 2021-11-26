package main

import (
	"fmt"
	"math"
	"sort"
)

// =================== 辅助函数 ======================
func abs(a int) int {
	if a > 0 {
		return a
	}
	return -a
}


// =================== 主体 ======================

/* 0001.Two-Sum/ 找到两数之和为某一个值
Given an array of integers, return indices of the two numbers such that they add up to a specific target.
You may assume that each input would have exactly one solution, and you may not use the same element twice. 
Given nums = [2, 7, 11, 15], target = 9,
Because nums[0] + nums[1] = 2 + 7 = 9,
return [0, 1]
思路：顺序扫描存到 map 中
*/
func twoSum(nums []int, target int) []int {
	m := make(map[int]int)
	for i := 0; i < len(nums); i++ {
		another := target - nums[i]
		if _, ok := m[another]; ok {
			return []int{m[another], i}
		}
		m[nums[i]] = i
	}
	return nil
}
func f1() {
	a := []int{2, 7, 11, 15}
	result := twoSum(a, 9)
	fmt.Println(result)
}

// 4
func f4(){

}


/* 0011.Container-With-Most-Water/
Given n non-negative integers a1, a2, …, an , where each represents a point at coordinate (i, ai). n vertical lines are drawn such that the two endpoints of line i is at (i, ai) and (i, 0). Find two lines, which together with x-axis forms a container, such that the container contains the most water.
Input: [1,8,6,2,5,4,8,3,7]
Output: 49  // 8 & 7
思路：对撞指针
*/
func maxArea(height []int) int {
	max, start, end := 0, 0, len(height)-1
	for start < end {
		width := end - start
		high := 0
		if height[start] < height[end] {
			high = height[start]
			start++
		} else {
			high = height[end]
			end--
		}

		temp := width * high
		if temp > max {
			max = temp
		}
	}
	return max
}
func f11() {
	height := []int{1, 8, 6, 2, 5, 4, 8, 3, 7}
	result := maxArea(height)
	fmt.Println(result)
}

/* 0015.3Sum/ 找到数组中和为零的三个数
Given an array nums of n integers, are there elements a, b, c in nums such that a + b + c = 0? Find all unique triplets in the array which gives the sum of zero.
Given array nums = [-1, 0, 1, 2, -1, -4],
A solution set is:
[
  [-1, 0, 1],
  [-1, -1, 2]
]
思路：遍历一个数（这里是中间的数字 index），然后对撞指针查找
需要注意的是要避免重复
*/
func threeSum(nums []int) [][]int {
	// 先排序
	sort.Ints(nums)
	// 这里的主循环是 index （中间的数），因此下面的循环条件是 start 和 end 在 index 两侧
	// 为了避免重复，要求排好序的三个数字，每一位都不重复，即下面的三个 && 所进行的判断
	result, start, end, index, addNum, length := make([][]int, 0), 0, 0, 0, 0, len(nums)
	for index=1; index<length-1; index++ {
		start, end = 0, length-1
		if index > 1 && nums[index] == nums[index-1]{
			start = index -1
		}
		for start < index && end > index {
			if start > 0 && nums[start] == nums[start-1]{
				start++
				continue
			}
			if end < length-1 && nums[end] == nums[end+1] {
				end--
				continue
			}
			addNum = nums[start] + nums[end] + nums[index]
			if addNum == 0{
				result = append(result, []int{nums[start], nums[index], nums[end]})
				start++
				end--
			} else if addNum > 0 {
				end--
			} else {
				start++
			}
		}
	}
	return result
}
func f15() {
	nums := []int{-1, 0, 1, 2, -1, -4}
	result := threeSum(nums)
	fmt.Println(result)
}

/* 0016.3Sum-Closest 找到数组中和最接近某个值的三个数
Given an array nums of n integers and an integer target, find three integers in nums such that the sum is closest to target. Return the sum of the three integers. You may assume that each input would have exactly one solution.

Given array nums = [-1, 2, 1, -4], and target = 1.
The sum that is closest to the target is 2. (-1 + 2 + 1 = 2).
思路：遍历第一个数 i，然后在其他（排好序）的数字中对撞指针查找
*/

func threeSumClosest(nums []int, target int) int {
	n := len(nums)
	res, diff := 0, math.MaxInt32
	if (n>2) {
		sort.Ints(nums)
		for i:=0; i<n-2; i++ {
			if i>0 && nums[i-1]==nums[i] {
				continue
			}
			for j,k:=i+1, n-1; j<k;{
				sum:=nums[i]+nums[j]+nums[k]
				if (abs(sum-target) < diff) {
					diff, res = abs(sum-target), sum
				}
				if diff == 0 {
					return res
				} else if (sum<target) {
					j++
				} else {
					k--
				}
			}
		}
	}
	return res
}
func f16(){
	nums:= []int{-1, 2, 1, -4}
	result := threeSumClosest(nums, 1)
	fmt.Println(result)
}



 func main() {
	// f15()
	// f16()

 }