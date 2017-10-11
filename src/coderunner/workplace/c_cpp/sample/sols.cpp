#include "sols.h"
class Solution{
    public:
        vector<int> twoSum(vector<int>& nums, int target) {
            map<int, int> chk;
            for (int i = 0; i < nums.size(); i++) {
                if (chk.find(target - nums[i]) == chk.end()) {
                    chk[nums[i]] = i;
                } else {
                    return {chk[target - nums[i]], i};
                }
            }
            return {0, 0};
        }
};
