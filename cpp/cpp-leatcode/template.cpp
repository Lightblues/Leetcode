#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>

using namespace std;

class Solution {
public:
    // 打印输出
    void printVector(vector<int>& v) {
        for (auto a:v) cout << a << " ";
        cout << endl;
    }
    void printInt(int a) {
        cout << a << endl;
    }
    void printString(string s) {
        cout << s << endl;
    }

/* 0001. 两数之和 */
    vector<int> twoSum(vector<int>& nums, int target) {
        unordered_map<int, int> hashtable;
        for (int i = 0; i < nums.size(); ++i) {
            auto it = hashtable.find(target - nums[i]);
            if (it != hashtable.end()) {
                return {it->second, i};
            }
            hashtable[nums[i]] = i;
        }
        return {};
    }
    void testTwoSum(){
        vector<int> nums = {2, 7, 11, 15};
        vector<int> result = twoSum(nums, 9);
        printVector(result);
        nums = {3, 2, 4};
        result = twoSum(nums, 6);
        printVector(result);
    }




};

Solution s;
// vector<int> ans = {
//     // s.numberOfMatches(7),
//     // s.numberOfMatches(8),
//     // s.minPartitions("11"),
//     // s.minPartitions("27346209830709182346"),
// };

int main() {
    s.testTwoSum();



    return 0;
}
