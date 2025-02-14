# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        Pos = Atual = ListNode()
        while list1 and list2:
            if list1.val < list2.val:
                Atual.next = list1
                list1 = list1.next
            else:
                Atual.next = list2
                list2 = list2.next
            Atual = Atual.next
        if list1:
            Atual.next = list1
        elif list2:
            Atual.next = list2
        
        return Pos.next
        