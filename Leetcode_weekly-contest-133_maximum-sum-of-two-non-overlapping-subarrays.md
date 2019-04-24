﻿# 题目内容
```
给出非负整数数组 A ，返回两个非重叠（连续）子数组中元素的最大和，子数组的长度分别为 L 和 M。（这里需要澄清的是，长为 L 的子数组可以出现在长为 M 的子数组之前或之后。）

从形式上看，返回最大的 V，而 V = (A[i] + A[i+1] + ... + A[i+L-1]) + (A[j] + A[j+1] + ... + A[j+M-1]) 并满足下列条件之一：

 

0 <= i < i + L - 1 < j < j + M - 1 < A.length, 或
0 <= j < j + M - 1 < i < i + L - 1 < A.length.
 

示例 1：

输入：A = [0,6,5,2,2,5,1,9,4], L = 1, M = 2
输出：20
解释：子数组的一种选择中，[9] 长度为 1，[6,5] 长度为 2。
示例 2：

输入：A = [3,8,1,3,2,1,8,9,0], L = 3, M = 2
输出：29
解释：子数组的一种选择中，[3,8,1] 长度为 3，[8,9] 长度为 2。
示例 3：

输入：A = [2,1,5,6,0,9,5,0,3,8], L = 4, M = 3
输出：31
解释：子数组的一种选择中，[5,6,0,9] 长度为 4，[0,3,8] 长度为 3。
 

提示：

L >= 1
M >= 1
L + M <= A.length <= 1000
0 <= A[i] <= 1000
```
题目链接：https://leetcode-cn.com/contest/weekly-contest-133/problems/maximum-sum-of-two-non-overlapping-subarrays/

# 解题思路
- 先分别求L、M连续子数组和，再进行匹配找到组合后的最大值，匹配时的条件是i+L-1 < j 或者 j+M-1 < i（即L在M左边或者L在M右边，且不重叠）。
```
class Solution(object):
    def maxSumTwoNoOverlap(self, A, L, M):
        """
        :type A: List[int]
        :type L: int
        :type M: int
        :rtype: int
        """
        Lmap, Rmap = dict(), dict()
        num = 0
        for i in range(len(A) - L + 1):
            if i == 0:
                Lmap[i] = sum(A[:L])
            else:
                Lmap[i] = Lmap[i-1] - A[i-1] + A[i+L-1]
        
        for i in range(len(A) - M + 1):
            if i == 0:
                Rmap[i] = sum(A[:M])
            else:
                Rmap[i] = Rmap[i-1] - A[i-1] + A[i+M-1]
                
        for i in range(len(A) - L + 1 ):
            for j in range(len(A) - M + 1):
                if i+L-1 < j or j+M-1 < i:
                    num = max(num, Lmap[i] + Rmap[j])
                    
        return num
                    
```