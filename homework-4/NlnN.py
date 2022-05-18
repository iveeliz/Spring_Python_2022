class Solution(object):
    def twoSum(self, nums, target):
        
        #binary search
        
        nums = sorted(enumerate(nums), key=lambda i: i[1])
        
        a = 0 
        b = len(nums) - 1
        
        while a < b:
            
            s = nums[a][1] + nums[b][1]
            
            if s > target:
                b -= 1
                
            if s < target:
                a += 1
                
            if s == target:
                return nums[a][0], nums[b][0]