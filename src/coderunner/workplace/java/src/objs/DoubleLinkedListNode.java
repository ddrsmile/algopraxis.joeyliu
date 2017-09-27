package objs;

public class DoubleLinkedListNode {
  public int val;
  public int key;
  public DoubleLinkedListNode prev;
  public DoubleLinkedListNode next;
  public DoubleLinkedListNode(int key, int val) {
    this.key = key;
    this.val = val;
    prev = null;
    next = null;
  }
}
