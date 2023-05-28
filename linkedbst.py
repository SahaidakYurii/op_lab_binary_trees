"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from linkedqueue import LinkedQueue
from math import log
from random import shuffle, choice
from time import time
import sys
sys.setrecursionlimit(1000000)

class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            string = ""
            if node is not None:
                string += recurse(node.right, level + 1)
                string += "| " * level
                string += str(node.data) + "\n"
                string += recurse(node.left, level + 1)
            return string

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        node = self._root
        while node:
            if item == node.data:
                return node.data
            if item < node.data:
                node = node.left
            else:
                node = node.right

        return None

        # def recurse(node):
        #     if node is None:
        #         return None
        #     elif item == node.data:
        #         return node.data
        #     elif item < node.data:
        #         return recurse(node.left)
        #     else:
        #         return recurse(node.right)

        # return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        if self.isEmpty():
            self._root = BSTNode(item)
            self._size += 1
            return
        
        node = self._root
        while node:
            if item < node.data:
                if node.left:
                    node = node.left
                else:
                    node.left = BSTNode(item)
                    self._size += 1
                    return
            if item > node.data:
                if node.right:
                    node = node.right
                else:
                    node.right = BSTNode(item)
                    self._size += 1
                    return
        # # Helper function to search for item's position
        # def recurse(node):
        #     # New item is less, go left until spot is found
        #     if item < node.data:
        #         if node.left == None:
        #             node.left = BSTNode(item)
        #         else:
        #             recurse(node.left)
        #     # New item is greater or equal,
        #     # go right until spot is found
        #     elif node.right == None:
        #         node.right = BSTNode(item)
        #     else:
        #         recurse(node.right)
        #         # End of recurse

        # # Tree is empty, so new item goes at the root
        # if self.isEmpty():
        #     self._root = BSTNode(item)
        # # Otherwise, search for the item's spot
        # else:
        #     recurse(self._root)
        # self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_in_left_subtree_to_top(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right == None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        removed_item = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node == None:
            if current_node.data == item:
                removed_item = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if removed_item == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left == None \
                and not current_node.right == None:
            lift_max_in_left_subtree_to_top(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left == None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return removed_item

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with new_item and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top: BSTNode):
            '''
            Helper function
            :param top:
            :return: int
            '''
            if not top:
                return 0
            if not top.left and not top.right:
                return 0
            if top.left and top.right:
                return max(height1(top.left), height1(top.right)) + 1
            if top.left:
                return height1(top.left) + 1
            return height1(top.right) + 1

        return height1(self._root)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        return (2 * log(len(self)+1, 2) - 1) > self.height()

    def range_find(self, low = None, high = None):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''

        def recurse(top: BSTNode, low = None, high = None):
            result = []
            if (not low or top.data >= low) and (not high or top.data <= high):
                result.append(top.data)
            if top.left:
                if not low or top.left.data >= low:
                    result = recurse(top.left, low, high) + result
            if top.right:
                if not high or top.right.data <= high:
                    result += recurse(top.right, low, high)
            return result

        return recurse(self._root, low, high)

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        elements = self.range_find()
        self.clear()

        def recurse(elem: list):
            if len(elem) == 0:
                return

            mid_idx = len(elem)//2
            self.add(elem[mid_idx])
            if len(elem) == 1:
                return

            recurse(elem[:mid_idx])
            recurse(elem[mid_idx+1:])

        recurse(elements)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        elems = self.range_find(low=item)
        if elems is None:
            return None
        if elems[0] == item:
            if len(elems) < 2:
                return None
            return elems[1]
        return elems[0]

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        elems = self.range_find(high=item)
        if elems is None:
            return None
        if elems[-1] == item:
            if len(elems) < 2:
                return None
            return elems[-2]
        return elems[-1]

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        with open(path, 'r', encoding='utf-8') as src:
            # 50000 is a number of words to be added to dictionary
            lst = [word.strip() for word in src.readlines()[:50000]]

        lin_tree = LinkedBST()
        rand_tree = LinkedBST()
        bal_tree = LinkedBST()

        for i, word in enumerate(lst):
            lin_tree.add(word)
            bal_tree.add(word)
            if i % 5000 == 0:
                print(f"{i}\twords added")

        bal_tree.rebalance()

        rand_lst = lst[:]
        shuffle(rand_lst)
        for word in rand_lst:
            rand_tree.add(word)

        timers = {"list": {"time": 0.0, "link": lst},
                  "linear_tree": {"time": 0.0, "link": lin_tree},
                  "random_tree": {"time": 0.0, "link": rand_tree},
                  "balanced_tree": {"time": 0.0, "link": bal_tree}}

        for iter in range(10000):
            word = choice(lst)
            for value in timers.values():
                structure = value["link"]
                start = time()
                _ = word in structure
                value["time"] += time() - start

        print("Time of search of 10000 different words in dictionary of 50000")
        for name, element in timers.items():
            sec = element["time"]
            print(f"{name} search time is:\t{sec}")


if __name__ == "__main__":
    tree = LinkedBST()
    tree.demo_bst("words.txt")
