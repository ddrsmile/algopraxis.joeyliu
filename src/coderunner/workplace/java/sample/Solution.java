import java.util.*;
public class Solution {
  public int[] twoSum(int[] nums, int target) {
    int[] res = {-1, -1};
    Map<Integer, Integer> map = new HashMap<Integer, Integer>();
    for (int i = 0; i < nums.length; i++) {
      if (map.containsKey(target - nums[i])) {
        res[0] = map.get(target - nums[i]);
        res[1] = i + 1;
        break;
      } else {
        map.put(nums[i], i + 1);
      }
    }
    return res;
  }
}
