/* 
@2025-06-09
https://leetcode.cn/contest/biweekly-contest-141
*/


/* 3314. 构造最小位运算数组 I 对于输入的一个质数数组, 给每个数字找到最小的 x, 满足 x or x+1 == number[i]
限制: n 100; val 1000 且为质数
思路1: #位运算
    观察可以发现, 
        特殊: 2 无法分解, 其他都可以!
        7 = 0b111, 这种类型, 需要 0b11 即可, 因为最高位的1可以进位得到;
        5 = 0b101, 这种类型, 需要 0b100, 无法进位;
    综上, 若后缀有k个1, 结果变为 k-1 个 1
*/
/**
 * @param {number[]} nums
 * @return {number[]}
 */
function minBitwiseArray(nums) {
    var ans = [];
    for (let num of nums) {
        var suffix = 0;
        while (num > 0 && num % 2 == 1) {
            suffix++;
            num = Math.floor(num / 2);
        }
        if (suffix == 0) {
            ans.push(-1);
        } else {
            ans.push((num << suffix) + (1 << (suffix-1)) - 1);
        }
    }
    return ans;
};

/* 3316. 从原字符串里进行删除操作的最多次数 #medium 已有 source 和其一个子序列 pattern. 给定下标集合, 问最多可以将其中多少的额index对应source字符删除, 仍满足 pattern为子序列
限制: n 3e3
 */
/**
 * @param {string} source
 * @param {string} pattern
 * @param {number[]} targetIndices
 * @return {number}
 */
var maxRemovals = function(source, pattern, targetIndices) {
    
};


var results = [
    minBitwiseArray([2, 3, 5, 7]),
];
for (let r of results) {
    console.log(r);
}
