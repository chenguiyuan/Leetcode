"""
94.二叉树的中序遍历
两种方法
1、递归实现
用时28ms，内存10.8MB
2、非递归实现
算法流程：a.根节点入栈
        b.循环执行如下操作：若栈顶节点的左孩子存在则左孩子入栈，
        否则栈顶节点出栈，然后检查该节点的右孩子是否存在，若存在则右孩子进栈，否则继续出栈
        c.栈空时算法停止
注意while的条件，只有当栈空并且节点全部遍历完才能跳出循环。
用时36ms，内存10.7MB

知识点
1、list中append和extend的区别
append追加的list保持原先的格式，extend则是相当于接了一个list上去。
2、取出list中最后一个元素用pop
3、Python中空值是None而不是Null
Python
>>> list1=['a','b']
>>> list1.append(['c', 'd'])
>>> list1
['a', 'b', ['c', 'd']]

>>> list1
['a', 'b']
>>> list1.extend(['c', 'd'])
>>> list1
['a', 'b', 'c', 'd']
"""
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None


class Solution(object):
    def inorderTraversal(self, root):
        """
        :type root: TreeNode
        :rtype: List[int]
        """
        res = []
        if not root:
            return res
        if root.left:
            res.extend(self.inorderTraversal(root.left))
        res.append(root.val)
        if root.right:
            res.extend(self.inorderTraversal(root.right))
        return res


# 非递归实现
class Solution(object):
    def inorderTraversal(self, root):
        """
        :type root: TreeNode
        :rtype: List[int]
        """
        stack = []
        res = []
        node = root
        if not node:
            return res
        while node or len(stack) > 0:
            if node:
                stack.append(node)
                node = node.left
            else:
                node = stack.pop()
                res.append(node.val)
                node = node.right
        return res
