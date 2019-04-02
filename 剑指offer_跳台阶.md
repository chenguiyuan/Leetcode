# 题目描述
一只青蛙一次可以跳上1级台阶，也可以跳上2级。求该青蛙跳上一个n级的台阶总共有多少种跳法（先后次序不同算不同的结果）。
原题链接：https://www.nowcoder.com/practice/8c82a5b80378478f9484d87d1c5f12a4?tpId=13&tqId=11161&tPage=1&rp=1&ru=/ta/coding-interviews&qru=/ta/coding-interviews/question-ranking

## 题目解析
其实就是斐波那契数列。

**递归方法**
```
class Solution {
public:
    int jumpFloor(int number) {
        if (number==1)
            return 1;
        else if (number==2)
            return 2;
        return jumpFloor(number-1) +　jumpFloor(number-2);
    }
}
```
**迭代方法**
```
class Solution {
public:
    int jumpFloor(int number) {
      int f = 0;
      int g = 1;
     while(number--)
     {
        g += f;
        f = g-f; 
    } 
    return f;
    }
}
```
