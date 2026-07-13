// Kadane's Algorithm — Optimal

class Solution {
public:
    int maxSubArray(vector<int>& nums) {
     int n = nums.size();
     int sum=0,maxsum=nums[0];
    for(int num:nums){
        sum+=num;
        maxsum=max(sum,maxsum);
        if(sum<0){sum=0;}
    }
     return maxsum;
    }
};

/*

*/