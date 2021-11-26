package main

import "fmt"

func max(i,j int) int {
	if i<j{
		return j
	}
	return i
}

func maxDistance(colors []int) int {
	if colors[0] != colors[len(colors)-1] {
		return len(colors)-1
	} else {
		res := 0
		currColor := colors[0]
		for i:=0; i<len(colors);i++ {
			if colors[i] != currColor {
				res=max(res, len(colors)-i-1)
				break
			}
		}
		for i:=len(colors)-1; i>=0;i-- {
			if colors[i] != currColor {
				res = max(res, i)
				break
			}
		}
		return res
	}
}
func c1(){
	fmt.Println(maxDistance([]int{1,1,1,6,1,1,1}))
}
func wateringPlants(plants []int, capacity int) int {
	res, remains:=0,capacity
	for i:=0; i<len(plants); i++ {
		if remains >= plants[i] {
			res ++
			remains -= plants[i]
		} else {
			res += 2*i+1
			remains = capacity - plants[i]
		}
	}
	return res
}
func c2(){
	fmt.Println(wateringPlants([]int{7,7,7,7,7,7,7}, 8))
}

type RangeFreqQuery struct {

}


func Constructor(arr []int) RangeFreqQuery {

}


func (this *RangeFreqQuery) Query(left int, right int, value int) int {

}


/**
 * Your RangeFreqQuery object will be instantiated and called as such:
 * obj := Constructor(arr);
 * param_1 := obj.Query(left,right,value);
 */