#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>

using namespace std;

class Solution {
public:
    void printVector(vector<int>& v) {
        // for (int i = 0; i < v.size(); i++) {
        //     cout << v[i] << " ";
        // }
        for (auto a:v)  count << v << " ";
        cout << endl;
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

int main() {
    Solution s;
    s.testTwoSum();
    return 0;
}
