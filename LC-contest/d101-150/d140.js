/* 3300. 替换为数位和以后的最小元素 #easy 将数组中每个数字都替换为数位和 */
/**
 * @param {number[]} nums
 * @return {number}
 */
var minElement = function(nums) {
    for (let i = 0; i < nums.length; i++) {
        nums[i] = nums[i].toString().split('').reduce((a, b) => a + parseInt(b), 0);
    }
    return Math.min(...nums);
};

/* 3301. 高度互不相同的最大塔高和 #medium 每个位置有一个最大高度限制, 要为每个位置设置一个高度, 使得各不相等的情况下, 求最大和, 不满足返回 -1 
思路: 排序
*/
/**
 * @param {number[]} maximumHeight
 * @return {number}
 */
var maximumTotalSum = function(maximumHeight) {
    maximumHeight.sort((a, b) => b - a);
    var acc = 0;
    var preMax = maximumHeight[0] + 1;
    for (let x of maximumHeight) {
        if (preMax == 1) return -1;
        var y = Math.min(preMax - 1, x);
        acc += y;
        preMax = y;
    }
    return acc;
};

// main
var results = [
    // minElement(nums = [10,12,13,14]),
    maximumTotalSum(maximumHeight = [2,3,4,3]),
];
for (let r of results) {
    console.log(r);
}

