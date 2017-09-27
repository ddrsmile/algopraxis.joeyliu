package utils;
import objs.ListNode;

public class ListNodes {
    
  public ListNode getList(int[] digits) {
    ListNode head = new ListNode(-1);
    if (digits.length == 0) {
      return head.next;
    }

    ListNode p = head;
    for (int i = 0; i < digits.length; i++) {
      p.next = new ListNode(digits[i]);
      p = p.next;
    }
    return head.next;
  }

  public ListNode getReserveNumList(int num) {
    ListNode head = new ListNode(-1);
    if (num == 0) {
      head.next = new ListNode(0);
      return head.next;
    }
    ListNode p = head;
    for (; num > 0; num /= 10) {
      p.next = new ListNode(num%10);
      p = p.next;
    }
    return head.next;
  }

  public ListNode getCycleList(int[] digits, int point) {
    ListNode head = getList(digits);
    if (head == null || head.next == null) return head;
    if (point == 0) point = 1;
    ListNode f = head, l = head;
    while (l.next != null) l = l.next;
    for (int i = 0; i < point - 1; i++) f = f.next;
    l.next = f;
    return head;
  }
  
  public ListNode reverse(ListNode head) {
    if (head == null || head.next == null) return head;
    ListNode c = head;
    ListNode p = null;
    while (c != null) {
      ListNode tmp = c;
      c = c.next;
      tmp.next = p;
      p = tmp;
    }
    return p;
  }

  public void showList(ListNode head) {
      if (head == null) {
          System.out.println("[]");
          return;
      }
      ListNode tmp = head;
      System.out.print("[");
      while (tmp.next != null) {
          System.out.print(tmp.val + ", ");
          tmp = tmp.next;
      }
      System.out.println(tmp.val + "]");
  }
}