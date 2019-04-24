# 1029. 两地调度  
## 题目内容

    用户通过次数 299
    用户尝试次数 494
    通过次数 305
    提交次数 985
    题目难度 Easy
    公司计划面试 2N 人。第 i 人飞往 A 市的费用为 costs[i][0]，飞往 B 市的费用为 costs[i][1]。
    
    返回将每个人都飞到某座城市的最低费用，要求每个城市都有 N 人抵达。
    
     
    
    示例：
    
    输入：[[10,20],[30,200],[400,50],[30,20]]
    输出：110
    解释：
    第一个人去 A 市，费用为 10。
    第二个人去 A 市，费用为 30。
    第三个人去 B 市，费用为 50。
    第四个人去 B 市，费用为 20。
    
    最低总费用为 10 + 30 + 50 + 20 = 110，每个城市都有一半的人在面试。
     
    
    提示：
    
    1 <= costs.length <= 100
    costs.length 为偶数
    1 <= costs[i][0], costs[i][1] <= 1000

# 解题方案
本方案参考自https://blog.csdn.net/qq_32424059/article/details/89430616
## 思路
算出每个人到A、B两城费用差的绝对值并按此从大到小排列，现将选择费用差较大的情况选择费用较小的城市。
```
class Solution(object):
    def twoCitySchedCost(self, costs):
        """
        :type costs: List[List[int]]
        :rtype: int
        """
        costs = sorted(costs, key= lambda x: abs(x[0] - x[1]))
        costs = costs[::-1]
        a, b = 0, 0
        res = 0
        n = len(costs) // 2
        for i, cost in enumerate(costs):
            if cost[0] <= cost[1] and a<n and b<=n:
                a += 1
                res += cost[0]
            elif cost[0] > cost[1] and a<=n and b<n:
                b += 1
                res += cost[1]
            elif a<n and b>=n:
                a += 1
                res += cost[0]
            else:
                b += 1
                res += cost[1] 
        return res
            
```


