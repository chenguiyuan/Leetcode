class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        map = {}
        for i, num in enumerate(nums):
            if target - num in map:
                return([map[target - num], i])
            else:
                map[num] = i

solution = Solution()
nums = [2, 8, 7, 11, 5, 9]
target = 11
print(solution.twoSum2(nums, target))