
#include <vector>
#include "objs/listnode.h"

using namespace std;

class ListNodes {
    public:
        // constructor
        ListNodes();
        // methods
        ListNode* getList(vector<int> digits);
        ListNode* cvtNum2List(int num);
        ListNode* getCycleList(vector<int> digits, int point);
        ListNode* reverse(ListNode* head);
};

ListNodes::ListNodes() {}

ListNode* ListNodes::getList(vector<int> digits) {
    ListNode* head = new ListNode(-1);
    ListNode* tmp = head;
    for (auto it = digits.begin(); it != digits.end(); it++) {
        tmp->next = new ListNode(*it);
        tmp = tmp->next;
    }
    return head->next;
}

ListNode* ListNodes::cvtNum2List(int num) {
    if (num == 0) {
        return new ListNode(0);
    }
    ListNode* head = new ListNode(-1);
    ListNode* tmp = head;
    for (; num > 0; num /= 10) {
        tmp->next = new ListNode(num%10);
        tmp = tmp->next;
    }
    return head->next;
}

ListNode* ListNodes::getCycleList(vector<int> digits, int point) {
    ListNode* head = this->getList(digits);
    if (head == NULL || head->next == NULL) {
        return head;
    }
    if (point > 0) point--;
    ListNode* f = head;
    ListNode* l = head;
    while (l->next) l = l->next;
    while (point > 0) f = f->next;
    l->next = f;
    return head->next;
}

ListNode* ListNodes::reverse(ListNode* head) {
    if (head == NULL || head->next == NULL) return head;
    ListNode* current = head;
    ListNode* previous = NULL;

    while (current) {
        ListNode* tmp = current;
        current = current->next;
        tmp->next = previous;
        previous = tmp;
    }
    return previous;
}