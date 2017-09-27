# -*- coding: utf-8 -*-
from coderunner.python.objs.ListNode import ListNode

class ListNodes(object):

    def get_list(self, digits):
        head = ListNode(-1)

        if not digits:
            return head.next

        p = head
        for i in digits:
            p.next = ListNode(i)
            p = p.next
        return head.next

    def get_reversed_num_list(self, num):
        head = ListNode(-1)
        if not num:
            return ListNode(0)

        p = head
        while num > 0:
            p.next = ListNode(num%10)
            p = p.next
            num /= 10

        return head.next

    def get_cycle_list(self, digits, point):
        head = self.get_list(digits)
        if not point:
            point = 1

        f = head
        l = head
        
        while l.next:
            l = l.next
        while point > 0:
            f = f.next
            point -= 1
        l.next = f
        return head

    def reserve(self, head):
        if not head or not head.next:
            return head

        c = head
        p = None 
        while c:
            tmp = c
            c = c.next
            tmp.next = p
            p = tmp
        return p

    def show_list(self, head):
        if not head:
            print("None")
            return None
        out = '['
        while head.next:
            out += str(head.val) + ', '
            head = head.next
        out += str(head.val) + ']'
        print(out)