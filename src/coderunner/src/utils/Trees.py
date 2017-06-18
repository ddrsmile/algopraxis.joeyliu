# -*- coding: utf-8 -*-
from coderunner.python.objs.TreeNode import TreeNode
from queue import Queue

class Trees(object):

    def get_BT(self, nodes):
        if not nodes:
            return None

        vals = nodes.split(',')
        root = TreeNode(int(vals[0]))
        q = Queue()
        q.put(root)

        half = len(vals)//2

        for i in range(half):
            if not vals[i] == "#":
                c = q.get()
                left = 2*i + 1
                right = 2*i + 2

                if not vals[left] == "#":
                    c.left = TreeNode(int(vals[left]))
                    q.put(c.left)

                if right < len(vals) and  not vals[right] == "#":
                    c.right = TreeNode(int(vals[right]))
                    q.put(c.right)
        return root

    def get_BST(self, nums, low, high):
        if low > high:
            return None
        mid = low + (high - low)/2
        node = TreeNode(nums[mid])
        node.left = self.get_BST(nums, low, mid - 1)
        node.right = self.get_BST(nums, mid + 1, high)
        return node

