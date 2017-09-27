package utils;
import java.util.HashMap;
import objs.DoubleLinkedListNode;

public class LRUCache {
  private HashMap<Integer, DoubleLinkedListNode> map = 
    new HashMap<Integer, DoubleLinkedListNode>();
  private DoubleLinkedListNode head;
  private DoubleLinkedListNode tail;
  private int capacity;
  private int len;

  public LRUCache(int capacity) {
    this.capacity = capacity;
  }

  public int get(int key) {
    if (map.containsKey(key)) {
      DoubleLinkedListNode latest = map.get(key);
      removeNode(latest);
      setHead(latest);
      return latest.val;
    } else {
      return -1;
    }
  }

  public void set(int key, int value) {
    if (map.containsKey(key)) {
      DoubleLinkedListNode oldNode = map.get(key);
      oldNode.val = value;
      removeNode(oldNode);
      setHead(oldNode);
    } else {
      DoubleLinkedListNode newNode = new DoubleLinkedListNode(key, value);
      if (len < capacity) {
        setHead(newNode);
        map.put(key, newNode);
        len++;
      } else {
        map.remove(tail.key);
        tail = tail.prev;
        if (tail != null) tail.next = null;
        setHead(newNode);
        map.put(key, newNode);
      }
    }
  }
  public void setHead(DoubleLinkedListNode node) {
    node.next = head;
    node.prev = null;
    if (head != null) head.prev = node;
    head = node;
  }

  public void removeNode(DoubleLinkedListNode node) {
    DoubleLinkedListNode p = node.prev;
    DoubleLinkedListNode n = node.next;
    if (p != null) {
      p.next = n;
    } else {
      head = n;
    }
    if (n != null) {
      n.prev = p;
    } else {
      tail = p;
    }
  }
}
