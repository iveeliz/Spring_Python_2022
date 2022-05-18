class Solution(object):
    def twoSum(self, nums, target):
        
        set = {}
        
        for i, n in enumerate(nums):
            
            difference = target - n
            
            if difference in set:
                return set[difference], i
            
            set[n] = i