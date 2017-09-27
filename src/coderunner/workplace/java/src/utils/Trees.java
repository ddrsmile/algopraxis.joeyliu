package utils;
import objs.TreeNode;
import java.util.ArrayList;
import java.util.Queue;
import java.util.LinkedList;

public class Trees{
  //Build Binary Tree
  public TreeNode getBT(String nodes) {
    if (nodes.length() == 0) return null;
    String[] vals = nodes.split(",");
    TreeNode root = new TreeNode(Integer.parseInt(vals[0]));
    Queue<TreeNode> q = new LinkedList<TreeNode>();
    q.add(root);

    final int half = vals.length/2;

    for (int i = 0; i < half; i++) {
      if (!vals[i].equals("#")) {
        TreeNode c = q.poll();
        int left = 2*i + 1;
        int right = 2*i + 2;
        if (!vals[left].equals("#")) {
          c.left = new TreeNode(Integer.parseInt(vals[left]));
          q.add(c.left);
        }

        if (right < vals.length && !vals[right].equals("#")) {
          c.right = new TreeNode(Integer.parseInt(vals[right]));
          q.add(c.right);
        }
      }
    }
    return root;
  }
  
  //Build Binary Search Tree by converting sorted Array
  public TreeNode getBST(int[] nums, int low, int high) {
    if (low > high) return null;
    int mid = low + (high - low) / 2;
    TreeNode node = new TreeNode(nums[mid]);
    node.left = getBST(nums, low, mid - 1);
    node.right = getBST(nums, mid + 1, high);
    return node;
  }

}
