# 题目内容
- 原题链接：https://leetcode-cn.com/contest/weekly-contest-134/problems/moving-stones-until-consecutive/
- 题目内容
三枚石子放置在数轴上，位置分别为 a，b，c。

每一回合，我们假设这三枚石子当前分别位于位置 x, y, z 且 x < y < z。从位置 x 或者是位置 z 拿起一枚石子，并将该石子移动到某一整数位置 k 处，其中 x < k < z 且 k != y。

当你无法进行任何移动时，即，这些石子的位置连续时，游戏结束。

要使游戏结束，你可以执行的最小和最大移动次数分别是多少？ 以长度为 2 的数组形式返回答案：answer = [minimum_moves, maximum_moves]

 

示例 1：

输入：a = 1, b = 2, c = 5
输出：[1, 2]
解释：将石子从 5 移动到 4 再移动到 3，或者我们可以直接将石子移动到 3。
示例 2：

输入：a = 4, b = 3, c = 2
输出：[0, 0]
解释：我们无法进行任何移动。
 

提示：

1 <= a <= 100
1 <= b <= 100
1 <= c <= 100
a != b, b != c, c != a
# 解题思路
首先对a, b, c三个数进行从大到小排序
-最小的移动次数为1有以下情况：
1. a+1=c and b+1!=c
2. a+1!=c and b+1=c
3. b-a=2 or c-b=2 这种情况如1， 3， 5直接将1上的石子放在4的位置上只需要移动一次
- 最大移动次数只需要将最大位置的石子和最小位置的石子依次一格一格往中间位置的石子移动即可。  
```
class Solution(object):
    def numMovesStones(self, a, b, c):
        """
        :type a: int
        :type b: int
        :type c: int
        :rtype: List[int]
        """
        alist = [a, b, c]
        alist = sorted(alist)
        minmove, maxmove = 0, 0
        if alist[0] + 1 != alist[1]:
            minmove += 1
            maxmove += alist[1] - alist[0] -1
        if alist[1] + 1 != alist[2]:
            minmove += 1
            maxmove += alist[2] - alist[1] -1
        if alist[1] - alist[0] == 2 or alist[2] - alist[1] == 2:
            minmove = 1
        return [minmove, maxmove]
```
