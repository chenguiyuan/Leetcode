# 题目描述
一只青蛙一次可以跳上1级台阶，也可以跳上2级……它也可以跳上n级。求该青蛙跳上一个n级的台阶总共有多少种跳法。
原题链接：https://www.nowcoder.com/practice/22243d016f6b47f2a6928b4313c85387?tpId=13&tqId=11162&tPage=1&rp=1&ru=/ta/coding-interviews&qru=/ta/coding-interviews/question-ranking

## 题目解析
其实是一个找规律的题，试着把跳1级、2级、3级、4级台阶的情况写出来，可以得到一个数列[1, 2, 4, 8, 16.....]，可以总结得出一个公式：

>                | 1       ,(n=0 ) 
> 
>     f(n) =     | 1       ,(n=1 )
> 
>                | 2*f(n-1),(n>=2)

```
class Solution {
public:
    int jumpFloorII(int number) {
        if（numbe<=0）
              return 0;
        return pow(2, number - 1);
    }
};
```
运行时间：4ms，运行内存450K。



